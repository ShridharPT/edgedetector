"""
Unit tests for edge detection module
"""

import pytest
import numpy as np
import cv2
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from edge_detection import EdgeDetector


@pytest.fixture
def test_image_path(tmp_path):
    """Create a test image."""
    image = np.ones((100, 100, 3), dtype=np.uint8) * 255
    cv2.rectangle(image, (25, 25), (75, 75), (0, 0, 0), -1)
    image_path = tmp_path / "test_image.jpg"
    cv2.imwrite(str(image_path), image)
    return str(image_path)


class TestEdgeDetector:
    """Test cases for EdgeDetector class."""
    
    def test_initialization(self, test_image_path):
        """Test EdgeDetector initialization."""
        detector = EdgeDetector(test_image_path)
        assert detector.image_path == test_image_path
        assert detector.original_image is not None
        assert detector.original_rgb is not None
    
    def test_invalid_image_path(self):
        """Test with invalid image path."""
        with pytest.raises(ValueError):
            EdgeDetector("nonexistent.jpg")
    
    def test_preprocessing(self, test_image_path):
        """Test image preprocessing."""
        detector = EdgeDetector(test_image_path)
        detector.preprocess()
        
        assert detector.gray_image is not None
        assert detector.blurred_image is not None
        assert len(detector.gray_image.shape) == 2  # Grayscale
    
    def test_sobel_detection(self, test_image_path):
        """Test Sobel edge detection."""
        detector = EdgeDetector(test_image_path)
        detector.preprocess()
        detector.apply_sobel()
        
        assert detector.sobel_x is not None
        assert detector.sobel_y is not None
        assert detector.sobel_combined is not None
    
    def test_laplacian_detection(self, test_image_path):
        """Test Laplacian edge detection."""
        detector = EdgeDetector(test_image_path)
        detector.preprocess()
        detector.apply_laplacian()
        
        assert detector.laplacian is not None
    
    def test_canny_detection(self, test_image_path):
        """Test Canny edge detection."""
        detector = EdgeDetector(test_image_path)
        detector.preprocess()
        detector.apply_canny()
        
        assert detector.canny is not None
    
    def test_custom_parameters(self, test_image_path):
        """Test custom parameter configuration."""
        detector = EdgeDetector(test_image_path)
        detector.preprocess(blur_kernel_size=(7, 7), sigma=2.0)
        detector.apply_sobel(kernel_size=5)
        detector.apply_laplacian(kernel_size=5)
        detector.apply_canny(threshold1=100, threshold2=200)
        
        assert detector.sobel_x is not None
        assert detector.laplacian is not None
        assert detector.canny is not None
    
    def test_save_results(self, test_image_path, tmp_path):
        """Test saving results."""
        detector = EdgeDetector(test_image_path)
        detector.preprocess()
        detector.apply_sobel()
        detector.apply_laplacian()
        detector.apply_canny()
        
        output_dir = str(tmp_path / "output")
        detector.save_results(output_dir=output_dir)
        
        # Check if files were created
        assert os.path.exists(f"{output_dir}/test_image_grayscale.jpg")
        assert os.path.exists(f"{output_dir}/test_image_sobel_x.jpg")
        assert os.path.exists(f"{output_dir}/test_image_canny.jpg")
    
    def test_complete_pipeline(self, test_image_path, tmp_path):
        """Test complete processing pipeline."""
        detector = EdgeDetector(test_image_path)
        output_dir = str(tmp_path / "output")
        
        # Run without display
        detector.process_complete_pipeline(save_output=True, display=False)
        
        # Verify all results exist
        assert detector.gray_image is not None
        assert detector.blurred_image is not None
        assert detector.sobel_combined is not None
        assert detector.laplacian is not None
        assert detector.canny is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
