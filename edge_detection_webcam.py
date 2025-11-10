"""
Real-Time Edge Detection on Webcam Feed
Implements live edge detection with multiple algorithms
"""

import cv2
import numpy as np


class WebcamEdgeDetector:
    """
    Real-time edge detection on webcam feed.
    """
    
    def __init__(self, camera_index=0):
        """
        Initialize webcam edge detector.
        
        Args:
            camera_index (int): Camera device index (default: 0)
        """
        self.camera_index = camera_index
        self.cap = None
        self.mode = 'canny'  # Default mode
        
        # Edge detection parameters
        self.blur_kernel = (5, 5)
        self.canny_threshold1 = 50
        self.canny_threshold2 = 150
        self.sobel_kernel = 3
        self.laplacian_kernel = 3
        
    def initialize_camera(self):
        """
        Initialize the camera capture.
        """
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera {self.camera_index}")
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("✓ Camera initialized successfully")
        print(f"  Resolution: {int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    
    def preprocess_frame(self, frame):
        """
        Preprocess the frame for edge detection.
        
        Args:
            frame: Input video frame
            
        Returns:
            Preprocessed grayscale and blurred frame
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, self.blur_kernel, 1.4)
        return gray, blurred
    
    def apply_sobel_x(self, blurred):
        """Apply Sobel X edge detection."""
        sobel_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=self.sobel_kernel)
        sobel_x = np.absolute(sobel_x)
        sobel_x = np.uint8(sobel_x)
        return sobel_x
    
    def apply_sobel_y(self, blurred):
        """Apply Sobel Y edge detection."""
        sobel_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=self.sobel_kernel)
        sobel_y = np.absolute(sobel_y)
        sobel_y = np.uint8(sobel_y)
        return sobel_y
    
    def apply_sobel_combined(self, blurred):
        """Apply combined Sobel edge detection."""
        sobel_x = self.apply_sobel_x(blurred)
        sobel_y = self.apply_sobel_y(blurred)
        sobel_combined = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
        return sobel_combined
    
    def apply_laplacian(self, blurred):
        """Apply Laplacian edge detection."""
        laplacian = cv2.Laplacian(blurred, cv2.CV_64F, ksize=self.laplacian_kernel)
        laplacian = np.absolute(laplacian)
        laplacian = np.uint8(laplacian)
        return laplacian
    
    def apply_canny(self, blurred):
        """Apply Canny edge detection."""
        canny = cv2.Canny(blurred, self.canny_threshold1, self.canny_threshold2)
        return canny
    
    def process_frame(self, frame):
        """
        Process a single frame based on current mode.
        
        Args:
            frame: Input video frame
            
        Returns:
            Processed frame with edge detection applied
        """
        gray, blurred = self.preprocess_frame(frame)
        
        if self.mode == 'original':
            return frame
        elif self.mode == 'sobel_x':
            result = self.apply_sobel_x(blurred)
        elif self.mode == 'sobel_y':
            result = self.apply_sobel_y(blurred)
        elif self.mode == 'sobel_combined':
            result = self.apply_sobel_combined(blurred)
        elif self.mode == 'laplacian':
            result = self.apply_laplacian(blurred)
        elif self.mode == 'canny':
            result = self.apply_canny(blurred)
        else:
            result = blurred
        
        # Convert single channel to BGR for consistent display
        if len(result.shape) == 2:
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        
        return result
    
    def add_info_overlay(self, frame):
        """
        Add information overlay to the frame.
        
        Args:
            frame: Frame to add overlay to
            
        Returns:
            Frame with overlay
        """
        # Create a copy to avoid modifying original
        display_frame = frame.copy()
        
        # Add semi-transparent background for text
        overlay = display_frame.copy()
        cv2.rectangle(overlay, (10, 10), (350, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, display_frame, 0.4, 0, display_frame)
        
        # Add text information
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        color = (255, 255, 255)
        thickness = 1
        
        cv2.putText(display_frame, f"Mode: {self.mode.upper()}", 
                   (20, 35), font, font_scale, color, thickness)
        cv2.putText(display_frame, "Controls:", 
                   (20, 60), font, 0.5, (200, 200, 200), thickness)
        cv2.putText(display_frame, "1:Sobel-X  2:Sobel-Y  3:Sobel-Combined", 
                   (20, 80), font, 0.4, color, thickness)
        cv2.putText(display_frame, "4:Laplacian  5:Canny  0:Original  Q:Quit", 
                   (20, 100), font, 0.4, font, thickness)
        
        return display_frame
    
    def run(self):
        """
        Run the real-time edge detection system.
        """
        try:
            self.initialize_camera()
            
            print("\n" + "=" * 60)
            print("REAL-TIME EDGE DETECTION - WEBCAM MODE")
            print("=" * 60)
            print("\nKeyboard Controls:")
            print("  1 - Sobel X (Vertical Edges)")
            print("  2 - Sobel Y (Horizontal Edges)")
            print("  3 - Sobel Combined")
            print("  4 - Laplacian")
            print("  5 - Canny Edge Detection")
            print("  0 - Original Video")
            print("  Q - Quit")
            print("\n" + "=" * 60)
            print("\nPress any key in the video window to start...")
            
            while True:
                # Capture frame
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Process frame based on current mode
                processed_frame = self.process_frame(frame)
                
                # Add information overlay
                display_frame = self.add_info_overlay(processed_frame)
                
                # Display the frame
                cv2.imshow('Real-Time Edge Detection', display_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    print("\n✓ Exiting...")
                    break
                elif key == ord('0'):
                    self.mode = 'original'
                    print("→ Mode: Original")
                elif key == ord('1'):
                    self.mode = 'sobel_x'
                    print("→ Mode: Sobel X")
                elif key == ord('2'):
                    self.mode = 'sobel_y'
                    print("→ Mode: Sobel Y")
                elif key == ord('3'):
                    self.mode = 'sobel_combined'
                    print("→ Mode: Sobel Combined")
                elif key == ord('4'):
                    self.mode = 'laplacian'
                    print("→ Mode: Laplacian")
                elif key == ord('5'):
                    self.mode = 'canny'
                    print("→ Mode: Canny")
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Clean up
            if self.cap is not None:
                self.cap.release()
            cv2.destroyAllWindows()
            print("✓ Camera released and windows closed")


def main():
    """
    Main function to run webcam edge detection.
    """
    import sys
    
    # Get camera index from command line or use default
    camera_index = 0
    if len(sys.argv) > 1:
        try:
            camera_index = int(sys.argv[1])
        except ValueError:
            print(f"Invalid camera index: {sys.argv[1]}")
            print("Using default camera (index 0)")
    
    try:
        detector = WebcamEdgeDetector(camera_index=camera_index)
        detector.run()
    except KeyboardInterrupt:
        print("\n✓ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
