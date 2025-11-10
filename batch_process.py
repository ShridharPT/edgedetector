"""
Batch Processing Script for Edge Detection
Process multiple images at once
"""

import os
import sys
from pathlib import Path
from edge_detection import EdgeDetector


def batch_process_images(input_folder='input', output_folder='output', display=False):
    """
    Process all images in a folder.
    
    Args:
        input_folder (str): Folder containing input images
        output_folder (str): Folder to save processed images
        display (bool): Whether to display results for each image
    """
    # Check if input folder exists
    if not os.path.exists(input_folder):
        print(f"❌ Error: Input folder '{input_folder}' not found")
        return
    
    # Get all image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
    image_files = [f for f in os.listdir(input_folder) 
                   if f.lower().endswith(image_extensions)]
    
    if not image_files:
        print(f"❌ No image files found in '{input_folder}'")
        print(f"   Supported formats: {', '.join(image_extensions)}")
        return
    
    print("\n" + "=" * 70)
    print("BATCH EDGE DETECTION PROCESSING")
    print("=" * 70)
    print(f"\nFound {len(image_files)} image(s) to process:")
    for i, img in enumerate(image_files, 1):
        print(f"  {i}. {img}")
    print()
    
    # Process each image
    successful = 0
    failed = 0
    
    for i, image_file in enumerate(image_files, 1):
        image_path = os.path.join(input_folder, image_file)
        
        print(f"\n[{i}/{len(image_files)}] Processing: {image_file}")
        print("-" * 70)
        
        try:
            # Create detector
            detector = EdgeDetector(image_path)
            
            # Process
            detector.preprocess()
            detector.apply_sobel()
            detector.apply_laplacian()
            detector.apply_canny()
            
            # Save results
            detector.save_results(output_dir=output_folder)
            
            # Display if requested
            if display:
                detector.display_results()
            
            print(f"✓ Successfully processed: {image_file}")
            successful += 1
            
        except Exception as e:
            print(f"❌ Failed to process {image_file}: {str(e)}")
            failed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 70)
    print(f"Total images: {len(image_files)}")
    print(f"✓ Successful: {successful}")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    print(f"\nAll results saved to: {output_folder}/")
    print("=" * 70 + "\n")


def main():
    """
    Main function for batch processing.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Batch process images for edge detection'
    )
    parser.add_argument(
        '--input',
        default='input',
        help='Input folder containing images (default: input)'
    )
    parser.add_argument(
        '--output',
        default='output',
        help='Output folder for processed images (default: output)'
    )
    parser.add_argument(
        '--display',
        action='store_true',
        help='Display results for each image (default: False)'
    )
    
    args = parser.parse_args()
    
    try:
        batch_process_images(
            input_folder=args.input,
            output_folder=args.output,
            display=args.display
        )
    except KeyboardInterrupt:
        print("\n\n✓ Batch processing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
