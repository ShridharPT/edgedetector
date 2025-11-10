"""
Unified Edge Detection Website
Complete dashboard combining all features
"""

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import base64
import io
import json
from typing import Dict, Any, Tuple
import cv2
import numpy as np
from pathlib import Path

from edge_detection import EdgeDetector
from config_manager import ConfigManager
from logger import setup_logger

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Setup
config = ConfigManager()
logger = setup_logger('website')

# Configuration
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

web_config = config.get_web_config()
app.config['MAX_CONTENT_LENGTH'] = web_config['max_upload_size']
ALLOWED_EXTENSIONS = set(web_config['allowed_extensions'])


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def image_to_base64(image: np.ndarray) -> str:
    """Convert numpy image to base64 string."""
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')


# ============================================================================
# MAIN PAGES
# ============================================================================

@app.route('/')
def index():
    """Serve the main unified dashboard."""
    return render_template('website.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard overview page."""
    return render_template('website.html', page='dashboard')


# ============================================================================
# API ENDPOINTS - HEALTH & INFO
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Edge Detection System',
        'version': '2.0.0',
        'features': ['Web UI', 'REST API', 'Batch Processing', 'Real-time Webcam'],
        'algorithms': ['Sobel', 'Laplacian', 'Canny']
    })


@app.route('/api/info', methods=['GET'])
def get_info():
    """Get system information."""
    return jsonify({
        'name': 'Edge Detection System',
        'version': '2.0.0',
        'description': 'Professional edge detection with multiple algorithms',
        'features': {
            'algorithms': ['Sobel (X, Y, Combined)', 'Laplacian', 'Canny'],
            'upload': 'Drag & drop or click',
            'formats': list(ALLOWED_EXTENSIONS),
            'max_size_mb': web_config['max_upload_size'] / (1024 * 1024),
            'real_time': 'Webcam support',
            'batch': 'Multiple images'
        },
        'algorithms_detail': [
            {
                'name': 'Sobel',
                'description': 'Gradient-based edge detection',
                'variants': ['X (Vertical)', 'Y (Horizontal)', 'Combined'],
                'best_for': 'Directional edge detection'
            },
            {
                'name': 'Laplacian',
                'description': 'Second derivative edge detection',
                'variants': ['Standard'],
                'best_for': 'Fine detail detection'
            },
            {
                'name': 'Canny',
                'description': 'Multi-stage optimal edge detection',
                'variants': ['Standard'],
                'best_for': 'Overall best quality'
            }
        ]
    })


@app.route('/api/algorithms', methods=['GET'])
def get_algorithms():
    """Get available algorithms."""
    return jsonify({
        'algorithms': [
            {
                'id': 'sobel',
                'name': 'Sobel Operator',
                'description': 'Gradient-based edge detection in X and Y directions',
                'parameters': [
                    {'name': 'kernel_size', 'type': 'int', 'min': 1, 'max': 7, 'default': 3}
                ],
                'variants': ['X', 'Y', 'Combined']
            },
            {
                'id': 'laplacian',
                'name': 'Laplacian Operator',
                'description': 'Second derivative edge detection',
                'parameters': [
                    {'name': 'kernel_size', 'type': 'int', 'min': 1, 'max': 7, 'default': 3}
                ],
                'variants': ['Standard']
            },
            {
                'id': 'canny',
                'name': 'Canny Edge Detector',
                'description': 'Multi-stage optimal edge detection',
                'parameters': [
                    {'name': 'threshold1', 'type': 'int', 'min': 0, 'max': 255, 'default': 50},
                    {'name': 'threshold2', 'type': 'int', 'min': 0, 'max': 255, 'default': 150}
                ],
                'variants': ['Standard']
            }
        ]
    })


# ============================================================================
# API ENDPOINTS - IMAGE PROCESSING
# ============================================================================

