"""
Unit tests for Flask API endpoints
"""

import unittest
import json
import io
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestFlaskAPI(unittest.TestCase):
    """Test cases for Flask API endpoints"""

    @patch("app.ImageCaptioner")
    @patch("app.CaptionTranslator")
    @patch("app.ImageProcessor")
    def setUp(self, mock_processor, mock_translator, mock_captioner):
        """Set up test fixtures"""
        # Import app after mocking
        from app import app

        self.app = app
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True

    def test_index_route(self):
        """Test the index route"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn("status", data)
        self.assertEqual(data["status"], "healthy")

    def test_get_languages(self):
        """Test get languages endpoint"""
        response = self.client.get("/api/languages")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("languages", data)
        self.assertIsInstance(data["languages"], list)

    def test_get_models(self):
        """Test get models endpoint"""
        response = self.client.get("/api/models")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("models", data)
        self.assertIsInstance(data["models"], list)

    def test_caption_no_image(self):
        """Test caption endpoint without image"""
        response = self.client.post("/api/caption")
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("error", data)

    @patch("app.captioner")
    @patch("app.image_processor")
    def test_caption_with_image(self, mock_processor, mock_captioner):
        """Test caption endpoint with valid image"""
        # Mock image processor
        mock_processor.check_file_extension.return_value = True
        mock_processor.validate_image.return_value = True
        mock_processor.preprocess_image.return_value = Mock()

        # Mock captioner
        mock_captioner.model_name = "blip"
        mock_captioner.generate_caption.return_value = {
            "caption": "A test image",
            "confidence": 0.95,
            "model": "blip",
        }

        # Create fake image file
        data = {"image": (io.BytesIO(b"fake image data"), "test.jpg")}

        response = self.client.post(
            "/api/caption", data=data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertTrue(response_data["success"])
        self.assertIn("caption", response_data)

    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
