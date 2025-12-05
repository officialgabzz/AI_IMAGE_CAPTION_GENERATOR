# AI-Based Image Caption Generator 🖼️✨

An open-source intelligent image captioning application powered by state-of-the-art neural networks. Upload any image and get accurate, contextual captions generated automatically using pre-trained transformer models.

## Features

- 🤖 **AI-Powered Captioning**: Uses advanced pre-trained models (BLIP, GIT) for accurate image understanding
- 🌍 **Multilingual Support**: Translate captions into 50+ languages
- 🌐 **Web Interface**: Easy-to-use Flask-based web application
- 🔌 **REST API**: Programmatic access for integration with other services
- 🎨 **Chrome Extension**: Caption any image on the web with a right-click
- ⚡ **Fast & Efficient**: Optimized for quick inference
- 🔒 **Privacy-First**: Process images locally, no data sent to third parties

## Tech Stack

- **Backend**: Python 3.8+
- **Deep Learning**: PyTorch, Transformers (Hugging Face)
- **Web Framework**: Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Translation**: Google Translate API / MarianMT
- **Extension**: Chrome Extension API (Manifest V3)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd community_contrib
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download AI models** (First run will download ~2GB of models)
```bash
python -m src.models.download_models
```

## Usage

### Running the Web Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

### Using the API

**Caption Generation Endpoint**
```bash
curl -X POST -F "image=@path/to/image.jpg" http://localhost:5000/api/caption
```

**With Translation**
```bash
curl -X POST -F "image=@path/to/image.jpg" -F "language=es" http://localhost:5000/api/caption
```

**Response Format**
```json
{
  "success": true,
  "caption": "A dog playing in the park",
  "translated_caption": "Un perro jugando en el parque",
  "language": "es",
  "confidence": 0.92
}
```

### Installing Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select the `chrome-extension` folder from this project
5. Right-click any image on the web and select "Generate Caption"

## Supported Languages

English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese (Simplified), Chinese (Traditional), Arabic, Hindi, and 40+ more languages.

## Project Structure

```
community_contrib/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── LICENSE                     # MIT License
├── .gitignore                 # Git ignore file
├── src/
│   ├── __init__.py
│   ├── captioner.py           # Core caption generation logic
│   ├── translator.py          # Multilingual translation module
│   ├── models/
│   │   ├── __init__.py
│   │   └── download_models.py # Model downloader utility
│   └── utils/
│       ├── __init__.py
│       └── image_processor.py # Image preprocessing utilities
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── templates/
│   └── index.html             # Web interface
├── chrome-extension/
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── popup.html
│   ├── popup.js
│   └── icons/
├── tests/
│   ├── __init__.py
│   ├── test_captioner.py
│   └── test_api.py
└── examples/
    └── sample_images/
```

## Models

This application uses the following pre-trained models:

- **BLIP** (Bootstrapping Language-Image Pre-training): Salesforce's state-of-the-art vision-language model
- **GIT** (Generative Image-to-text Transformer): Microsoft's efficient image captioning model
- **MarianMT**: Neural machine translation for multilingual support

## API Reference

### POST /api/caption

Generate caption for an image.

**Parameters:**
- `image` (file, required): Image file (JPEG, PNG, WebP)
- `language` (string, optional): Target language code (ISO 639-1)
- `model` (string, optional): Model to use ('blip' or 'git', default: 'blip')

**Response:**
```json
{
  "success": true,
  "caption": "string",
  "translated_caption": "string",
  "language": "string",
  "confidence": 0.0-1.0,
  "model_used": "string"
}
```

### GET /api/languages

Get list of supported languages.

**Response:**
```json
{
  "languages": [
    {"code": "en", "name": "English"},
    {"code": "es", "name": "Spanish"},
    ...
  ]
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Performance

- Average inference time: ~1-2 seconds per image (CPU)
- GPU acceleration supported for faster processing
- Supports batch processing for multiple images

## Limitations

- Maximum image size: 10MB
- Supported formats: JPEG, PNG, WebP, BMP
- Caption length: typically 10-20 words
- Translation quality depends on source caption accuracy

## Roadmap

- [ ] Add more pre-trained models (CLIP, ViT-GPT2)
- [ ] Implement fine-tuning capability
- [ ] Add batch processing UI
- [ ] Mobile app (React Native)
- [ ] Docker containerization
- [ ] Cloud deployment guides (AWS, GCP, Azure)
- [ ] Video caption generation
- [ ] Real-time webcam captioning

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Hugging Face Transformers library
- Salesforce Research (BLIP model)
- Microsoft Research (GIT model)
- Flask framework
- PyTorch team

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Citation

If you use this project in your research, please cite:

```bibtex
@software{ai_image_caption_generator,
  author = {Community Contributors},
  title = {AI-Based Image Caption Generator},
  year = {2025},
  url = {https://github.com/yourusername/community_contrib}
}
```

---

Made with ❤️ by the open-source community
