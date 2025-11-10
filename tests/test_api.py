"""
Unit tests for Flask API
"""

import pytest
import io
import sys
from pathlib import Path
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_image():
    """Create test image bytes."""
    image = np.ones((100, 100, 3), dtype=np.uint8) * 255
    cv2.rectangle(image, (25, 25), (75, 75), (0, 0, 0), -1)
    _, buffer = cv2.imencode('.jpg', image)
    return io.BytesIO(buffer)


class TestAPI:
    """Test cases for Flask API."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_index_page(self, client):
        """Test index page loads."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_get_algorithms(self, client):
        """Test algorithms endpoint."""
        response = client.get('/api/algorithms')
        assert response.status_code == 200
        data = response.get_json()
        assert 'algorithms' in data
        assert len(data['algorithms']) == 3
    
    def test_detect_no_file(self, client):
        """Test detection without file."""
        response = client.post('/api/detect')
        assert response.status_code == 400
    
    def test_detect_with_image(self, client, test_image):
        """Test detection with valid image."""
        data = {
            'image': (test_image, 'test.jpg'),
            'sobel_kernel': '3',
            'laplacian_kernel': '3',
            'canny_threshold1': '50',
            'canny_threshold2': '150',
            'blur_kernel': '5'
        }
        
        response = client.post(
            '/api/detect',
            data=data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] == True
        assert 'results' in json_data
        assert 'canny' in json_data['results']
    
    def test_invalid_file_type(self, client):
        """Test with invalid file type."""
        data = {
            'image': (io.BytesIO(b'test'), 'test.txt')
        }
        
        response = client.post(
            '/api/detect',
            data=data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
