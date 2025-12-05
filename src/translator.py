"""
Translator Module
Handles translation of captions to multiple languages.
"""

from deep_translator import GoogleTranslator
from langdetect import detect
import logging
from typing import Optional, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CaptionTranslator:
    """
    A class to translate image captions to multiple languages.
    """

    # Supported languages with their codes
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh-CN": "Chinese (Simplified)",
        "zh-TW": "Chinese (Traditional)",
        "ar": "Arabic",
        "hi": "Hindi",
        "bn": "Bengali",
        "nl": "Dutch",
        "pl": "Polish",
        "tr": "Turkish",
        "vi": "Vietnamese",
        "th": "Thai",
        "sv": "Swedish",
        "da": "Danish",
        "fi": "Finnish",
        "no": "Norwegian",
        "cs": "Czech",
        "el": "Greek",
        "he": "Hebrew",
        "id": "Indonesian",
        "ms": "Malay",
        "ro": "Romanian",
        "uk": "Ukrainian",
        "hu": "Hungarian",
        "sk": "Slovak",
        "bg": "Bulgarian",
        "hr": "Croatian",
        "sr": "Serbian",
        "sl": "Slovenian",
        "lt": "Lithuanian",
        "lv": "Latvian",
        "et": "Estonian",
        "fa": "Persian",
        "ur": "Urdu",
        "sw": "Swahili",
        "ta": "Tamil",
        "te": "Telugu",
        "kn": "Kannada",
        "ml": "Malayalam",
        "mr": "Marathi",
        "gu": "Gujarati",
    }

    def __init__(self):
        """Initialize the translator."""
        self.translator = None
        logger.info("CaptionTranslator initialized")

    def translate(
        self, text: str, target_language: str, source_language: str = "auto"
    ) -> Dict[str, str]:
        """
        Translate text to the target language.

        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'es', 'fr')
            source_language: Source language code (default: 'auto' for auto-detection)

        Returns:
            Dictionary containing translated text and metadata
        """
        try:
            # Validate target language
            if target_language not in self.SUPPORTED_LANGUAGES:
                raise ValueError(
                    f"Language '{target_language}' not supported. "
                    f"Choose from: {', '.join(self.SUPPORTED_LANGUAGES.keys())}"
                )

            # Detect source language if auto
            if source_language == "auto":
                try:
                    detected_lang = detect(text)
                    logger.info(f"Detected source language: {detected_lang}")
                    source_language = detected_lang
                except Exception as e:
                    logger.warning(f"Could not detect language: {e}. Defaulting to 'en'")
                    source_language = "en"

            # Skip translation if source and target are the same
            if source_language == target_language:
                logger.info("Source and target languages are the same. Skipping translation.")
                return {
                    "translated_text": text,
                    "source_language": source_language,
                    "target_language": target_language,
                    "source_language_name": self.SUPPORTED_LANGUAGES.get(
                        source_language, "Unknown"
                    ),
                    "target_language_name": self.SUPPORTED_LANGUAGES.get(
                        target_language, "Unknown"
                    ),
                }

            # Perform translation
            translator = GoogleTranslator(source=source_language, target=target_language)
            translated_text = translator.translate(text)

            logger.info(
                f"Translated '{text}' from {source_language} to {target_language}: '{translated_text}'"
            )

            return {
                "translated_text": translated_text,
                "source_language": source_language,
                "target_language": target_language,
                "source_language_name": self.SUPPORTED_LANGUAGES.get(
                    source_language, "Unknown"
                ),
                "target_language_name": self.SUPPORTED_LANGUAGES.get(
                    target_language, "Unknown"
                ),
            }

        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise

    def batch_translate(
        self, texts: List[str], target_language: str, source_language: str = "auto"
    ) -> List[Dict[str, str]]:
        """
        Translate multiple texts to the target language.

        Args:
            texts: List of texts to translate
            target_language: Target language code
            source_language: Source language code (default: 'auto')

        Returns:
            List of dictionaries containing translated texts and metadata
        """
        results = []
        for text in texts:
            try:
                result = self.translate(text, target_language, source_language)
                results.append(result)
            except Exception as e:
                logger.error(f"Error translating text '{text}': {e}")
                results.append(
                    {
                        "translated_text": None,
                        "error": str(e),
                        "original_text": text,
                    }
                )

        return results

    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get a dictionary of supported languages.

        Returns:
            Dictionary with language codes as keys and language names as values
        """
        return self.SUPPORTED_LANGUAGES.copy()

    def is_language_supported(self, language_code: str) -> bool:
        """
        Check if a language is supported.

        Args:
            language_code: Language code to check

        Returns:
            True if supported, False otherwise
        """
        return language_code in self.SUPPORTED_LANGUAGES

    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of the given text.

        Args:
            text: Text to detect language from

        Returns:
            Language code or None if detection fails
        """
        try:
            lang_code = detect(text)
            logger.info(f"Detected language: {lang_code} ({self.SUPPORTED_LANGUAGES.get(lang_code, 'Unknown')})")
            return lang_code
        except Exception as e:
            logger.error(f"Language detection error: {str(e)}")
            return None


# Convenience function
def translate_caption(
    caption: str, target_language: str, source_language: str = "auto"
) -> str:
    """
    Quick function to translate a caption.

    Args:
        caption: Caption text to translate
        target_language: Target language code
        source_language: Source language code (default: 'auto')

    Returns:
        Translated caption as string
    """
    translator = CaptionTranslator()
    result = translator.translate(caption, target_language, source_language)
    return result["translated_text"]


if __name__ == "__main__":
    # Example usage
    translator = CaptionTranslator()

    # Test translation
    text = "A dog playing in the park"
    result = translator.translate(text, "es")
    print(f"Original: {text}")
    print(f"Translated to Spanish: {result['translated_text']}")

    # Show supported languages
    print(f"\nSupported languages: {len(translator.get_supported_languages())}")
    for code, name in list(translator.get_supported_languages().items())[:10]:
        print(f"  {code}: {name}")
