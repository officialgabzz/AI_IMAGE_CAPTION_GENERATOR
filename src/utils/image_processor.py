"""
Image Processing Utilities
Helper functions for image preprocessing and validation.
"""

from PIL import Image
import io
import logging
from typing import Tuple, Optional, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageProcessor:
    """Utility class for image processing operations."""

    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "bmp", "gif"}
    MAX_IMAGE_SIZE = (2048, 2048)  # Max dimensions
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes

    @staticmethod
    def validate_image(file_data: Union[bytes, str]) -> bool:
        """
        Validate if the file is a valid image.

        Args:
            file_data: Image file data (bytes) or file path (str)

        Returns:
            True if valid, False otherwise
        """
        try:
            if isinstance(file_data, str):
                with open(file_data, "rb") as f:
                    Image.open(f).verify()
            else:
                Image.open(io.BytesIO(file_data)).verify()
            return True
        except Exception as e:
            logger.error(f"Image validation failed: {str(e)}")
            return False

    @staticmethod
    def check_file_extension(filename: str) -> bool:
        """
        Check if file has allowed extension.

        Args:
            filename: Name of the file

        Returns:
            True if extension is allowed, False otherwise
        """
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in ImageProcessor.ALLOWED_EXTENSIONS
        )

    @staticmethod
    def resize_image(
        image: Image.Image,
        max_size: Tuple[int, int] = MAX_IMAGE_SIZE,
        maintain_aspect: bool = True,
    ) -> Image.Image:
        """
        Resize image to fit within max_size while maintaining aspect ratio.

        Args:
            image: PIL Image object
            max_size: Maximum dimensions (width, height)
            maintain_aspect: Whether to maintain aspect ratio

        Returns:
            Resized PIL Image object
        """
        if maintain_aspect:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        else:
            image = image.resize(max_size, Image.Resampling.LANCZOS)

        logger.info(f"Image resized to {image.size}")
        return image

    @staticmethod
    def convert_to_rgb(image: Image.Image) -> Image.Image:
        """
        Convert image to RGB mode.

        Args:
            image: PIL Image object

        Returns:
            RGB PIL Image object
        """
        if image.mode != "RGB":
            logger.info(f"Converting image from {image.mode} to RGB")
            image = image.convert("RGB")
        return image

    @staticmethod
    def preprocess_image(
        image_data: Union[bytes, str, Image.Image],
        resize: bool = True,
        max_size: Tuple[int, int] = MAX_IMAGE_SIZE,
    ) -> Image.Image:
        """
        Preprocess image for caption generation.

        Args:
            image_data: Image as bytes, file path, or PIL Image
            resize: Whether to resize the image
            max_size: Maximum dimensions if resizing

        Returns:
            Preprocessed PIL Image object
        """
        try:
            # Load image
            if isinstance(image_data, str):
                image = Image.open(image_data)
            elif isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            elif isinstance(image_data, Image.Image):
                image = image_data
            else:
                raise ValueError("Invalid image data type")

            # Convert to RGB
            image = ImageProcessor.convert_to_rgb(image)

            # Resize if needed
            if resize:
                image = ImageProcessor.resize_image(image, max_size)

            logger.info(f"Image preprocessed successfully. Size: {image.size}")
            return image

        except Exception as e:
            logger.error(f"Image preprocessing error: {str(e)}")
            raise

    @staticmethod
    def get_image_info(image: Union[str, Image.Image]) -> dict:
        """
        Get information about the image.

        Args:
            image: Image path or PIL Image object

        Returns:
            Dictionary with image metadata
        """
        try:
            if isinstance(image, str):
                img = Image.open(image)
            else:
                img = image

            info = {
                "size": img.size,
                "width": img.width,
                "height": img.height,
                "mode": img.mode,
                "format": img.format,
            }

            logger.info(f"Image info: {info}")
            return info

        except Exception as e:
            logger.error(f"Error getting image info: {str(e)}")
            raise

    @staticmethod
    def compress_image(
        image: Image.Image, quality: int = 85, format: str = "JPEG"
    ) -> bytes:
        """
        Compress image to reduce file size.

        Args:
            image: PIL Image object
            quality: Compression quality (1-100)
            format: Output format

        Returns:
            Compressed image as bytes
        """
        try:
            buffer = io.BytesIO()
            image.save(buffer, format=format, quality=quality, optimize=True)
            buffer.seek(0)

            logger.info(f"Image compressed with quality {quality}")
            return buffer.getvalue()

        except Exception as e:
            logger.error(f"Image compression error: {str(e)}")
            raise


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        processor = ImageProcessor()

        # Get image info
        info = processor.get_image_info(image_path)
        print(f"Image Info: {info}")

        # Preprocess image
        processed = processor.preprocess_image(image_path)
        print(f"Preprocessed image size: {processed.size}")
    else:
        print("Usage: python image_processor.py <image_path>")
