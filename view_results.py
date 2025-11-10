"""
View Edge Detection Results
Display all processed images in a comparison grid
"""

import cv2
import matplotlib.pyplot as plt
import sys
import os

def view_results(base_name='test_image'):
    """
    View all edge detection results for a given image.
    """
    output_dir = 'output'
    
    # Check if files exist
    required_files = [
        f'{output_dir}/{base_name}_grayscale.jpg',
        f'{output_dir}/{base_name}_blurred.jpg',
        f'{output_dir}/{base_name}_sobel_x.jpg',
        f'{output_dir}/{base_name}_sobel_y.jpg',
        f'{output_dir}/{base_name}_sobel_combined.jpg',
        f'{output_dir}/{base_name}_laplacian.jpg',
        f'{output_dir}/{base_name}_canny.jpg'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"[ERROR] Missing result files:")
        for f in missing_files:
            print(f"  - {f}")
        print("\nPlease run edge detection first:")
        print(f"  python run_edge_detection_quick.py")
        return
    
    # Load images
    print("Loading results...")
    grayscale = cv2.imread(f'{output_dir}/{base_name}_grayscale.jpg', cv2.IMREAD_GRAYSCALE)
    blurred = cv2.imread(f'{output_dir}/{base_name}_blurred.jpg', cv2.IMREAD_GRAYSCALE)
    sobel_x = cv2.imread(f'{output_dir}/{base_name}_sobel_x.jpg', cv2.IMREAD_GRAYSCALE)
    sobel_y = cv2.imread(f'{output_dir}/{base_name}_sobel_y.jpg', cv2.IMREAD_GRAYSCALE)
    sobel_combined = cv2.imread(f'{output_dir}/{base_name}_sobel_combined.jpg', cv2.IMREAD_GRAYSCALE)
    laplacian = cv2.imread(f'{output_dir}/{base_name}_laplacian.jpg', cv2.IMREAD_GRAYSCALE)
    canny = cv2.imread(f'{output_dir}/{base_name}_canny.jpg', cv2.IMREAD_GRAYSCALE)
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    fig.suptitle(f'Edge Detection Results - {base_name}', fontsize=16, fontweight='bold')
    
    # Display images
    axes[0, 0].imshow(grayscale, cmap='gray')
    axes[0, 0].set_title('Grayscale', fontweight='bold')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(blurred, cmap='gray')
    axes[0, 1].set_title('Gaussian Blurred', fontweight='bold')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(sobel_x, cmap='gray')
    axes[0, 2].set_title('Sobel X (Vertical)', fontweight='bold')
    axes[0, 2].axis('off')
    
    axes[0, 3].imshow(sobel_y, cmap='gray')
    axes[0, 3].set_title('Sobel Y (Horizontal)', fontweight='bold')
    axes[0, 3].axis('off')
    
    axes[1, 0].imshow(sobel_combined, cmap='gray')
    axes[1, 0].set_title('Sobel Combined', fontweight='bold')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(laplacian, cmap='gray')
    axes[1, 1].set_title('Laplacian', fontweight='bold')
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(canny, cmap='gray')
    axes[1, 2].set_title('Canny (Best Quality)', fontweight='bold', color='green')
    axes[1, 2].axis('off')
    
    # Hide the last subplot
    axes[1, 3].axis('off')
    axes[1, 3].text(0.5, 0.5, 'Close window\nto continue', 
                    ha='center', va='center', fontsize=12,
                    transform=axes[1, 3].transAxes)
    
    plt.tight_layout()
    print("[OK] Displaying results window...")
    print("     Close the window to continue")
    plt.show()
    
    print("\n[OK] Results displayed successfully!")

def main():
    base_name = 'test_image'
    
    if len(sys.argv) > 1:
        base_name = sys.argv[1]
    
    print("\n" + "=" * 60)
    print("EDGE DETECTION RESULTS VIEWER")
    print("=" * 60)
    print(f"\nViewing results for: {base_name}")
    
    view_results(base_name)
    
    print("\n" + "=" * 60)
    print("All result files are saved in: output/")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Viewer closed by user")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
