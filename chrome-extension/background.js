// Background service worker for Chrome extension

// Create context menu item on installation
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'generateCaption',
    title: 'Generate Caption for Image',
    contexts: ['image']
  });
  
  console.log('AI Image Caption Generator installed!');
});

// Handle context menu click
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'generateCaption') {
    const imageUrl = info.srcUrl;
    
    // Send message to content script
    chrome.tabs.sendMessage(tab.id, {
      action: 'generateCaption',
      imageUrl: imageUrl
    });
  }
});

// Handle messages from content script or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'captionGenerated') {
    // Store the last generated caption
    chrome.storage.local.set({
      lastCaption: request.caption,
      lastImage: request.imageUrl,
      timestamp: Date.now()
    });
    
    // Send notification
    showNotification(request.caption);
  }
  
  if (request.action === 'getSettings') {
    // Get stored settings
    chrome.storage.local.get(['apiUrl', 'model', 'language'], (result) => {
      sendResponse({
        apiUrl: result.apiUrl || 'http://localhost:5000',
        model: result.model || 'blip',
        language: result.language || ''
      });
    });
    return true; // Keep message channel open for async response
  }
  
  if (request.action === 'saveSettings') {
    // Save settings
    chrome.storage.local.set({
      apiUrl: request.apiUrl,
      model: request.model,
      language: request.language
    }, () => {
      sendResponse({ success: true });
    });
    return true;
  }
});

// Show notification
function showNotification(caption) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icons/icon128.png',
    title: 'Caption Generated',
    message: caption.substring(0, 100) + (caption.length > 100 ? '...' : ''),
    priority: 2
  });
}
