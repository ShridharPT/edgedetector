# 🚀 Quick Start Guide

Get started with edge detection in just a few steps!

## ⚡ Installation (1 minute)

```bash
# Install required packages
pip install -r requirements.txt
```

## 🎯 Option 1: Use Sample Images

```bash
# Download sample test images
python download_sample_images.py

# Run edge detection on a sample
python edge_detection.py input/sample1.png
```

## 📸 Option 2: Use Your Own Images

```bash
# Copy your image to the input folder
# (Place any .jpg, .png, or .bmp file in the 'input' folder)

# Run edge detection
python edge_detection.py input/your_image.jpg
```

## 🎥 Option 3: Live Webcam Detection

```bash
# Start real-time edge detection
python edge_detection_webcam.py

# Controls:
# - Press 1-5 to switch between algorithms
# - Press Q to quit
```

## 📦 Batch Processing Multiple Images

```bash
# Process all images in the input folder
python batch_process.py

# Process with display (shows each result)
python batch_process.py --display
```

## 📊 What You'll Get

After running edge detection, you'll get 7 processed images:
- Original (grayscale)
- Gaussian blurred version
- Sobel X (vertical edges)
- Sobel Y (horizontal edges)
- Sobel combined
- Laplacian edges
- Canny edges (best quality)

All saved in the `output/` folder!

## 🎨 Customizing Parameters

Edit the Python files to adjust:
- **Blur amount**: Change `blur_kernel_size` in `preprocess()`
- **Edge sensitivity**: Adjust thresholds in `apply_canny()`
- **Kernel sizes**: Modify kernel parameters in Sobel/Laplacian

## 🆘 Troubleshooting

**"No module named cv2"**
```bash
pip install opencv-python
```

**"Could not read image"**
- Check the file path is correct
- Ensure the image format is supported

**Webcam not working**
- Try different camera index: `python edge_detection_webcam.py 1`
- Check camera permissions

## 📖 Need More Help?

See the full [README.md](README.md) for detailed documentation!

---
**Happy edge detecting! 🎯**
