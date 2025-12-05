// Main JavaScript for Image Caption Generator

// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const imageInput = document.getElementById('imageInput');
const previewSection = document.getElementById('previewSection');
const imagePreview = document.getElementById('imagePreview');
const removeBtn = document.getElementById('removeBtn');
const modelSelect = document.getElementById('modelSelect');
const languageSelect = document.getElementById('languageSelect');
const generateBtn = document.getElementById('generateBtn');
const resultSection = document.getElementById('resultSection');
const captionText = document.getElementById('captionText');
const confidence = document.getElementById('confidence');
const modelUsed = document.getElementById('modelUsed');
const translationBox = document.getElementById('translationBox');
const translationText = document.getElementById('translationText');
const languageName = document.getElementById('languageName');
const copyBtn = document.getElementById('copyBtn');
const newBtn = document.getElementById('newBtn');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const languageCount = document.getElementById('languageCount');

// State
let selectedFile = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadLanguages();
    setupEventListeners();
});

// Load supported languages
async function loadLanguages() {
    try {
        const response = await fetch('/api/languages');
        const data = await response.json();
        
        if (data.success) {
            languageCount.textContent = data.languages.length;
            
            data.languages.forEach(lang => {
                const option = document.createElement('option');
                option.value = lang.code;
                option.textContent = lang.name;
                languageSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading languages:', error);
    }
}

// Setup event listeners
function setupEventListeners() {
    // Upload box click
    uploadBox.addEventListener('click', () => imageInput.click());
    
    // File input change
    imageInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadBox.addEventListener('dragover', handleDragOver);
    uploadBox.addEventListener('dragleave', handleDragLeave);
    uploadBox.addEventListener('drop', handleDrop);
    
    // Remove button
    removeBtn.addEventListener('click', resetUpload);
    
    // Generate button
    generateBtn.addEventListener('click', generateCaption);
    
    // Copy button
    copyBtn.addEventListener('click', copyCaption);
    
    // New image button
    newBtn.addEventListener('click', resetAll);
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

// Handle drag over
function handleDragOver(event) {
    event.preventDefault();
    uploadBox.classList.add('dragover');
}

// Handle drag leave
function handleDragLeave(event) {
    event.preventDefault();
    uploadBox.classList.remove('dragover');
}

// Handle drop
function handleDrop(event) {
    event.preventDefault();
    uploadBox.classList.remove('dragover');
    
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        processFile(file);
    } else {
        showError('Please drop a valid image file');
    }
}

// Process selected file
function processFile(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file');
        return;
    }
    
    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('File size must be less than 10MB');
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        uploadBox.style.display = 'none';
        previewSection.style.display = 'block';
        generateBtn.disabled = false;
        hideError();
    };
    reader.readAsDataURL(file);
}

// Reset upload
function resetUpload() {
    selectedFile = null;
    imageInput.value = '';
    imagePreview.src = '';
    uploadBox.style.display = 'block';
    previewSection.style.display = 'none';
    generateBtn.disabled = true;
    hideError();
}

// Reset all
function resetAll() {
    resetUpload();
    resultSection.style.display = 'none';
    modelSelect.value = 'blip';
    languageSelect.value = '';
}

// Generate caption
async function generateCaption() {
    if (!selectedFile) return;
    
    // Show loading
    loading.style.display = 'block';
    resultSection.style.display = 'none';
    hideError();
    generateBtn.disabled = true;
    
    // Prepare form data
    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('model', modelSelect.value);
    
    if (languageSelect.value) {
        formData.append('language', languageSelect.value);
    }
    
    try {
        const response = await fetch('/api/caption', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'Failed to generate caption');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please try again.');
    } finally {
        loading.style.display = 'none';
        generateBtn.disabled = false;
    }
}

// Display results
function displayResults(data) {
    // Show caption
    captionText.textContent = data.caption;
    confidence.textContent = `Confidence: ${(data.confidence * 100).toFixed(1)}%`;
    modelUsed.textContent = `Model: ${data.model_used.toUpperCase()}`;
    
    // Show translation if available
    if (data.translated_caption) {
        translationText.textContent = data.translated_caption;
        languageName.textContent = `Translated to ${data.language_name}`;
        translationBox.style.display = 'block';
    } else {
        translationBox.style.display = 'none';
    }
    
    // Show result section
    resultSection.style.display = 'block';
}

// Copy caption to clipboard
async function copyCaption() {
    const textToCopy = languageSelect.value 
        ? translationText.textContent 
        : captionText.textContent;
    
    try {
        await navigator.clipboard.writeText(textToCopy);
        
        // Visual feedback
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied!';
        copyBtn.style.background = '#10b981';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '';
        }, 2000);
    } catch (error) {
        console.error('Copy failed:', error);
        showError('Failed to copy to clipboard');
    }
}

// Show error
function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(hideError, 5000);
}

// Hide error
function hideError() {
    errorMessage.style.display = 'none';
}
