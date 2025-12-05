# API Documentation

Complete API reference for the AI Image Caption Generator.

## Base URL

```
http://localhost:5000
```

For production, replace with your deployed server URL.

---

## Authentication

Currently, no authentication is required. For production deployment, consider implementing API keys or OAuth.

---

## Endpoints

### 1. Generate Caption

Generate an AI-powered caption for an uploaded image.

**Endpoint:** `POST /api/caption`

**Content-Type:** `multipart/form-data`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image | file | Yes | Image file (JPEG, PNG, WebP, BMP) |
| language | string | No | Target language code (ISO 639-1) |
| model | string | No | Model to use: 'blip' or 'git' (default: 'blip') |

**Example Request (cURL):**

```bash
curl -X POST \
  http://localhost:5000/api/caption \
  -F "image=@/path/to/image.jpg" \
  -F "language=es" \
  -F "model=blip"
```

**Example Request (Python):**

```python
import requests

url = "http://localhost:5000/api/caption"
files = {"image": open("image.jpg", "rb")}
data = {
    "language": "es",
    "model": "blip"
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

**Success Response (200):**

```json
{
  "success": true,
  "caption": "A dog playing in the park",
  "translated_caption": "Un perro jugando en el parque",
  "confidence": 0.92,
  "model_used": "blip",
  "language": "es",
  "language_name": "Spanish",
  "timestamp": "2025-12-05T10:30:00.000Z"
}
```

**Error Response (400):**

```json
{
  "success": false,
  "error": "No image file provided"
}
```

**Error Response (500):**

```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

### 2. Get Supported Languages

Retrieve a list of all supported languages for translation.

**Endpoint:** `GET /api/languages`

**Example Request:**

```bash
curl http://localhost:5000/api/languages
```

**Success Response (200):**

```json
{
  "success": true,
  "languages": [
    {
      "code": "en",
      "name": "English"
    },
    {
      "code": "es",
      "name": "Spanish"
    },
    {
      "code": "fr",
      "name": "French"
    }
    // ... more languages
  ]
}
```

---

### 3. Get Available Models

Get information about available AI models.

**Endpoint:** `GET /api/models`

**Example Request:**

```bash
curl http://localhost:5000/api/models
```

**Success Response (200):**

```json
{
  "success": true,
  "models": [
    {
      "name": "blip",
      "display_name": "BLIP (Salesforce)",
      "description": "Bootstrapping Language-Image Pre-training"
    },
    {
      "name": "git",
      "display_name": "GIT (Microsoft)",
      "description": "Generative Image-to-text Transformer"
    }
  ],
  "current_model": "blip"
}
```

---

### 4. Health Check

Check if the API server is running and healthy.

**Endpoint:** `GET /api/health`

**Example Request:**

```bash
curl http://localhost:5000/api/health
```

**Success Response (200):**

```json
{
  "status": "healthy",
  "model": "blip",
  "device": "cpu",
  "timestamp": "2025-12-05T10:30:00.000Z"
}
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Endpoint doesn't exist |
| 413 | Payload Too Large - File exceeds 10MB |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider implementing:
- Rate limiting per IP address
- Request throttling
- API key quotas

---

## Language Codes

Common language codes supported:

| Code | Language |
|------|----------|
| en | English |
| es | Spanish |
| fr | French |
| de | German |
| it | Italian |
| pt | Portuguese |
| ru | Russian |
| ja | Japanese |
| ko | Korean |
| zh-CN | Chinese (Simplified) |
| zh-TW | Chinese (Traditional) |
| ar | Arabic |
| hi | Hindi |

See `/api/languages` endpoint for the complete list of 50+ supported languages.

---

## Usage Examples

### Python SDK Example

```python
import requests
from typing import Optional

class CaptionClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
    
    def caption(self, image_path: str, language: Optional[str] = None, 
                model: str = "blip") -> dict:
        """Generate caption for an image"""
        url = f"{self.base_url}/api/caption"
        
        files = {"image": open(image_path, "rb")}
        data = {"model": model}
        
        if language:
            data["language"] = language
        
        response = requests.post(url, files=files, data=data)
        return response.json()
    
    def get_languages(self) -> dict:
        """Get supported languages"""
        url = f"{self.base_url}/api/languages"
        response = requests.get(url)
        return response.json()

# Usage
client = CaptionClient()
result = client.caption("photo.jpg", language="es")
print(result["caption"])
```

### JavaScript Example

```javascript
async function generateCaption(imageFile, language = null) {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('model', 'blip');
  
  if (language) {
    formData.append('language', language);
  }
  
  const response = await fetch('http://localhost:5000/api/caption', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  return data;
}

// Usage
const fileInput = document.getElementById('image-input');
const file = fileInput.files[0];
const result = await generateCaption(file, 'fr');
console.log(result.caption);
```

### Batch Processing Example

```python
import requests
from pathlib import Path
import json

def batch_caption(image_dir: str, output_file: str, language: str = None):
    """Caption all images in a directory"""
    results = []
    
    for image_path in Path(image_dir).glob("*.{jpg,jpeg,png}"):
        try:
            files = {"image": open(image_path, "rb")}
            data = {"language": language} if language else {}
            
            response = requests.post(
                "http://localhost:5000/api/caption",
                files=files,
                data=data
            )
            
            result = response.json()
            result["filename"] = image_path.name
            results.append(result)
            
            print(f"✓ {image_path.name}: {result.get('caption')}")
            
        except Exception as e:
            print(f"✗ {image_path.name}: {e}")
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {output_file}")

# Usage
batch_caption("./images", "captions.json", language="es")
```

---

## Best Practices

1. **Image Size**: Keep images under 10MB. Resize large images before uploading.

2. **File Formats**: Use JPEG for photos, PNG for screenshots/graphics.

3. **Error Handling**: Always check the `success` field in responses.

4. **Performance**: 
   - First request may be slower (model loading)
   - Subsequent requests are faster
   - Consider caching results for repeated images

5. **Translation**: Only request translation when needed to save processing time.

6. **Model Selection**:
   - Use BLIP for better accuracy
   - Use GIT for faster processing

---

## Limitations

- Maximum file size: 10MB
- Supported formats: JPEG, PNG, WebP, BMP
- Caption length: typically 10-20 words
- Processing time: 1-3 seconds per image (CPU)
- Translation requires internet connection

---

## Support

For issues or questions:
- Open an issue on GitHub
- Check the README.md documentation
- Review test files for usage examples
