# DICOM Viewer

## Overview

This repository contains a custom-built DICOM viewer application, developed as part of a student project. The application provides an intuitive interface to view, explore, and anonymize DICOM files, supporting both 2D and 3D imaging data. It was inspired by existing DICOM viewers such as RadiAnt, MicroDicom, IMAIOS, and ezDICOM.

## Features

1. **DICOM File Support**

   - Open and view any DICOM file containing 2D, Multi-2D (M2D), or 3D images.


2. **Viewing Options**

   - **2D Images:** Display single 2D images.
   - **M2D Images:** Display images as a video.
   - **3D Images:** Display slices as tiled views.

3. **DICOM Tag Exploration**

   - Display all DICOM tags in the file along with their values.
   - Search for specific DICOM tags and display their values.
   - Explore values of key DICOM elements (Patient, Study, Modality, Physician, Image) through dedicated UI buttons.


4. **Anonymization**

   - Anonymize critical information in the DICOM file by replacing sensitive data with random values prefixed by user-provided text.

### Images to Explain

Below are some images that illustrate key aspects of the project:

![Image 1](https://github.com/user-attachments/assets/bb4789a3-f4a5-4887-b56e-3785c8834e0b)
![Image 2](https://github.com/user-attachments/assets/88c481a4-0e7b-4de1-bd1e-59963d807096)
![Image 3](https://github.com/user-attachments/assets/2a8b8aa0-d0a7-4ac8-b7aa-09a9a0f692aa)
![Image 4](https://github.com/user-attachments/assets/88aedf81-36d2-4791-b4e2-ddf8032ba6e9)
![Image 5](https://github.com/user-attachments/assets/37dce5a1-21bd-4b14-9a0b-b17f45aed551)

## Technology Stack

- **Programming Language:** [Specify the language, e.g., Python, C++, etc.]
- **Libraries/Frameworks:**
  - [Specify relevant libraries, e.g., PyDicom, SimpleITK, etc.]

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/dicom-viewer.git
   cd dicom-viewer
   ```

2. Run the application:

   ```bash
   python main.py
   ```

## Usage

1. **Opening a File:** Use the "Open File" button in the UI to load a DICOM file.
2. **Viewing Images:**
   - For M2D: Click "Play" to view images as a video.
   - For 3D: Images will be displayed as a tiled view.
3. **Exploring Tags:** Use the dedicated buttons or search functionality to explore specific DICOM tags.
4. **Anonymizing Files:**
   - Enter a prefix in the "Anonymization" input field.
   - Click the "Anonymize" button to replace sensitive data.

## Acknowledgments

- **Inspired By:**
  - RadiAnt
  - MicroDicom
  - IMAIOS
  - ezDICOM
  - OsiriX
- **Special Thanks:**
  - [Mention any instructors, supervisors, or collaborators]

## License

This project is licensed under the [Your License Name] License. See the LICENSE file for details.

---

