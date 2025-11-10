"""
Quick Edge Detection Runner - Saves results without GUI display
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

from edge_detection import EdgeDetector
import sys
import os

def main():
    image_path = 'input/test_image.jpg'
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"[ERROR] Image not found: {image_path}")
        sys.exit(1)
    
    print("Starting edge detection...")
    print(f"Input: {image_path}")
    
    # Create detector
    detector = EdgeDetector(image_path)
    
    # Run pipeline without display
    detector.process_complete_pipeline(save_output=True, display=False)
    
    print("\n" + "=" * 60)
    print("SUCCESS! Edge detection completed.")
    print(f"Results saved in: output/")
    print("=" * 60)

if __name__ == "__main__":
    main()
