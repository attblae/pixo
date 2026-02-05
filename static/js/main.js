// Account script
let selectedFiles = [];
        
function handleFileSelect(event) {
    selectedFiles = Array.from(event.target.files);
    updateFileInfo();
    showPreview();
    updateUploadButton();
}

function updateFileInfo() {
    const fileInfo = document.getElementById('fileInfo');
    if (selectedFiles.length === 0) {
        fileInfo.innerHTML = '<p style="color:#666;">No files selected</p>';
        return;
    }
    
    fileInfo.innerHTML = `
        <p>Selected files: ${selectedFiles.length}</p>
    `;
}

function showPreview() {
    const container = document.getElementById('previewContainer');
    container.innerHTML = '';
    
    selectedFiles.slice(0, 3).forEach(file => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'preview';
            img.title = file.name;
            container.appendChild(img);
        };
        reader.readAsDataURL(file);
    });
    
    if (selectedFiles.length > 3) {
        const remaining = document.createElement('p');
        remaining.textContent = `... и еще ${selectedFiles.length - 3} files`;
        container.appendChild(remaining);
    }
}

function updateUploadButton() {
    const button = document.getElementById('uploadButton');
    button.disabled = selectedFiles.length === 0;
}

function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

async function uploadFiles() {
    if (selectedFiles.length === 0) {
        showMessage('Please select files', 'error');
        return;
    }
    
    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    
    const uploadButton = document.getElementById('uploadButton');
    const progressContainer = document.getElementById('progressContainer');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    
    // Показываем прогресс
    uploadButton.disabled = true;
    uploadButton.textContent = 'Loading...';
    progressContainer.style.display = 'block';
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        // Имитация прогресса
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            if (progress > 90) {
                clearInterval(interval);
            }
            progressFill.style.width = progress + '%';
            progressText.textContent = progress + '%';
        }, 200);
        
        const result = await response.json();
        
        if (response.ok) {
            // Завершаем прогресс
            progressFill.style.width = '100%';
            progressText.textContent = '100%';
            
            showMessage(`Successfully uploaded ${result.uploaded_files.length} files!`, 'success');
            
            // Очищаем форму
            selectedFiles = [];
            document.getElementById('fileInput').value = '';
            updateFileInfo();
            showPreview();
            updateUploadButton();
            
            // Обновляем список файлов
            await loadUploadedFiles();
            
            // Сбрасываем через 2 секунды
            setTimeout(() => {
                progressContainer.style.display = 'none';
                progressFill.style.width = '0%';
                progressText.textContent = '0%';
            }, 2000);
            
        } else {
            showMessage(`Error: ${result.detail || 'Unknown error'}`, 'error');
        }
        
        clearInterval(interval);
        
    } catch (error) {
        showMessage(`Network error: ${error.message}`, 'error');
    } finally {
        uploadButton.disabled = false;
        uploadButton.textContent = 'Upload your work';
    }
}

async function loadUploadedFiles() {
    try {
        const response = await fetch('/files');
        const files = await response.json();
        
        const container = document.getElementById('filesContainer');
        container.innerHTML = '';
        
        if (files.length === 0) {
            container.innerHTML = '<p>Files have not been uploaded yet.</p>';
            return;
        }
        
        files.forEach(file => {
            const fileDiv = document.createElement('div');
            fileDiv.style.padding = '10px';
            fileDiv.style.borderBottom = '1px solid #eee';
            fileDiv.style.display = 'flex';
            fileDiv.style.justifyContent = 'space-between';
            fileDiv.style.alignItems = 'center';
            
            const sizeKB = (file.size / 1024).toFixed(1);
            
            fileDiv.innerHTML = `
                <div>
                    <p>${file.filename}</p><br>
                    <small><p>${sizeKB} KB</p></small>
                </div>
                <a href="/files/${file.filename}" target="_blank" 
                    style="color:#007bff;text-decoration:underline;margin-left:20px;">
                    View
                </a>
            `;
            
            container.appendChild(fileDiv);
        });
        
    } catch (error) {
        console.error('Error loading file list:', error);
    }
}

// Загружаем список файлов при старте
document.addEventListener('DOMContentLoaded', loadUploadedFiles);

// Drag and Drop
const uploadArea = document.querySelector('.upload-area');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    uploadArea.addEventListener(eventName, () => {
        uploadArea.style.background = '#e3f2fd';
        uploadArea.style.borderColor = '#2196f3';
    });
});

['dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, () => {
        uploadArea.style.background = '#f8f9fa';
        uploadArea.style.borderColor = '#007bff';
    });
});

uploadArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    // Обновляем input файлов
    const dataTransfer = new DataTransfer();
    Array.from(files).forEach(file => dataTransfer.items.add(file));
    document.getElementById('fileInput').files = dataTransfer.files;
    
    // Триггерим событие change
    const event = new Event('change', { bubbles: true });
    document.getElementById('fileInput').dispatchEvent(event);
}