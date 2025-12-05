# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                          │
├─────────────┬─────────────────┬──────────────┬─────────────────┤
│  Web Browser│   API Client    │ Python Script│ Chrome Extension│
│  (HTML/CSS) │   (REST API)    │   (Direct)   │   (Context Menu)│
└──────┬──────┴────────┬────────┴──────┬───────┴────────┬─────────┘
       │               │               │                │
       │               │               │                │
       └───────────────┴───────────────┴────────────────┘
                              │
                              ▼
       ┌──────────────────────────────────────────────┐
       │          FLASK WEB APPLICATION                │
       │              (app.py)                         │
       │                                               │
       │  ┌─────────────────────────────────────┐    │
       │  │        REST API Endpoints            │    │
       │  │  • POST /api/caption                 │    │
       │  │  • GET  /api/languages               │    │
       │  │  • GET  /api/models                  │    │
       │  │  • GET  /api/health                  │    │
       │  └─────────────────────────────────────┘    │
       └───────────┬──────────────┬──────────────────┘
                   │              │
                   ▼              ▼
       ┌───────────────┐  ┌──────────────────┐
       │  Image        │  │  Translation     │
       │  Captioner    │  │  Service         │
       │  Module       │  │  Module          │
       └───────┬───────┘  └────────┬─────────┘
               │                    │
               ▼                    ▼
       ┌──────────────────┐  ┌──────────────────┐
       │  Image           │  │  Google          │
       │  Processor       │  │  Translate API   │
       └──────────────────┘  └──────────────────┘
               │
               ▼
       ┌──────────────────────────────────────┐
       │     AI MODELS (PyTorch)               │
       │  ┌────────────┐    ┌──────────────┐  │
       │  │   BLIP     │    │     GIT      │  │
       │  │ (Salesforce)│    │ (Microsoft)  │  │
       │  └────────────┘    └──────────────┘  │
       └──────────────────────────────────────┘
```

## Component Interaction Flow

### Web Interface Flow
```
User uploads image
       │
       ▼
JavaScript validates file
       │
       ▼
FormData created with image + options
       │
       ▼
POST /api/caption
       │
       ▼
Flask receives & validates
       │
       ▼
Image preprocessing
       │
       ▼
AI model generates caption
       │
       ▼
Translation (if requested)
       │
       ▼
JSON response returned
       │
       ▼
UI displays caption
```

### Chrome Extension Flow
```
User right-clicks image
       │
       ▼
Context menu "Generate Caption"
       │
       ▼
Content script extracts image URL
       │
       ▼
Fetch image as blob
       │
       ▼
Send to API server
       │
       ▼
Receive caption response
       │
       ▼
Display caption overlay
       │
       ▼
User can copy caption
```

## Module Dependencies

```
app.py
  ├── src.captioner
  │     ├── torch
  │     ├── transformers
  │     └── PIL
  │
  ├── src.translator
  │     ├── deep_translator
  │     └── langdetect
  │
  ├── src.utils.image_processor
  │     └── PIL
  │
  ├── flask
  ├── flask_cors
  └── werkzeug
```

## Data Flow Diagram

```
┌─────────┐
│  Image  │
│  File   │
└────┬────┘
     │
     ▼
┌──────────────────┐
│ Image Validation │
│ • Size check     │
│ • Format check   │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Preprocessing    │
│ • Resize         │
│ • RGB convert    │
│ • Normalize      │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Model Processor  │
│ • Tokenize       │
│ • Create tensors │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ AI Model         │
│ • BLIP/GIT       │
│ • Beam search    │
│ • Generate       │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Decode Output    │
│ • Text caption   │
│ • Confidence     │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ Translation      │ (Optional)
│ • Detect lang    │
│ • Translate      │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│ JSON Response    │
│ • Caption        │
│ • Translation    │
│ • Metadata       │
└──────────────────┘
```

## File Structure with Responsibilities

```
community_contrib/
│
├── app.py                          [Web Server & API Routing]
│   • Flask app initialization
│   • Route handling
│   • Request/response management
│   • Error handling
│
├── src/
│   ├── captioner.py               [AI Caption Generation]
│   │   • Model loading
│   │   • Image-to-text inference
│   │   • Confidence scoring
│   │
│   ├── translator.py              [Multilingual Translation]
│   │   • Language detection
│   │   • Caption translation
│   │   • 50+ language support
│   │
│   └── utils/
│       └── image_processor.py     [Image Preprocessing]
│           • Validation
│           • Resizing
│           • Format conversion
│
├── static/
│   ├── css/style.css              [UI Styling]
│   │   • Responsive design
│   │   • Animations
│   │
│   └── js/main.js                 [Frontend Logic]
│       • File upload handling
│       • API communication
│       • UI updates
│
├── templates/
│   └── index.html                 [Web Interface]
│       • Upload form
│       • Result display
│
├── chrome-extension/
│   ├── manifest.json              [Extension Config]
│   ├── background.js              [Service Worker]
│   │   • Context menu
│   │   • Message handling
│   │
│   ├── content.js                 [Page Interaction]
│   │   • Image extraction
│   │   • Caption display
│   │
│   └── popup.html/js              [Extension Settings]
│       • Configuration UI
│
└── tests/
    ├── test_captioner.py          [Unit Tests]
    └── test_api.py                [API Tests]
