"""
Create a test image with geometric shapes for edge detection demo
"""

import cv2
import numpy as np
import os

# Create output directory
os.makedirs('input', exist_ok=True)

# Create a test image with geometric shapes
width, height = 600, 400
image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background

# Draw various shapes
# Rectangle
cv2.rectangle(image, (50, 50), (200, 150), (0, 0, 255), -1)  # Red filled rectangle
cv2.rectangle(image, (50, 50), (200, 150), (0, 0, 0), 3)    # Black border

# Circle
cv2.circle(image, (350, 100), 60, (0, 255, 0), -1)  # Green filled circle
cv2.circle(image, (350, 100), 60, (0, 0, 0), 3)     # Black border

# Triangle
triangle_pts = np.array([[450, 50], [550, 150], [350, 150]], np.int32)
cv2.fillPoly(image, [triangle_pts], (255, 0, 0))  # Blue filled triangle
cv2.polylines(image, [triangle_pts], True, (0, 0, 0), 3)  # Black border

# Ellipse
cv2.ellipse(image, (150, 280), (80, 50), 0, 0, 360, (255, 255, 0), -1)  # Cyan ellipse
cv2.ellipse(image, (150, 280), (80, 50), 0, 0, 360, (0, 0, 0), 3)  # Black border

# Polygon (Pentagon)
pentagon_pts = np.array([[450, 250], [500, 220], [520, 270], [480, 310], [420, 290]], np.int32)
cv2.fillPoly(image, [pentagon_pts], (255, 0, 255))  # Magenta pentagon
cv2.polylines(image, [pentagon_pts], True, (0, 0, 0), 3)

# Add some text
cv2.putText(image, 'Edge Detection Test', (170, 380), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# Save the image
cv2.imwrite('input/test_image.jpg', image)
print("[OK] Test image created: input/test_image.jpg")
print("     Image contains: rectangles, circles, triangles, ellipses, and polygons")
