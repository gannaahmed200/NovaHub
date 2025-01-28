# AI Organ Classifier

An AI model designed to classify medical images of the main organs: **heart**, **brain**, **liver**, and **limbs**. This project aims to assist in the automated analysis of medical images, making the process faster and more accurate.

## Features
- **Organ Classification**: Identifies and classifies the organ in the input medical image.
- **Supported Organs**: Heart, Brain, Liver, and Limbs.
- **High Accuracy**: Trained on a robust dataset to ensure precision.
- **User-Friendly**: Easy-to-use interface for predictions.



## Images

### Image 1
![Description of Image 1](https://github.com/user-attachments/assets/6b22a5d3-71eb-4cfa-a8a2-f5431ee1a35c)

### Image 2
![Description of Image 2](https://github.com/user-attachments/assets/2ccc88b2-fa6f-4721-959e-2934681bbe06)

### Image 3
![Description of Image 3](https://github.com/user-attachments/assets/464cfe4a-930f-4266-aece-49df77d39d3f)

### Image 4
![Description of Image 4](https://github.com/user-attachments/assets/e81c517e-6a98-48b3-9b8a-e6156b1569bd)

### Image 5
![Description of Image 5](https://github.com/user-attachments/assets/39981851-196b-48a5-8d43-5b03f6f04be8)

### Image 6
![Description of Image 6](https://github.com/user-attachments/assets/0e15e9cc-217a-4df2-9016-45efb3ea2d2b)

### Image 7
![Description of Image 7](https://github.com/user-attachments/assets/8e1188ca-d085-453a-8c24-5d9814fbc522)


## Table of Contents
1. [Usage](#usage)
2. [Dataset](#dataset)
3. [Development Environment](#development-environment)
4. [Contributing](#contributing)
5. [License](#license)

---
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

