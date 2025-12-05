"""
Flask Web Application - AI Image Caption Generator
Main application file with REST API and web interface.
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from src.captioner import ImageCaptioner
from src.translator import CaptionTranslator
from src.utils.image_processor import ImageProcessor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_CONTENT_LENGTH", 10485760))  # 10MB
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")

# Enable CORS
CORS(app)

# Create upload folder
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize components
logger.info("Initializing AI models...")
captioner = ImageCaptioner(
    model_name=os.getenv("DEFAULT_MODEL", "blip"),
    device=os.getenv("DEVICE", None),
)
translator = CaptionTranslator()
image_processor = ImageProcessor()

logger.info("Application initialized successfully!")


@app.route("/")
def index():
    """Render the main web interface."""
    return render_template("index.html")


@app.route("/api/caption", methods=["POST"])
def generate_caption():
    """
    API endpoint to generate captions for uploaded images.

    Expected form data:
        - image: Image file (required)
        - language: Target language code (optional)
        - model: Model to use - 'blip' or 'git' (optional)

    Returns:
        JSON response with caption and metadata
    """
    try:
        # Check if image is present
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image file provided"}), 400

        file = request.files["image"]

        if file.filename == "":
            return jsonify({"success": False, "error": "No file selected"}), 400

        # Validate file extension
        if not image_processor.check_file_extension(file.filename):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Invalid file type. Allowed: {', '.join(image_processor.ALLOWED_EXTENSIONS)}",
                    }
                ),
                400,
            )

        # Read and validate image
        file_data = file.read()
        if not image_processor.validate_image(file_data):
            return jsonify({"success": False, "error": "Invalid image file"}), 400

        # Preprocess image
        image = image_processor.preprocess_image(file_data)

        # Get optional parameters
        target_language = request.form.get("language", None)
        model_name = request.form.get("model", os.getenv("DEFAULT_MODEL", "blip"))

        # Switch model if needed
        if model_name != captioner.model_name:
            captioner.switch_model(model_name)

        # Generate caption
        logger.info(f"Generating caption with {model_name} model")
        caption_result = captioner.generate_caption(image)

        response_data = {
            "success": True,
            "caption": caption_result["caption"],
            "confidence": caption_result["confidence"],
            "model_used": caption_result["model"],
            "timestamp": datetime.now().isoformat(),
        }

        # Translate if language is specified
        if target_language and target_language != "en":
            if translator.is_language_supported(target_language):
                logger.info(f"Translating caption to {target_language}")
                translation_result = translator.translate(
                    caption_result["caption"], target_language
                )
                response_data["translated_caption"] = translation_result[
                    "translated_text"
                ]
                response_data["language"] = target_language
                response_data["language_name"] = translation_result[
                    "target_language_name"
                ]
            else:
                response_data["warning"] = f"Language {target_language} not supported"

        logger.info(f"Caption generated successfully: {caption_result['caption']}")
        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"Error generating caption: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/languages", methods=["GET"])
def get_languages():
    """
    API endpoint to get supported languages.

    Returns:
        JSON response with list of supported languages
    """
    try:
        languages = translator.get_supported_languages()
        formatted_languages = [
            {"code": code, "name": name} for code, name in languages.items()
        ]

        return jsonify({"success": True, "languages": formatted_languages}), 200

    except Exception as e:
        logger.error(f"Error getting languages: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/models", methods=["GET"])
def get_models():
    """
    API endpoint to get supported models.

    Returns:
        JSON response with list of available models
    """
    try:
        models = [
            {
                "name": "blip",
                "display_name": "BLIP (Salesforce)",
                "description": "Bootstrapping Language-Image Pre-training",
            },
            {
                "name": "git",
                "display_name": "GIT (Microsoft)",
                "description": "Generative Image-to-text Transformer",
            },
        ]

        return (
            jsonify(
                {"success": True, "models": models, "current_model": captioner.model_name}
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.

    Returns:
        JSON response with application status
    """
    return (
        jsonify(
            {
                "status": "healthy",
                "model": captioner.model_name,
                "device": captioner.device,
                "timestamp": datetime.now().isoformat(),
            }
        ),
        200,
    )


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return (
        jsonify(
            {
                "success": False,
                "error": f"File too large. Maximum size: {app.config['MAX_CONTENT_LENGTH'] / (1024*1024):.1f}MB",
            }
        ),
        413,
    )


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"success": False, "error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"success": False, "error": "Internal server error"}), 500


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"

    logger.info(f"Starting server on {host}:{port}")
    logger.info(f"Debug mode: {debug}")

    app.run(host=host, port=port, debug=debug)
