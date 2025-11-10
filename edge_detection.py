"""
Edge Detection System using OpenCV
Implements Sobel, Laplacian, and Canny edge detection algorithms
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path


class EdgeDetector:
    """
    A class to perform various edge detection techniques on images.
    """
    
    def __init__(self, image_path):
        """
        Initialize the EdgeDetector with an input image.
        
        Args:
            image_path (str): Path to the input image
        """
        self.image_path = image_path
        self.original_image = cv2.imread(image_path)
        
        if self.original_image is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Convert to RGB for display (OpenCV loads as BGR)
        self.original_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        
        # Preprocessing
        self.gray_image = None
        self.blurred_image = None
        
        # Edge detection results
        self.sobel_x = None
        self.sobel_y = None
        self.sobel_combined = None
        self.laplacian = None
        self.canny = None
        
    def preprocess(self, blur_kernel_size=(5, 5), sigma=1.4):
        """
        Preprocess the image: convert to grayscale and apply Gaussian blur.
        
        Args:
            blur_kernel_size (tuple): Size of the Gaussian kernel
            sigma (float): Standard deviation for Gaussian kernel
        """
        print("Preprocessing image...")
        
        # Convert to grayscale
        self.gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        self.blurred_image = cv2.GaussianBlur(self.gray_image, blur_kernel_size, sigma)
        
        print("[OK] Image converted to grayscale")
        print(f"[OK] Gaussian blur applied (kernel: {blur_kernel_size}, sigma: {sigma})")
    
    def apply_sobel(self, kernel_size=3):
        """
        Apply Sobel edge detection in X and Y directions.
        
        Args:
            kernel_size (int): Size of the Sobel kernel (must be odd: 1, 3, 5, or 7)
        """
        print("\nApplying Sobel edge detection...")
        
        # Sobel in X direction (vertical edges)
        self.sobel_x = cv2.Sobel(self.blurred_image, cv2.CV_64F, 1, 0, ksize=kernel_size)
        self.sobel_x = np.absolute(self.sobel_x)
        self.sobel_x = np.uint8(self.sobel_x)
        
        # Sobel in Y direction (horizontal edges)
        self.sobel_y = cv2.Sobel(self.blurred_image, cv2.CV_64F, 0, 1, ksize=kernel_size)
        self.sobel_y = np.absolute(self.sobel_y)
        self.sobel_y = np.uint8(self.sobel_y)
        
        # Combine Sobel X and Y
        self.sobel_combined = cv2.addWeighted(self.sobel_x, 0.5, self.sobel_y, 0.5, 0)
        
        print(f"[OK] Sobel edge detection completed (kernel size: {kernel_size})")
    
    def apply_laplacian(self, kernel_size=3):
        """
        Apply Laplacian edge detection.
        
        Args:
            kernel_size (int): Size of the Laplacian kernel
        """
        print("\nApplying Laplacian edge detection...")
        
        self.laplacian = cv2.Laplacian(self.blurred_image, cv2.CV_64F, ksize=kernel_size)
        self.laplacian = np.absolute(self.laplacian)
        self.laplacian = np.uint8(self.laplacian)
        
        print(f"[OK] Laplacian edge detection completed (kernel size: {kernel_size})")
    
    def apply_canny(self, threshold1=50, threshold2=150):
        """
        Apply Canny edge detection.
        
        Args:
            threshold1 (int): Lower threshold for hysteresis
            threshold2 (int): Upper threshold for hysteresis
        """
        print("\nApplying Canny edge detection...")
        
        self.canny = cv2.Canny(self.blurred_image, threshold1, threshold2)
        
        print(f"[OK] Canny edge detection completed (thresholds: {threshold1}, {threshold2})")
    
    def display_results(self):
        """
        Display all edge detection results in a single figure.
        """
        print("\nDisplaying results...")
        
        fig, axes = plt.subplots(2, 4, figsize=(18, 10))
        fig.suptitle('Edge Detection Results Comparison', fontsize=16, fontweight='bold')
        
        # Original Image
        axes[0, 0].imshow(self.original_rgb)
        axes[0, 0].set_title('Original Image', fontweight='bold')
        axes[0, 0].axis('off')
        
        # Grayscale
        axes[0, 1].imshow(self.gray_image, cmap='gray')
        axes[0, 1].set_title('Grayscale', fontweight='bold')
        axes[0, 1].axis('off')
        
        # Blurred
        axes[0, 2].imshow(self.blurred_image, cmap='gray')
        axes[0, 2].set_title('Gaussian Blurred', fontweight='bold')
        axes[0, 2].axis('off')
        
        # Sobel X
        axes[0, 3].imshow(self.sobel_x, cmap='gray')
        axes[0, 3].set_title('Sobel X (Vertical Edges)', fontweight='bold')
        axes[0, 3].axis('off')
        
        # Sobel Y
        axes[1, 0].imshow(self.sobel_y, cmap='gray')
        axes[1, 0].set_title('Sobel Y (Horizontal Edges)', fontweight='bold')
        axes[1, 0].axis('off')
        
        # Sobel Combined
        axes[1, 1].imshow(self.sobel_combined, cmap='gray')
        axes[1, 1].set_title('Sobel Combined', fontweight='bold')
        axes[1, 1].axis('off')
        
        # Laplacian
        axes[1, 2].imshow(self.laplacian, cmap='gray')
        axes[1, 2].set_title('Laplacian', fontweight='bold')
        axes[1, 2].axis('off')
        
        # Canny
        axes[1, 3].imshow(self.canny, cmap='gray')
        axes[1, 3].set_title('Canny Edge Detection', fontweight='bold')
        axes[1, 3].axis('off')
        
        plt.tight_layout()
        plt.show()
        
        print("[OK] Results displayed successfully")
    
    def save_results(self, output_dir='output'):
        """
        Save all edge detection results to files.
        
        Args:
            output_dir (str): Directory to save output images
        """
        print(f"\nSaving results to '{output_dir}' directory...")
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        # Get base filename
        base_name = Path(self.image_path).stem
        
        # Save each result
        cv2.imwrite(f"{output_dir}/{base_name}_grayscale.jpg", self.gray_image)
        cv2.imwrite(f"{output_dir}/{base_name}_blurred.jpg", self.blurred_image)
        cv2.imwrite(f"{output_dir}/{base_name}_sobel_x.jpg", self.sobel_x)
        cv2.imwrite(f"{output_dir}/{base_name}_sobel_y.jpg", self.sobel_y)
        cv2.imwrite(f"{output_dir}/{base_name}_sobel_combined.jpg", self.sobel_combined)
        cv2.imwrite(f"{output_dir}/{base_name}_laplacian.jpg", self.laplacian)
        cv2.imwrite(f"{output_dir}/{base_name}_canny.jpg", self.canny)
        
        print("[OK] All results saved successfully:")
        print(f"  - {base_name}_grayscale.jpg")
        print(f"  - {base_name}_blurred.jpg")
        print(f"  - {base_name}_sobel_x.jpg")
        print(f"  - {base_name}_sobel_y.jpg")
        print(f"  - {base_name}_sobel_combined.jpg")
        print(f"  - {base_name}_laplacian.jpg")
        print(f"  - {base_name}_canny.jpg")
    
    def process_complete_pipeline(self, save_output=True, display=True):
        """
        Run the complete edge detection pipeline.
        
        Args:
            save_output (bool): Whether to save results to disk
            display (bool): Whether to display results
        """
        print("=" * 60)
        print("EDGE DETECTION PIPELINE")
        print("=" * 60)
        
        # Preprocessing
        self.preprocess()
        
        # Apply all edge detection methods
        self.apply_sobel()
        self.apply_laplacian()
        self.apply_canny()
        
        # Display results
        if display:
            self.display_results()
        
        # Save results
        if save_output:
            self.save_results()
        
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)


def main():
    """
    Main function to run the edge detection system.
    """
    import sys
    
    # Check if image path is provided
    if len(sys.argv) < 2:
        print("\n" + "=" * 60)
        print("Edge Detection System - Usage Instructions")
        print("=" * 60)
        print("\nUsage: python edge_detection.py <image_path>")
        print("\nExample:")
        print("  python edge_detection.py input/sample.jpg")
        print("\nNote: Place your images in the 'input' folder")
        print("=" * 60 + "\n")
        
        # Check if there are sample images in input folder
        if os.path.exists('input'):
            images = [f for f in os.listdir('input') 
                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
            if images:
                print(f"Found {len(images)} image(s) in 'input' folder:")
                for img in images:
                    print(f"  - {img}")
                print("\nTry running:")
                print(f"  python edge_detection.py input/{images[0]}")
                print()
        else:
            print("Tip: Create an 'input' folder and add some images to get started!")
            print()
        
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"\n[ERROR] Image file not found: {image_path}")
        print("Please provide a valid image path.\n")
        sys.exit(1)
    
    try:
        # Create EdgeDetector instance
        detector = EdgeDetector(image_path)
        
        # Run complete pipeline
        detector.process_complete_pipeline(save_output=True, display=True)
        
    except Exception as e:
        print(f"\n[ERROR] Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
