# Getting Started Guide

This guide will help you set up and run the AI Image Caption Generator.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment tool (venv)
- At least 4GB of free disk space (for AI models)
- At least 4GB of RAM (8GB recommended)

## Installation Steps

### 1. Clone or Download the Repository

```bash
cd /Users/garubamalik/Documents/community_contrib
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

On macOS/Linux:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- Flask (web framework)
- PyTorch (deep learning)
- Transformers (pre-trained models)
- Pillow (image processing)
- deep-translator (multilingual support)

### 5. Download AI Models

```bash
python -m src.models.download_models
```

This will download approximately 2GB of pre-trained models. It may take 5-15 minutes depending on your internet connection.

### 6. Configure Environment (Optional)

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` to customize settings:
- `PORT`: Server port (default: 5000)
- `DEFAULT_MODEL`: Default AI model (blip or git)
- `DEVICE`: Processing device (cpu, cuda, or mps)

### 7. Run the Application

```bash
python app.py
```

The server will start at `http://localhost:5000`

### 8. Test the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

You should see the web interface where you can upload images and generate captions.

## Installing the Chrome Extension

### 1. Open Chrome Extensions Page

Navigate to: `chrome://extensions/`

### 2. Enable Developer Mode

Toggle the "Developer mode" switch in the top right corner.

### 3. Load the Extension

1. Click "Load unpacked"
2. Navigate to: `/Users/garubamalik/Documents/community_contrib/chrome-extension`
3. Select the folder and click "Open"

### 4. Create Extension Icons (Optional)

The extension works without custom icons, but you can add them:

```bash
cd chrome-extension/icons
# Create icons using Python or any image editor
python create_icons.py  # If you create this script
```

### 5. Test the Extension

1. Make sure the Flask server is running (`python app.py`)
2. Right-click any image on a webpage
3. Select "Generate Caption for Image"
4. Wait for the caption to appear

## Using the API

### Generate Caption (Python)

```python
import requests

url = "http://localhost:5000/api/caption"
files = {"image": open("path/to/image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Generate Caption with Translation

```python
import requests

url = "http://localhost:5000/api/caption"
files = {"image": open("path/to/image.jpg", "rb")}
data = {"language": "es"}  # Spanish
response = requests.post(url, files=files, data=data)
print(response.json())
```

### Using cURL

```bash
curl -X POST -F "image=@path/to/image.jpg" http://localhost:5000/api/caption
```

## Troubleshooting

### Issue: Models not downloading

**Solution**: Check your internet connection and try again. If problems persist, manually download models:
```bash
python -m src.models.download_models
```

### Issue: Out of memory errors

**Solution**: The models require significant RAM. Try:
1. Close other applications
2. Use a smaller model (switch to 'git' instead of 'blip')
3. Process smaller images

### Issue: Slow caption generation

**Solution**: 
- First run is slower due to model loading
- Use GPU if available (set `DEVICE=cuda` in `.env`)
- On Mac M1/M2, use `DEVICE=mps` for better performance

### Issue: Chrome extension not working

**Solution**:
1. Make sure the Flask server is running
2. Check the extension settings (click extension icon)
3. Verify the API URL is correct (default: `http://localhost:5000`)
4. Check browser console for errors (F12)

### Issue: Translation not working

**Solution**:
- Ensure you have internet connection (Google Translate API requires it)
- Check if the language code is valid
- Try translating to a common language first (es, fr, de)

## Next Steps

- Explore the API documentation in README.md
- Customize the web interface (edit `templates/index.html` and `static/css/style.css`)
- Fine-tune models on your own dataset
- Deploy to a cloud server (AWS, GCP, Azure)

## Getting Help

- Check the main README.md for detailed documentation
- Review test files in `tests/` for usage examples
- Open an issue on GitHub

## Uninstalling

1. Deactivate virtual environment: `deactivate`
2. Remove the project directory
3. Uninstall Chrome extension from `chrome://extensions/`
