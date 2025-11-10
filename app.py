"""
Flask Web Application for Edge Detection
REST API with web interface
"""

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import base64
import io
from typing import Dict, Any, Tuple, Optional
import cv2
import numpy as np
from pathlib import Path

from edge_detection import EdgeDetector
from config_manager import ConfigManager
from logger import setup_logger

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup
config = ConfigManager()
logger = setup_logger('web_app')

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
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def image_to_base64(image: np.ndarray) -> str:
    """Convert numpy image to base64 string."""
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')


@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Edge Detection API',
        'version': '1.0.0'
    })


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
        logger.debug(f"Parameters - Sobel: {sobel_kernel}, Laplacian: {laplacian_kernel}, Canny: ({canny_t1}, {canny_t2})")
        
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
        
        # Cleanup
        os.remove(filepath)
        
        logger.info(f"Successfully processed image: {filename}")
        
        return jsonify({
            'success': True,
            'message': 'Edge detection completed',
            'results': results,
            'filename': filename
        })
    
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/algorithms', methods=['GET'])
def get_algorithms():
    """Get available edge detection algorithms."""
    return jsonify({
        'algorithms': [
            {
                'name': 'Sobel',
                'description': 'Gradient-based edge detection in X and Y directions',
                'parameters': ['kernel_size']
            },
            {
                'name': 'Laplacian',
                'description': 'Second derivative edge detection',
                'parameters': ['kernel_size']
            },
            {
                'name': 'Canny',
                'description': 'Multi-stage optimal edge detection',
                'parameters': ['threshold1', 'threshold2']
            }
        ]
    })


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
    
    logger.info(f"Starting Edge Detection API server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