```

## Technology Stack Map

```
┌────────────────────────────────────────────────┐
│                  Frontend                      │
│  ┌──────────────────────────────────────┐     │
│  │ HTML5 │ CSS3 │ JavaScript (Vanilla)  │     │
│  └──────────────────────────────────────┘     │
└─────────────────┬──────────────────────────────┘
                  │ HTTP/REST
┌─────────────────▼──────────────────────────────┐
│                  Backend                       │
│  ┌──────────────────────────────────────┐     │
│  │ Flask │ Flask-CORS │ Werkzeug        │     │
│  └──────────────────────────────────────┘     │
│  ┌──────────────────────────────────────┐     │
│  │ Python 3.8+ │ dotenv                 │     │
│  └──────────────────────────────────────┘     │
└─────────────────┬──────────────────────────────┘
                  │
┌─────────────────▼──────────────────────────────┐
│              AI/ML Layer                       │
│  ┌──────────────────────────────────────┐     │
│  │ PyTorch │ Transformers (HuggingFace) │     │
│  └──────────────────────────────────────┘     │
│  ┌──────────────────────────────────────┐     │
│  │ BLIP Model │ GIT Model               │     │
│  └──────────────────────────────────────┘     │
└─────────────────┬──────────────────────────────┘
                  │
┌─────────────────▼──────────────────────────────┐
│            Supporting Services                 │
│  ┌──────────────────────────────────────┐     │
│  │ Pillow │ NumPy                       │     │
│  └──────────────────────────────────────┘     │
│  ┌──────────────────────────────────────┐     │
│  │ deep-translator │ langdetect         │     │
│  └──────────────────────────────────────┘     │
└────────────────────────────────────────────────┘
```

## Deployment Architecture (Future)

```
                    ┌──────────────┐
                    │   End Users  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Load Balancer│
                    └──────┬───────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
    ┌───────▼────────┐          ┌────────▼───────┐
    │  Web Server 1  │          │  Web Server 2  │
    │  (Flask App)   │          │  (Flask App)   │
    └───────┬────────┘          └────────┬───────┘
            │                             │
            └──────────────┬──────────────┘
                           │
                    ┌──────▼───────┐
                    │  Model Cache │
                    │  (Shared)    │
                    └──────────────┘
                           │
                    ┌──────▼───────┐
                    │   Database   │
                    │  (Optional)  │
                    └──────────────┘
```

## Security Considerations

```
┌─────────────────────────────────────┐
│      Security Measures              │
├─────────────────────────────────────┤
│ • File type validation              │
│ • File size limits (10MB)           │
│ • Image format verification         │
│ • CORS configuration                │
│ • Input sanitization                │
│ • Error message sanitization        │
│ • No persistent storage (privacy)   │
│ • Local model processing            │
└─────────────────────────────────────┘
```

## Performance Optimization

```
┌────────────────────────────────────────┐
│        Performance Strategy            │
├────────────────────────────────────────┤
│ Model Loading                          │
│  • Load once at startup                │
│  • Keep in memory                      │
│  • Lazy loading option                 │
├────────────────────────────────────────┤
│ Image Processing                       │
│  • Resize before processing            │
│  • Batch processing support            │
│  • GPU acceleration (optional)         │
├────────────────────────────────────────┤
│ Caching                                │
│  • Model weights cached                │
│  • Static assets cached                │
│  • Browser caching enabled             │
└────────────────────────────────────────┘
```

---

This architecture supports:
- ✅ Scalability
- ✅ Maintainability
- ✅ Extensibility
- ✅ Performance
- ✅ Security
- ✅ Privacy
