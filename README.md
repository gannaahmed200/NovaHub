
# Image Viewer with Advanced Image Processing Techniques

## Overview
This project is an image viewer application that provides various advanced image processing functionalities. The user can view, modify, and analyze grayscale images using a variety of tools, such as zooming, filtering, noise addition, and denoising techniques. The application supports two viewports where the user can apply changes sequentially to the image and compare the results. The viewer also includes the ability to display image histograms for further analysis.

## Features
- **Input and Output Viewports:** 
  - View an input image in the first viewport.
  - Apply changes on the input image and see the result in the second viewport.
  - Sequential processing: Apply multiple changes to an image and view the results in different output viewports.
  
- **Image Manipulation:**
  - **Zooming:** Zoom in/out with different interpolation methods, including:
    - Nearest-Neighbor Interpolation
    - Linear Interpolation
    - Bilinear Interpolation
    - Cubic Interpolation
  
- **Image Analysis:**
  - **Histogram Display:** Double-click (or another action) to display the histogram of any image at any point.
  - **SNR (Signal-to-Noise Ratio):** Measure the SNR or CNR (Contrast-to-Noise Ratio) by selecting two regions of interest (ROIs) and calculating the average intensities inside them.
  
- **Noise Addition and Denoising:**
  - Add three types of noise to the image: 
    - Gaussian Noise
    - Salt and Pepper Noise
    - Poisson Noise
  - Apply three different denoising techniques to clean the noisy image:
    - Gaussian Blur
    - Median Filter
    - Bilateral Filter

- **Filtering:**
  - Apply low-pass and high-pass filters to enhance or suppress certain frequencies in the image.

- **Contrast and Brightness Adjustment:**
  - Change the brightness and contrast of the image.
  - Apply three types of contrast adjustment methods:
    - Histogram Equalization
    - CLAHE (Contrast Limited Adaptive Histogram Equalization)
    - Custom Contrast Adjustment

## Getting Started
Follow these steps to get the project running on your local machine.

### Prerequisites
Make sure you have the following installed:
- Python 3.x
- Required Python libraries:
  - `numpy`
  - `opencv-python`
  - `matplotlib`
  - `PIL`
  - `scikit-image`
  - `scipy`

You can install the required libraries using:
```bash
pip install -r requirements.txt
```

### Running the Application
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/image-viewer.git
   cd image-viewer
   ```

2. Run the application:
   ```bash
   python image_viewer.py
   ```

### Using the Application
1. **Load an Image:** Open a grayscale image in the input viewport.
2. **Apply Changes:**
   - Zoom in/out and adjust the image resolution using different interpolation methods.
   - Add noise and apply denoising techniques.
   - Change the brightness and contrast of the image.
   - Apply low-pass or high-pass filters.
   - Apply different contrast adjustment techniques to improve CNR.
3. **View Results:** See the changes in the output viewports and their histograms.

### Histogram Analysis
- Double-click on any image in the viewport to see the histogram of that image.
  
### Measuring SNR/CNR
- Select two regions of interest (ROIs) in the image to calculate the SNR or CNR by measuring the average pixel intensities within them.

## Example Workflow
1. Load a grayscale image into the input viewport.
2. Zoom in on the image using linear interpolation.
3. Apply Gaussian noise and view the noisy image in output1.
4. Denoise the image using a median filter and view the result in output2.
5. Adjust the contrast using histogram equalization and observe the improvements in the output.
6. Measure the SNR/CNR by selecting two ROIs and comparing their average intensities.

## Project Structure
```
image-viewer/
│
├── image_viewer.py          # Main application code
├── requirements.txt         # List of Python dependencies
├── images/                  # Folder containing sample images for testing
│
└── README.md                # Project documentation
```

## Contributing
We welcome contributions to this project! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Commit your changes.
4. Push your changes to your forked repository.
5. Open a pull request with a description of the changes you've made.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
