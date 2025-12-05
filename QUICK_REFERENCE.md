# Quick Reference Card

## 🚀 Installation (One Command)

```bash
python setup.py
```

## 🎯 Common Commands

### Start Server
```bash
python app.py
```
Access at: http://localhost:5000

### Download Models Only
```bash
python -m src.models.download_models
```

### Run Tests
```bash
pytest tests/
```

### Check Code Style
```bash
black src/ tests/ app.py
flake8 src/ tests/ app.py
```

## 🔌 API Quick Reference

### Generate Caption
```bash
curl -X POST -F "image=@photo.jpg" http://localhost:5000/api/caption
```

### Caption with Translation
```bash
curl -X POST -F "image=@photo.jpg" -F "language=es" http://localhost:5000/api/caption
```

### Get Languages
```bash
curl http://localhost:5000/api/languages
```

### Health Check
```bash
curl http://localhost:5000/api/health
```

## 🐍 Python Quick Examples

### Simple Caption
```python
from src.captioner import caption_image
caption = caption_image("photo.jpg")
print(caption)
```

### With Translation
```python
from src.captioner import ImageCaptioner
from src.translator import CaptionTranslator

captioner = ImageCaptioner()
translator = CaptionTranslator()

result = captioner.generate_caption("photo.jpg")
translated = translator.translate(result["caption"], "es")
print(translated["translated_text"])
```

### Batch Processing
```python
from pathlib import Path
from src.captioner import ImageCaptioner

captioner = ImageCaptioner()
for img in Path("images/").glob("*.jpg"):
    result = captioner.generate_caption(str(img))
    print(f"{img.name}: {result['caption']}")
```

## ⚙️ Environment Variables (.env)

```bash
# Server
HOST=0.0.0.0
PORT=5000
DEBUG=True

# Model
DEFAULT_MODEL=blip  # or 'git'
DEVICE=cpu          # or 'cuda', 'mps'

# Upload
MAX_CONTENT_LENGTH=10485760  # 10MB
```

## 🌐 Chrome Extension Setup

1. Open: `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select: `chrome-extension` folder
5. Right-click any image → "Generate Caption"

## 📁 Important Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `src/captioner.py` | AI captioning logic |
| `src/translator.py` | Translation service |
| `requirements.txt` | Dependencies |
| `.env` | Configuration |

## 🎨 Supported Languages (Top 20)

en, es, fr, de, it, pt, ru, ja, ko, zh-CN, zh-TW, ar, hi, bn, nl, pl, tr, vi, th, sv

See `/api/languages` for all 50+

## 🤖 Available Models

| Model | Description | Speed | Accuracy |
|-------|-------------|-------|----------|
| BLIP | Salesforce | Medium | High |
| GIT | Microsoft | Fast | Good |

## 🔧 Troubleshooting

### Models not downloading?
```bash
python -m src.models.download_models
```

### Out of memory?
- Switch to GIT model (faster, less memory)
- Use smaller images
- Set DEVICE=cpu in .env

### Chrome extension not working?
- Check server is running
- Verify API URL in extension settings
- Check browser console (F12)

### Import errors?
```bash
pip install -r requirements.txt
```

## 📊 Project Structure (Simplified)

```
community_contrib/
├── app.py              # Run this!
├── setup.py            # Or run this first!
├── src/                # Core logic
│   ├── captioner.py
│   ├── translator.py
│   └── utils/
├── static/             # Web UI
├── templates/          # HTML
├── chrome-extension/   # Browser extension
└── tests/              # Unit tests
```

## 🎯 Testing Your Setup

1. **Test Web UI**: Visit http://localhost:5000
2. **Test API**: `curl http://localhost:5000/api/health`
3. **Test Python**: `python -c "from src import captioner"`
4. **Test Extension**: Right-click image in Chrome

## 💡 Tips

- First run downloads ~2GB models
- Use virtual environment
- GPU speeds up processing (CUDA/MPS)
- Keep images under 10MB
- BLIP = better quality, GIT = faster

## 📚 Documentation

| Doc | Content |
|-----|---------|
| README.md | Full documentation |
| GETTING_STARTED.md | Setup guide |
| API_DOCS.md | API reference |
| PROJECT_SUMMARY.md | Overview |

## 🆘 Get Help

1. Check README.md
2. Check GETTING_STARTED.md
3. Run with DEBUG=True
4. Check logs
5. Open GitHub issue

---

**Ready? Run:** `python setup.py` 🚀
