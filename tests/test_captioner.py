"""
Unit tests for Image Captioner module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import torch
from PIL import Image
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.captioner import ImageCaptioner, caption_image


class TestImageCaptioner(unittest.TestCase):
    """Test cases for ImageCaptioner class"""

    @patch("src.captioner.BlipProcessor")
    @patch("src.captioner.BlipForConditionalGeneration")
    def setUp(self, mock_model, mock_processor):
        """Set up test fixtures"""
        self.mock_processor = mock_processor
        self.mock_model = mock_model
        self.captioner = ImageCaptioner(model_name="blip", device="cpu")

    def test_initialization_with_blip(self):
        """Test captioner initialization with BLIP model"""
        self.assertEqual(self.captioner.model_name, "blip")
        self.assertEqual(self.captioner.device, "cpu")

    def test_initialization_with_invalid_model(self):
        """Test initialization with invalid model name"""
        with self.assertRaises(ValueError):
            ImageCaptioner(model_name="invalid_model")

    def test_supported_models(self):
        """Test that supported models are correctly defined"""
        expected_models = {"blip", "git"}
        self.assertEqual(set(ImageCaptioner.SUPPORTED_MODELS.keys()), expected_models)

    @patch("src.captioner.Image")
    def test_generate_caption_with_file_path(self, mock_image):
        """Test caption generation with file path"""
        # Mock image
        mock_img = Mock(spec=Image.Image)
        mock_image.open.return_value = mock_img
        mock_img.convert.return_value = mock_img

        # Mock processor and model
        self.captioner.processor = Mock()
        self.captioner.processor.return_value = {
            "pixel_values": torch.zeros(1, 3, 224, 224)
        }
        self.captioner.processor.decode.return_value = "A test caption"

        self.captioner.model = Mock()
        self.captioner.model.generate.return_value = torch.tensor([[1, 2, 3]])

        # Test
        result = self.captioner.generate_caption("test_image.jpg")

        self.assertIn("caption", result)
        self.assertIn("confidence", result)
        self.assertIn("model", result)
        self.assertEqual(result["model"], "blip")

    def test_calculate_confidence(self):
        """Test confidence calculation"""
        output = torch.tensor([[1, 2, 3]])
        confidence = self.captioner._calculate_confidence(output)

        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)


class TestCaptionImageFunction(unittest.TestCase):
    """Test cases for caption_image convenience function"""

    @patch("src.captioner.ImageCaptioner")
    def test_caption_image(self, mock_captioner_class):
        """Test convenience function"""
        # Mock captioner
        mock_captioner = Mock()
        mock_captioner.generate_caption.return_value = {
            "caption": "Test caption",
            "confidence": 0.9,
            "model": "blip",
        }
        mock_captioner_class.return_value = mock_captioner

        # Test
        result = caption_image("test.jpg", model="blip")

        self.assertEqual(result, "Test caption")
        mock_captioner.generate_caption.assert_called_once_with("test.jpg")


if __name__ == "__main__":
    unittest.main()
