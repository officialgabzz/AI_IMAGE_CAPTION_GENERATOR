// Content script for Chrome extension

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'generateCaption') {
    generateCaption(request.imageUrl);
  }
});

// Generate caption for image
async function generateCaption(imageUrl) {
  try {
    // Show loading indicator
    showLoadingIndicator();
    
    // Get settings
    const settings = await getSettings();
    
    // Fetch image as blob
    const imageBlob = await fetchImageAsBlob(imageUrl);
    
    // Create form data
    const formData = new FormData();
    formData.append('image', imageBlob, 'image.jpg');
    formData.append('model', settings.model);
    
    if (settings.language) {
      formData.append('language', settings.language);
    }
    
    // Send to API
    const response = await fetch(`${settings.apiUrl}/api/caption`, {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    
    if (data.success) {
      // Show caption
      showCaption(data.caption, data.translated_caption, imageUrl);
      
      // Notify background script
      chrome.runtime.sendMessage({
        action: 'captionGenerated',
        caption: data.translated_caption || data.caption,
        imageUrl: imageUrl
      });
    } else {
      showError(data.error || 'Failed to generate caption');
    }
  } catch (error) {
    console.error('Caption generation error:', error);
    showError('Error generating caption. Make sure the server is running.');
  } finally {
    hideLoadingIndicator();
  }
}

// Fetch image as blob
async function fetchImageAsBlob(imageUrl) {
  const response = await fetch(imageUrl);
  const blob = await response.blob();
  return blob;
}

// Get settings from storage
function getSettings() {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage({ action: 'getSettings' }, (response) => {
      resolve(response);
    });
  });
}

// Show loading indicator
function showLoadingIndicator() {
  const loader = document.createElement('div');
  loader.id = 'ai-caption-loader';
  loader.innerHTML = `
    <div style="
      position: fixed;
      top: 20px;
      right: 20px;
      background: white;
      padding: 16px 24px;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.2);
      z-index: 999999;
      font-family: Arial, sans-serif;
      display: flex;
      align-items: center;
      gap: 12px;
    ">
      <div style="
        width: 20px;
        height: 20px;
        border: 3px solid #e5e7eb;
        border-top-color: #6366f1;
        border-radius: 50%;
        animation: spin 1s linear infinite;
      "></div>
      <span style="color: #111827; font-weight: 500;">Generating caption...</span>
    </div>
    <style>
      @keyframes spin {
        to { transform: rotate(360deg); }
      }
    </style>
  `;
  document.body.appendChild(loader);
}

// Hide loading indicator
function hideLoadingIndicator() {
  const loader = document.getElementById('ai-caption-loader');
  if (loader) {
    loader.remove();
  }
}

// Show caption
function showCaption(caption, translatedCaption, imageUrl) {
  const displayCaption = translatedCaption || caption;
  
  const captionBox = document.createElement('div');
  captionBox.id = 'ai-caption-box';
  captionBox.innerHTML = `
    <div style="
      position: fixed;
      top: 20px;
      right: 20px;
      background: white;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.2);
      z-index: 999999;
      max-width: 400px;
      font-family: Arial, sans-serif;
    ">
      <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
        <h3 style="margin: 0; color: #111827; font-size: 16px; font-weight: 600;">Generated Caption</h3>
        <button id="ai-caption-close" style="
          background: none;
          border: none;
          font-size: 24px;
          cursor: pointer;
          color: #6b7280;
          padding: 0;
          line-height: 1;
        ">×</button>
      </div>
      <p style="color: #374151; margin: 0 0 12px 0; font-size: 15px; line-height: 1.5;">${displayCaption}</p>
      <div style="display: flex; gap: 8px;">
        <button id="ai-caption-copy" style="
          background: #6366f1;
          color: white;
          border: none;
          padding: 8px 16px;
          border-radius: 6px;
          cursor: pointer;
          font-size: 14px;
          font-weight: 500;
        ">Copy</button>
      </div>
    </div>
  `;
  
  document.body.appendChild(captionBox);
  
  // Close button
  document.getElementById('ai-caption-close').addEventListener('click', () => {
    captionBox.remove();
  });
  
  // Copy button
  document.getElementById('ai-caption-copy').addEventListener('click', () => {
    navigator.clipboard.writeText(displayCaption);
    const btn = document.getElementById('ai-caption-copy');
    btn.textContent = '✓ Copied!';
    btn.style.background = '#10b981';
    setTimeout(() => {
      btn.textContent = 'Copy';
      btn.style.background = '#6366f1';
    }, 2000);
  });
  
  // Auto-close after 10 seconds
  setTimeout(() => {
    if (captionBox && captionBox.parentNode) {
      captionBox.remove();
    }
  }, 10000);
}

// Show error
function showError(message) {
  const errorBox = document.createElement('div');
  errorBox.innerHTML = `
    <div style="
      position: fixed;
      top: 20px;
      right: 20px;
      background: #fee2e2;
      border: 2px solid #ef4444;
      padding: 16px 20px;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.2);
      z-index: 999999;
      max-width: 400px;
      font-family: Arial, sans-serif;
    ">
      <p style="color: #991b1b; margin: 0; font-weight: 500;">${message}</p>
    </div>
  `;
  
  document.body.appendChild(errorBox);
  
  setTimeout(() => {
    errorBox.remove();
  }, 5000);
}
