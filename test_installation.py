"""
Test Installation Script
Verify that all dependencies are correctly installed
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        os.system('chcp 65001 > nul')
    except:
        pass


def test_imports():
    """
    Test if all required packages can be imported.
    """
    print("\n" + "=" * 60)
    print("TESTING INSTALLATION")
    print("=" * 60 + "\n")
    
    packages = {
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'matplotlib.pyplot': 'Matplotlib'
    }
    
    all_ok = True
    
    for package, name in packages.items():
        try:
            print(f"Testing {name}...", end=" ")
            __import__(package)
            
            # Get version if available
            try:
                if package == 'cv2':
                    import cv2
                    version = cv2.__version__
                elif package == 'numpy':
                    import numpy
                    version = numpy.__version__
                elif package == 'matplotlib.pyplot':
                    import matplotlib
                    version = matplotlib.__version__
                else:
                    version = "unknown"
                
                print(f"[OK] (version {version})")
            except:
                print("[OK]")
                
        except ImportError as e:
            print("[FAILED]")
            print(f"   Error: {str(e)}")
            all_ok = False
    
    print("\n" + "=" * 60)
    
    if all_ok:
        print("[PASS] ALL TESTS PASSED")
        print("=" * 60)
        print("\nInstallation is complete and working!")
        print("\nNext steps:")
        print("1. Download sample images: python download_sample_images.py")
        print("2. Run edge detection: python edge_detection.py input/sample1.png")
        print("3. Try examples: python examples.py")
        print("=" * 60 + "\n")
        return True
    else:
        print("[FAIL] SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease install missing packages:")
        print("  pip install -r requirements.txt")
        print("\nOr install manually:")
        print("  pip install opencv-python numpy matplotlib")
        print("=" * 60 + "\n")
        return False


def test_opencv_functionality():
    """
    Test basic OpenCV functionality.
    """
    try:
        import cv2
        import numpy as np
        
        print("Testing OpenCV functionality...")
        
        # Create a simple test image
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        test_image[25:75, 25:75] = [255, 255, 255]  # White square
        
        # Test grayscale conversion
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        
        # Test edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        print("[OK] OpenCV functionality test passed")
        return True
        
    except Exception as e:
        print(f"[FAIL] OpenCV functionality test failed: {str(e)}")
        return False


def main():
    """
    Main test function.
    """
    try:
        # Test imports
        if not test_imports():
            sys.exit(1)
        
        # Test OpenCV functionality
        print("\nRunning functionality tests...\n")
        if not test_opencv_functionality():
            sys.exit(1)
        
        print("\n[SUCCESS] All tests passed! System is ready to use.\n")
        
    except KeyboardInterrupt:
        print("\n\n[INFO] Test interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
