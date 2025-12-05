// Popup script for Chrome extension settings

const apiUrlInput = document.getElementById('apiUrl');
const modelSelect = document.getElementById('model');
const languageSelect = document.getElementById('language');
const saveBtn = document.getElementById('saveBtn');
const status = document.getElementById('status');

// Load saved settings on popup open
document.addEventListener('DOMContentLoaded', loadSettings);

// Save settings
saveBtn.addEventListener('click', saveSettings);

// Load settings from storage
function loadSettings() {
  chrome.runtime.sendMessage({ action: 'getSettings' }, (response) => {
    if (response) {
      apiUrlInput.value = response.apiUrl || 'http://localhost:5000';
      modelSelect.value = response.model || 'blip';
      languageSelect.value = response.language || '';
    }
  });
}

// Save settings to storage
function saveSettings() {
  const settings = {
    apiUrl: apiUrlInput.value.trim(),
    model: modelSelect.value,
    language: languageSelect.value
  };
  
  // Validate API URL
  if (!settings.apiUrl) {
    showStatus('Please enter a valid API URL', 'error');
    return;
  }
  
  chrome.runtime.sendMessage({
    action: 'saveSettings',
    ...settings
  }, (response) => {
    if (response && response.success) {
      showStatus('Settings saved successfully!', 'success');
    } else {
      showStatus('Failed to save settings', 'error');
    }
  });
}

// Show status message
function showStatus(message, type) {
  status.textContent = message;
  status.className = `status ${type}`;
  status.style.display = 'block';
  
  setTimeout(() => {
    status.style.display = 'none';
  }, 3000);
}
