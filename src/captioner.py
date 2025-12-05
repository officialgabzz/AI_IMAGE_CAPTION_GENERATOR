"""
Image Captioner Module
Handles image caption generation using pre-trained transformer models.
"""

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import logging
from typing import Dict, Optional, Union
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageCaptioner:
    """
    A class to generate captions for images using pre-trained models.
    Supports BLIP and GIT models from Hugging Face.
    """

    SUPPORTED_MODELS = {
        "blip": "Salesforce/blip-image-captioning-large",
        "git": "microsoft/git-base-coco",
    }

    def __init__(
        self,
        model_name: str = "blip",
        device: Optional[str] = None,
        cache_dir: Optional[str] = None,
    ):
        """
        Initialize the ImageCaptioner.

        Args:
            model_name: Name of the model to use ('blip' or 'git')
            device: Device to run the model on ('cpu', 'cuda', or 'mps')
            cache_dir: Directory to cache downloaded models
        """
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Model {model_name} not supported. Choose from {list(self.SUPPORTED_MODELS.keys())}"
            )

        self.model_name = model_name
        self.model_id = self.SUPPORTED_MODELS[model_name]

        # Set device
        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
        else:
            self.device = device

        logger.info(f"Using device: {self.device}")

        # Set cache directory
        self.cache_dir = cache_dir or os.path.join(
            os.path.expanduser("~"), ".cache", "image-captioner"
        )
        os.makedirs(self.cache_dir, exist_ok=True)

        # Load model and processor
        self._load_model()

    def _load_model(self):
        """Load the model and processor from Hugging Face."""
        try:
            logger.info(f"Loading {self.model_name} model...")

            if self.model_name == "blip":
                self.processor = BlipProcessor.from_pretrained(
                    self.model_id, cache_dir=self.cache_dir
                )
                self.model = BlipForConditionalGeneration.from_pretrained(
                    self.model_id, cache_dir=self.cache_dir
                ).to(self.device)
            elif self.model_name == "git":
                self.processor = AutoProcessor.from_pretrained(
                    self.model_id, cache_dir=self.cache_dir
                )
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_id, cache_dir=self.cache_dir
                ).to(self.device)

            self.model.eval()
            logger.info(f"Model {self.model_name} loaded successfully!")

        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def generate_caption(
        self,
        image: Union[str, Image.Image],
        max_length: int = 50,
        num_beams: int = 5,
        temperature: float = 1.0,
    ) -> Dict[str, Union[str, float]]:
        """
        Generate a caption for the given image.

        Args:
            image: Path to image file or PIL Image object
            max_length: Maximum length of generated caption
            num_beams: Number of beams for beam search
            temperature: Sampling temperature (higher = more random)

        Returns:
            Dictionary containing caption and confidence score
        """
        try:
            # Load image if path is provided
            if isinstance(image, str):
                image = Image.open(image).convert("RGB")
            elif not isinstance(image, Image.Image):
                raise ValueError("Image must be a file path or PIL Image object")

            # Preprocess image
            inputs = self.processor(image, return_tensors="pt").to(self.device)

            # Generate caption
            with torch.no_grad():
                if self.model_name == "blip":
                    output = self.model.generate(
                        **inputs,
                        max_length=max_length,
                        num_beams=num_beams,
                        temperature=temperature,
                        early_stopping=True,
                    )
                elif self.model_name == "git":
                    output = self.model.generate(
                        pixel_values=inputs.pixel_values,
                        max_length=max_length,
                        num_beams=num_beams,
                    )

            # Decode caption
            caption = self.processor.decode(output[0], skip_special_tokens=True)

            # Calculate confidence (simplified - based on output probability)
            confidence = self._calculate_confidence(output)

            logger.info(f"Generated caption: {caption}")

            return {
                "caption": caption.strip(),
                "confidence": confidence,
                "model": self.model_name,
            }

        except Exception as e:
            logger.error(f"Error generating caption: {str(e)}")
            raise

    def _calculate_confidence(self, output: torch.Tensor) -> float:
        """
        Calculate a confidence score for the generated caption.
        This is a simplified version - in production, you might want more sophisticated scoring.

        Args:
            output: Model output tensor

        Returns:
            Confidence score between 0 and 1
        """
        # Simplified confidence calculation
        # In practice, you'd use the model's logits to calculate actual probability
        return 0.85  # Placeholder - can be enhanced with actual probability calculation

    def batch_generate_captions(
        self, images: list, max_length: int = 50, num_beams: int = 5
    ) -> list:
        """
        Generate captions for multiple images in batch.

        Args:
            images: List of image paths or PIL Image objects
            max_length: Maximum length of generated caption
            num_beams: Number of beams for beam search

        Returns:
            List of dictionaries containing captions and metadata
        """
        results = []
        for image in images:
            try:
                result = self.generate_caption(image, max_length, num_beams)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing image: {str(e)}")
                results.append({"caption": None, "error": str(e)})

        return results

    def switch_model(self, model_name: str):
        """
        Switch to a different model.

        Args:
            model_name: Name of the model to switch to
        """
        if model_name == self.model_name:
            logger.info(f"Already using {model_name}")
            return

        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Model {model_name} not supported. Choose from {list(self.SUPPORTED_MODELS.keys())}"
            )

        # Clear current model from memory
        del self.model
        del self.processor
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

        # Load new model
        self.model_name = model_name
        self.model_id = self.SUPPORTED_MODELS[model_name]
        self._load_model()

        logger.info(f"Switched to {model_name} model")


# Convenience function for quick usage
def caption_image(
    image_path: str, model: str = "blip", device: Optional[str] = None
) -> str:
    """
    Quick function to generate a caption for an image.

    Args:
        image_path: Path to the image file
        model: Model to use ('blip' or 'git')
        device: Device to run on

    Returns:
        Generated caption as string
    """
    captioner = ImageCaptioner(model_name=model, device=device)
    result = captioner.generate_caption(image_path)
    return result["caption"]


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        caption = caption_image(image_path)
        print(f"Caption: {caption}")
    else:
        print("Usage: python captioner.py <image_path>")
