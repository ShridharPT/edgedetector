"""
Edge Detection Examples
Demonstrates various use cases and parameter configurations
"""

from edge_detection import EdgeDetector
import os


def example_basic():
    """
    Example 1: Basic edge detection with default parameters
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Edge Detection")
    print("=" * 60)
    
    # Check if sample image exists
    if not os.path.exists('input/sample1.png'):
        print("Please run download_sample_images.py first to get sample images!")
        return
    
    # Create detector and run complete pipeline
    detector = EdgeDetector('input/sample1.png')
    detector.process_complete_pipeline(save_output=True, display=True)


def example_custom_parameters():
    """
    Example 2: Custom parameters for specific use cases
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Custom Parameters for Fine-Tuning")
    print("=" * 60)
    
    if not os.path.exists('input/sample1.png'):
        print("Please run download_sample_images.py first!")
        return
    
    detector = EdgeDetector('input/sample1.png')
    
    # Aggressive noise reduction (more blur)
    print("\n→ Using aggressive noise reduction...")
    detector.preprocess(blur_kernel_size=(9, 9), sigma=2.0)
    
    # Larger Sobel kernel for smoother edges
    print("→ Using larger Sobel kernel...")
    detector.apply_sobel(kernel_size=5)
    
    # Larger Laplacian kernel
    print("→ Using larger Laplacian kernel...")
    detector.apply_laplacian(kernel_size=5)
    
    # More sensitive Canny detection (lower thresholds)
    print("→ Using sensitive Canny detection...")
    detector.apply_canny(threshold1=30, threshold2=100)
    
    detector.display_results()
    detector.save_results(output_dir='output/custom_params')


def example_high_contrast():
    """
    Example 3: Optimized for high-contrast images
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: High-Contrast Image Optimization")
    print("=" * 60)
    
    if not os.path.exists('input/sample1.png'):
        print("Please run download_sample_images.py first!")
        return
    
    detector = EdgeDetector('input/sample1.png')
    
    # Minimal blur for high-contrast images
    detector.preprocess(blur_kernel_size=(3, 3), sigma=0.8)
    
    # Standard Sobel
    detector.apply_sobel(kernel_size=3)
    
    # Standard Laplacian
    detector.apply_laplacian(kernel_size=3)
    
    # Aggressive Canny thresholds for clear edges
    detector.apply_canny(threshold1=100, threshold2=200)
    
    detector.display_results()
    detector.save_results(output_dir='output/high_contrast')


def example_noisy_image():
    """
    Example 4: Optimized for noisy images
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Noisy Image Optimization")
    print("=" * 60)
    
    if not os.path.exists('input/sample1.png'):
        print("Please run download_sample_images.py first!")
        return
    
    detector = EdgeDetector('input/sample1.png')
    
    # Heavy blur for noise reduction
    detector.preprocess(blur_kernel_size=(11, 11), sigma=3.0)
    
    # Larger kernels to smooth out noise
    detector.apply_sobel(kernel_size=7)
    detector.apply_laplacian(kernel_size=5)
    
    # Conservative Canny thresholds
    detector.apply_canny(threshold1=60, threshold2=180)
    
    detector.display_results()
    detector.save_results(output_dir='output/noisy_image')


