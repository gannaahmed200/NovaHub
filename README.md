# Multi-Planar DICOM Viewer Project

This project is a custom DICOM viewer application designed to facilitate the visualization and interaction with medical imaging data. It provides multi-planar imaging capabilities, navigation features, and image manipulation tools to enhance user experience.

## Features

### 1. Multi-Planar Image Viewports
- **Three separate viewers** to visualize different planes of the 3D volume.
- Each viewport displays slices from a specific orientation.

### 2. Basic Navigation Features
- **Slice Scrolling**: Navigate through slices in each view using the scroll wheel.
- **Cine Play/Pause/Stop**: Play a series of slices like a movie, with options to pause or stop playback.
- **Slice Indicator**: Highlights the corresponding slice in other planar viewers to maintain spatial context.

### 3. Basic Image Manipulation Features
- **Zoom In/Out**: Use the mouse to zoom into or out of the image for better detail visualization.
- **Brightness and Contrast Control**: Adjust brightness and contrast interactively using mouse movements.

### 4. 3D Point Mapping
- Select a point in the 3D volume, and the application displays its location in all three 2D planar viewers.

## Requirements

### Software Dependencies
- **Programming Language**: Python
- **Libraries/Frameworks**: 
  - vtk
  - PyQt or other GUI framework (if applicable)
  - numpy
  - pydicom
  
### Hardware Requirements
- A computer capable of running Python and handling medical imaging data.
- A compatible mouse for zoom and adjustment controls.

## Usage
1. Launch the application:
   ```bash
   python main.py
   ```
2. Load a DICOM dataset using the provided file dialog.
3. Use the navigation and manipulation tools to explore the dataset.

## Contributing
We welcome contributions to this project! Please follow these steps:
1. Fork this repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to your forked repository:
   ```bash
   git push origin feature-branch-name
   ```
5. Open a pull request on the main repository.

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For questions or feedback, please open an issue in this repository or contact the maintainer at [your.email@example.com].

