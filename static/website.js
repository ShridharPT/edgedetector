// Tab switching
function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
    
    if (tabName === 'info') {
        loadSystemInfo();
    }
}

// File inputs
const imageInput = document.getElementById('imageInput');
const batchInput = document.getElementById('batchInput');
const compareInput = document.getElementById('compareInput');
const analyzeInput = document.getElementById('analyzeInput');

let selectedFile = null;
let selectedFiles = [];
let compareFile = null;
let analyzeFile = null;

imageInput.addEventListener('change', (e) => handleFileSelect(e.target.files[0], 'single'));
batchInput.addEventListener('change', (e) => handleBatchSelect(e.target.files));
compareInput.addEventListener('change', (e) => handleFileSelect(e.target.files[0], 'compare'));
analyzeInput.addEventListener('change', (e) => handleFileSelect(e.target.files[0], 'analyze'));

// Drag and drop
setupDragDrop('dropZone', 'single');
setupDragDrop('batchDropZone', 'batch');
setupDragDrop('compareDropZone', 'compare');
setupDragDrop('analyzeDropZone', 'analyze');

function setupDragDrop(zoneId, type) {
    const zone = document.getElementById(zoneId);
    
    zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.classList.add('dragover');
    });
    
    zone.addEventListener('dragleave', () => {
        zone.classList.remove('dragover');
    });
    
    zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.classList.remove('dragover');
        
        if (type === 'batch') {
            handleBatchSelect(e.dataTransfer.files);
        } else {
            handleFileSelect(e.dataTransfer.files[0], type);
        }
    });
}

function handleFileSelect(file, type) {
    if (!file || !file.type.startsWith('image/')) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        if (type === 'single') {
            selectedFile = file;
            document.getElementById('processBtn').disabled = false;
            document.getElementById('preview').innerHTML = `
                <img src="${e.target.result}" style="max-width: 300px; max-height: 200px; border-radius: 10px;">
                <p style="margin-top: 10px; color: var(--primary); font-weight: bold;">✓ ${file.name}</p>
            `;
        } else if (type === 'compare') {
            compareFile = file;
            document.getElementById('compareBtn').disabled = false;
        } else if (type === 'analyze') {
            analyzeFile = file;
            document.getElementById('analyzeBtn').disabled = false;
        }
    };
    reader.readAsDataURL(file);
}

function handleBatchSelect(files) {
    selectedFiles = Array.from(files).filter(f => f.type.startsWith('image/'));
    document.getElementById('batchProcessBtn').disabled = selectedFiles.length === 0;
}

// Process single image
document.getElementById('processBtn').addEventListener('click', async () => {
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('blur_kernel', document.getElementById('blurKernel').value);
    formData.append('sobel_kernel', document.getElementById('sobelKernel').value);
    formData.append('laplacian_kernel', document.getElementById('laplacianKernel').value);
    formData.append('canny_threshold1', document.getElementById('cannyT1').value);
    formData.append('canny_threshold2', document.getElementById('cannyT2').value);
    
    showLoading('single');
    
    try {
        const response = await fetch('/api/detect', { method: 'POST', body: formData });
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.results, 'single');
        } else {
            showError('single', data.error);
        }
    } catch (err) {
        showError('single', err.message);
    } finally {
        hideLoading('single');
    }
});

// Process batch
document.getElementById('batchProcessBtn').addEventListener('click', async () => {
    if (selectedFiles.length === 0) return;
    
    const formData = new FormData();
    selectedFiles.forEach(file => formData.append('images', file));
    
    showLoading('batch');
    
    try {
        const response = await fetch('/api/batch-detect', { method: 'POST', body: formData });
        const data = await response.json();
        
        if (data.success) {
            displayBatchResults(data.results);
        } else {
            showError('batch', data.error);
        }
    } catch (err) {
        showError('batch', err.message);
    } finally {
        hideLoading('batch');
    }
});

// Compare algorithms
document.getElementById('compareBtn').addEventListener('click', async () => {
    if (!compareFile) return;
    
    const formData = new FormData();
    formData.append('image', compareFile);
    
    showLoading('compare');
    
    try {
        const response = await fetch('/api/compare', { method: 'POST', body: formData });
        const data = await response.json();
        displayComparison(data);
    } catch (err) {
        showError('compare', err.message);
    } finally {
        hideLoading('compare');
    }
});