def example_comparison():
    """
    Example 5: Compare different Canny thresholds
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Canny Threshold Comparison")
    print("=" * 60)
    
    if not os.path.exists('input/sample1.png'):
        print("Please run download_sample_images.py first!")
        return
    
    import matplotlib.pyplot as plt
    import cv2
    
    detector = EdgeDetector('input/sample1.png')
    detector.preprocess()
    
    # Test different threshold combinations
    threshold_configs = [
        (30, 90, "Low Thresholds (Sensitive)"),
        (50, 150, "Default Thresholds"),
        (100, 200, "High Thresholds (Selective)"),
        (150, 250, "Very High Thresholds")
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Canny Edge Detection - Threshold Comparison', 
                 fontsize=14, fontweight='bold')
    
    for idx, (t1, t2, title) in enumerate(threshold_configs):
        row = idx // 2
        col = idx % 2
        
        # Apply Canny with specific thresholds
        canny = cv2.Canny(detector.blurred_image, t1, t2)
        
        # Display
        axes[row, col].imshow(canny, cmap='gray')
        axes[row, col].set_title(f'{title}\n({t1}, {t2})', fontweight='bold')
        axes[row, col].axis('off')
    
    plt.tight_layout()
    plt.show()


def example_step_by_step():
    """
    Example 6: Step-by-step processing with intermediate results
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Step-by-Step Processing")
    print("=" * 60)
    
    if not os.path.exists('input/sample1.png'):
        print("Please run download_sample_images.py first!")
        return
    
    import matplotlib.pyplot as plt
    
    detector = EdgeDetector('input/sample1.png')
    
    # Step 1: Show original
    print("\nStep 1: Original Image")
    
    # Step 2: Grayscale conversion
    print("Step 2: Converting to Grayscale")
    detector.preprocess(blur_kernel_size=(5, 5), sigma=1.4)
    
    # Step 3: Edge detection
    print("Step 3: Applying Edge Detection Algorithms")
    detector.apply_sobel()
    detector.apply_laplacian()
    detector.apply_canny()
    
    # Show preprocessing steps
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Preprocessing Pipeline', fontsize=14, fontweight='bold')
    
    axes[0].imshow(detector.original_rgb)
    axes[0].set_title('1. Original Image', fontweight='bold')
    axes[0].axis('off')
    
    axes[1].imshow(detector.gray_image, cmap='gray')
    axes[1].set_title('2. Grayscale Conversion', fontweight='bold')
    axes[1].axis('off')
    
    axes[2].imshow(detector.blurred_image, cmap='gray')
    axes[2].set_title('3. Gaussian Blur (Noise Reduction)', fontweight='bold')
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Show edge detection results
    detector.display_results()


def print_menu():
    """
    Print the examples menu
    """
    print("\n" + "=" * 60)
    print("EDGE DETECTION EXAMPLES")
    print("=" * 60)
    print("\nAvailable Examples:")
    print("  1. Basic Edge Detection (Default Settings)")
    print("  2. Custom Parameters (Fine-Tuning)")
    print("  3. High-Contrast Image Optimization")
    print("  4. Noisy Image Optimization")
    print("  5. Canny Threshold Comparison")
    print("  6. Step-by-Step Processing Pipeline")
    print("  0. Run All Examples")
    print("  Q. Quit")
    print("=" * 60)


def main():
    """
    Main function with interactive menu
    """
    examples = {
        '1': example_basic,
        '2': example_custom_parameters,
        '3': example_high_contrast,
        '4': example_noisy_image,
        '5': example_comparison,
        '6': example_step_by_step
    }
    
    # Check if input folder has images
    if not os.path.exists('input'):
        print("\n❌ 'input' folder not found!")
        print("Please run: python download_sample_images.py")
        return
    
    input_files = [f for f in os.listdir('input') 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
    if not input_files:
        print("\n❌ No images found in 'input' folder!")
        print("Please run: python download_sample_images.py")
        return
    
    while True:
        print_menu()
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print("\n✓ Exiting examples...")
            break
        elif choice == '0':
            print("\n→ Running all examples...")
            for example_func in examples.values():
                try:
                    example_func()
                except KeyboardInterrupt:
                    print("\n✓ Examples interrupted")
                    break
                except Exception as e:
                    print(f"❌ Error in example: {str(e)}")
                    continue
        elif choice in examples:
            try:
                examples[choice]()
            except KeyboardInterrupt:
                print("\n✓ Example interrupted")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ Invalid choice! Please try again.")
    
    print("\n" + "=" * 60)
    print("Thank you for exploring edge detection!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Exiting...")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
