"""
Download Sample Images for Testing
Downloads royalty-free sample images from the web
"""

import os
import urllib.request
import sys


def download_sample_images():
    """
    Download sample images for testing edge detection.
    Uses placeholder.com for demo images.
    """
    print("\n" + "=" * 60)
    print("SAMPLE IMAGE DOWNLOADER")
    print("=" * 60)
    print("\nThis script will download sample images for testing.")
    print("Note: You can also add your own images to the 'input' folder.")
    print()
    
    # Create input folder if it doesn't exist
    os.makedirs('input', exist_ok=True)
    
    # Sample image URLs (using free, no-attribution required sources)
    sample_images = [
        {
            'url': 'https://via.placeholder.com/600x400.png/09f/fff?text=Sample+Image+1',
            'filename': 'input/sample1.png',
            'description': 'Simple geometric shapes'
        },
        {
            'url': 'https://via.placeholder.com/600x400.png/0099ff/ffffff?text=Edge+Detection+Test',
            'filename': 'input/sample2.png',
            'description': 'Text-based image'
        },
        {
            'url': 'https://via.placeholder.com/600x400.png/ff6b6b/ffffff?text=Test+Image',
            'filename': 'input/sample3.png',
            'description': 'High contrast image'
        }
    ]
    
    print("Downloading sample images...\n")
    
    successful = 0
    failed = 0
    
    for i, img in enumerate(sample_images, 1):
        try:
            print(f"[{i}/{len(sample_images)}] Downloading: {img['description']}")
            print(f"    URL: {img['url']}")
            print(f"    Saving to: {img['filename']}")
            
            # Download image
            urllib.request.urlretrieve(img['url'], img['filename'])
            
            # Check if file was created
            if os.path.exists(img['filename']):
                file_size = os.path.getsize(img['filename'])
                print(f"    ✓ Downloaded ({file_size} bytes)\n")
                successful += 1
            else:
                print(f"    ❌ Failed to save file\n")
                failed += 1
                
        except Exception as e:
            print(f"    ❌ Error: {str(e)}\n")
            failed += 1
    
    # Summary
    print("=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"✓ Successful: {successful}")
    if failed > 0:
        print(f"❌ Failed: {failed}")
    
    if successful > 0:
        print(f"\nImages saved to 'input' folder.")
        print("\nNext steps:")
        print("1. Run edge detection on a single image:")
        print("   python edge_detection.py input/sample1.png")
        print("\n2. Or process all images at once:")
        print("   python batch_process.py")
    
    print("=" * 60 + "\n")
    
    # Alternative suggestion
    print("💡 TIP: For better results, add your own photos to the 'input' folder!")
    print("   Supported formats: .jpg, .jpeg, .png, .bmp, .gif, .tiff\n")


def main():
    """
    Main function.
    """
    try:
        download_sample_images()
    except KeyboardInterrupt:
        print("\n\n✓ Download interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