// Analyze image
document.getElementById('analyzeBtn').addEventListener('click', async () => {
    if (!analyzeFile) return;
    
    const formData = new FormData();
    formData.append('image', analyzeFile);
    
    showLoading('analyze');
    
    try {
        const response = await fetch('/api/analyze', { method: 'POST', body: formData });
        const data = await response.json();
        displayAnalysis(data);
    } catch (err) {
        showError('analyze', err.message);
    } finally {
        hideLoading('analyze');
    }
});

// Display functions
function displayResults(results, type) {
    const grid = document.getElementById(type + 'ResultsGrid');
    grid.innerHTML = '';
    
    const items = [
        { key: 'original', label: 'Original' },
        { key: 'grayscale', label: 'Grayscale' },
        { key: 'blurred', label: 'Blurred' },
        { key: 'sobel_x', label: 'Sobel X' },
        { key: 'sobel_y', label: 'Sobel Y' },
        { key: 'sobel_combined', label: 'Sobel Combined' },
        { key: 'laplacian', label: 'Laplacian' },
        { key: 'canny', label: 'Canny ⭐' }
    ];
    
    items.forEach(item => {
        if (results[item.key]) {
            const div = document.createElement('div');
            div.className = 'result-item';
            div.innerHTML = `
                <h3>${item.label}</h3>
                <img src="data:image/jpeg;base64,${results[item.key]}" alt="${item.label}">
            `;
            grid.appendChild(div);
        }
    });
    
    document.getElementById(type + 'Results').style.display = 'block';
}

function displayBatchResults(results) {
    const grid = document.getElementById('batchResultsGrid');
    grid.innerHTML = '';
    
    results.forEach(result => {
        if (result.status === 'success') {
            const div = document.createElement('div');
            div.className = 'result-item';
            div.innerHTML = `
                <h3>${result.filename}</h3>
                <img src="data:image/jpeg;base64,${result.canny}" alt="${result.filename}">
            `;
            grid.appendChild(div);
        }
    });
    
    document.getElementById('batchResults').style.display = 'block';
}

function displayComparison(data) {
    const grid = document.getElementById('compareResultsGrid');
    grid.innerHTML = '';
    
    const items = [
        { key: 'sobel_x', label: 'Sobel X' },
        { key: 'sobel_y', label: 'Sobel Y' },
        { key: 'sobel_combined', label: 'Sobel Combined' },
        { key: 'laplacian', label: 'Laplacian' },
        { key: 'canny', label: 'Canny' }
    ];
    
    items.forEach(item => {
        if (data.algorithms[item.key]) {
            const div = document.createElement('div');
            div.className = 'result-item';
            let src = data.algorithms[item.key];
            if (typeof src === 'object') src = src.combined || src.standard;
            
            div.innerHTML = `
                <h3>${item.label}</h3>
                <img src="data:image/jpeg;base64,${src}" alt="${item.label}">
            `;
            grid.appendChild(div);
        }
    });
    
    document.getElementById('compareResults').style.display = 'block';
}

function displayAnalysis(data) {
    const stats = document.getElementById('analyzeStats');
    stats.innerHTML = `
        <div class="card">
            <h3>📊 Image Properties</h3>
            <p><strong>Dimensions:</strong> ${data.dimensions.width}x${data.dimensions.height}</p>
            <p><strong>Mean Brightness:</strong> ${data.statistics.mean_brightness.toFixed(2)}</p>
            <p><strong>Std Deviation:</strong> ${data.statistics.std_brightness.toFixed(2)}</p>
            <p><strong>Contrast:</strong> ${data.statistics.contrast.toFixed(2)}</p>
        </div>
    `;
    document.getElementById('analyzeResults').style.display = 'block';
}

function loadSystemInfo() {
    fetch('/api/info')
        .then(r => r.json())
        .then(data => {
            const info = document.getElementById('systemInfo');
            info.innerHTML = `
                <p><strong>Service:</strong> ${data.name}</p>
                <p><strong>Version:</strong> ${data.version}</p>
                <p><strong>Algorithms:</strong> ${data.features.algorithms.join(', ')}</p>
                <p><strong>Max Upload:</strong> ${data.features.max_size_mb} MB</p>
                <p><strong>Formats:</strong> ${data.features.formats.join(', ')}</p>
            `;
        });
}

// Utility functions
function showLoading(type) {
    document.getElementById(type + 'Loading').style.display = 'block';
}

function hideLoading(type) {
    document.getElementById(type + 'Loading').style.display = 'none';
}

function showError(type, msg) {
    const el = document.getElementById(type + 'Error');
    if (el) {
        el.textContent = msg;
        el.style.display = 'block';
    }
}
