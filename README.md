# AI Organ Classifier

An AI model designed to classify medical images of the main organs: **heart**, **brain**, **liver**, and **limbs**. This project aims to assist in the automated analysis of medical images, making the process faster and more accurate.

## Features
- **Organ Classification**: Identifies and classifies the organ in the input medical image.
- **Supported Organs**: Heart, Brain, Liver, and Limbs.
- **High Accuracy**: Trained on a robust dataset to ensure precision.
- **User-Friendly**: Easy-to-use interface for predictions.

---

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Dataset](#dataset)
4. [Development Environment](#development-environment)
5. [Contributing](#contributing)
6. [License](#license)

---

## Installation

### Prerequisites
- Python 3.8 or above
- VS Code installed with Python support
- Required libraries (TensorFlow, NumPy, Matplotlib, etc.)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-organ-classifier.git
   cd ai-organ-classifier
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Train the Model**:
   - Place your dataset in the `data` folder.
   - Run the training script:
     ```bash
     python train.py
     ```
   - The trained model will be saved in the `models` folder.

2. **Predict Using Pre-Trained Model**:
   - Place your test image in the `test_images` folder.
   - Run the prediction script:
     ```bash
     python predict.py --image test_images/example.jpg
     ```
   - The result will display the predicted organ class.

---

## Dataset
The model is trained on a curated dataset of medical images. Each image is labeled with the organ it represents.  
To use your own dataset:
1. Organize your dataset into subfolders by organ class (e.g., `data/heart`, `data/brain`).
2. Update the `config.json` file with the dataset path.

---

## Development Environment
- **Code Editor**: [VS Code](https://code.visualstudio.com/)
- **Programming Language**: Python 3.8+
- **Libraries Used**:
  - TensorFlow
  - NumPy
  - Matplotlib
  - OpenCV (optional, for image preprocessing)

---

## Contributing
We welcome contributions to enhance the AI Organ Classifier. Here's how you can contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature description"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact
For questions or support, please contact:
- **Email**: your-email@example.com
- **GitHub Issues**: [Open an Issue](https://github.com/your-username/ai-organ-classifier/issues)