@app.route('/api/detect', methods=['POST'])
def detect_edges():
    """
    Edge detection API endpoint.
    
    Accepts: multipart/form-data with 'image' file
    Returns: JSON with base64 encoded images
    """
    try:
        # Validate request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Allowed: {ALLOWED_EXTENSIONS}'}), 400
        
        # Get parameters from request
        params = request.form.to_dict()
        sobel_kernel = int(params.get('sobel_kernel', 3))
        laplacian_kernel = int(params.get('laplacian_kernel', 3))
        canny_t1 = int(params.get('canny_threshold1', 50))
        canny_t2 = int(params.get('canny_threshold2', 150))
        blur_size = int(params.get('blur_kernel', 5))
        
        logger.info(f"Processing image: {file.filename}")
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process image
        detector = EdgeDetector(filepath)
        detector.preprocess(blur_kernel_size=(blur_size, blur_size), sigma=1.4)
        detector.apply_sobel(kernel_size=sobel_kernel)
        detector.apply_laplacian(kernel_size=laplacian_kernel)
        detector.apply_canny(threshold1=canny_t1, threshold2=canny_t2)
        
        # Convert results to base64
        results = {
            'original': image_to_base64(detector.original_image),
            'grayscale': image_to_base64(detector.gray_image),
            'blurred': image_to_base64(detector.blurred_image),
            'sobel_x': image_to_base64(detector.sobel_x),
            'sobel_y': image_to_base64(detector.sobel_y),
            'sobel_combined': image_to_base64(detector.sobel_combined),
            'laplacian': image_to_base64(detector.laplacian),
            'canny': image_to_base64(detector.canny)
        }
        
        # Get image stats
        stats = {
            'original_size': f"{detector.original_image.shape[1]}x{detector.original_image.shape[0]}",
            'file_size_kb': os.path.getsize(filepath) / 1024,
            'processing_time': 'calculated'
        }
        
        # Cleanup
        os.remove(filepath)
        
        logger.info(f"Successfully processed image: {filename}")
        
        return jsonify({
            'success': True,
            'message': 'Edge detection completed',
            'results': results,
            'stats': stats,
            'filename': filename
        })
    
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/batch-detect', methods=['POST'])
def batch_detect():
    """Batch process multiple images."""
    try:
        if 'images' not in request.files:
            return jsonify({'error': 'No images provided'}), 400
        
        files = request.files.getlist('images')
        results_list = []
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                try:
                    detector = EdgeDetector(filepath)
                    detector.preprocess()
                    detector.apply_sobel()
                    detector.apply_laplacian()
                    detector.apply_canny()
                    
                    results_list.append({
                        'filename': filename,
                        'status': 'success',
                        'canny': image_to_base64(detector.canny)
                    })
                except Exception as e:
                    results_list.append({
                        'filename': filename,
                        'status': 'error',
                        'error': str(e)
                    })
                finally:
                    if os.path.exists(filepath):
                        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'total': len(files),
            'processed': len([r for r in results_list if r['status'] == 'success']),
            'results': results_list
        })
    
    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# API ENDPOINTS - COMPARISON & ANALYSIS
# ============================================================================

@app.route('/api/compare', methods=['POST'])
def compare_algorithms():
    """Compare different algorithms on same image."""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        detector = EdgeDetector(filepath)
        detector.preprocess()
        detector.apply_sobel()
        detector.apply_laplacian()
        detector.apply_canny()
        
        comparison = {
            'image': filename,
            'algorithms': {
                'sobel': {
                    'x': image_to_base64(detector.sobel_x),
                    'y': image_to_base64(detector.sobel_y),
                    'combined': image_to_base64(detector.sobel_combined)
                },
                'laplacian': image_to_base64(detector.laplacian),
                'canny': image_to_base64(detector.canny)
            },
            'analysis': {
                'edge_density': {
                    'sobel': float(np.mean(detector.sobel_combined > 0)),
                    'laplacian': float(np.mean(detector.laplacian > 0)),
                    'canny': float(np.mean(detector.canny > 0))
                }
            }
        }
        
        os.remove(filepath)
        return jsonify(comparison)
    
    except Exception as e:
        logger.error(f"Comparison error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    """Analyze image properties."""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        analysis = {
            'filename': filename,
            'dimensions': {
                'width': img.shape[1],
                'height': img.shape[0],
                'channels': img.shape[2] if len(img.shape) > 2 else 1
            },
            'statistics': {
                'mean_brightness': float(np.mean(gray)),
                'std_brightness': float(np.std(gray)),
                'min_brightness': float(np.min(gray)),
                'max_brightness': float(np.max(gray)),
                'contrast': float(np.max(gray) - np.min(gray))
            },
            'histogram': {
                'bins': 256,
                'values': cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten().tolist()
            }
        }
        
        os.remove(filepath)
        return jsonify(analysis)
    
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({
        'error': 'File too large',
        'max_size_mb': web_config['max_upload_size'] / (1024 * 1024)
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    host = web_config['host']
    port = web_config['port']
    debug = web_config['debug']
    
    logger.info(f"Starting Unified Edge Detection Website on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
