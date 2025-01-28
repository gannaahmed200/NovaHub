import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QFileDialog, QComboBox,
                             QSlider, QMessageBox, QGroupBox, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.zoom_factor = 1.0
        self.zoom_method = "Region"
        self.interpolation = cv2.INTER_LINEAR
        self.pan_start = QPoint()
        self.last_pos = QPoint()
        self.drawing_roi = False
        self.roi_start = None
        self.roi_end = None
        self.rois = []
        self.original_image = None
        self.original_pixmap = None
        self.setMouseTracking(True)
        self.setAlignment(Qt.AlignCenter)

    def set_zoom_method(self, method):
        self.zoom_method = method
        self.update_zoom()

    def set_interpolation(self, method):
        interpolation_methods = {
            "Nearest Neighbor": cv2.INTER_NEAREST,
            "Bilinear": cv2.INTER_LINEAR,
            "Bicubic": cv2.INTER_CUBIC,
            "Lanczos": cv2.INTER_LANCZOS4
        }
        self.interpolation = interpolation_methods.get(method, cv2.INTER_LINEAR)
        self.update_zoom()

    def wheelEvent(self, event):
        if self.original_image is not None:
            old_zoom = self.zoom_factor
            delta = event.angleDelta().y()
            zoom_speed = 0.001
            self.zoom_factor *= (1 + (delta * zoom_speed))
            self.zoom_factor = max(0.1, min(5.0, self.zoom_factor))
            pos = event.pos()
            self.update_zoom(pos if self.zoom_method == "Region" else None)
            if hasattr(self.parent, 'update_zoom_spinbox'):
                self.parent.update_zoom_spinbox(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if len(self.rois) < 3:  # Allow up to 3 ROIs
                self.drawing_roi = True
                self.roi_start = event.pos()
                self.roi_end = event.pos()
        elif event.button() == Qt.RightButton:
            self.pan_start = event.pos()
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing_roi and self.roi_start:
            self.roi_end = event.pos()
            self.update()
        elif event.buttons() & Qt.RightButton and self.original_image is not None:
            delta = event.pos() - self.last_pos
            self.last_pos = event.pos()
            self.parent.pan_image(delta)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing_roi:
            self.drawing_roi = False
            if self.roi_start and self.roi_end:
                self.rois.append((self.roi_start, self.roi_end))
                self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.pixmap():
            return

        painter = QPainter(self)

        # Draw existing ROIs with different colors
        colors = [Qt.red, Qt.blue, Qt.green]
        for i, (start, end) in enumerate(self.rois):
            painter.setPen(QPen(colors[i], 2, Qt.SolidLine))
            painter.drawRect(min(start.x(), end.x()), min(start.y(), end.y()),
                           abs(end.x() - start.x()), abs(end.y() - start.y()))

        # Draw ROI being created
        if self.drawing_roi and self.roi_start and self.roi_end:
            painter.setPen(QPen(colors[len(self.rois)], 2, Qt.DashLine))
            painter.drawRect(min(self.roi_start.x(), self.roi_end.x()),
                           min(self.roi_start.y(), self.roi_end.y()),
                           abs(self.roi_end.x() - self.roi_start.x()),
                           abs(self.roi_end.y() - self.roi_start.y()))

    def update_zoom(self, center_pos=None):
        if self.original_image is not None:
            height, width = self.original_image.shape
            new_width = int(width * self.zoom_factor)
            new_height = int(height * self.zoom_factor)

            # Resize image using OpenCV with selected interpolation
            resized = cv2.resize(self.original_image, (new_width, new_height),
                                 interpolation=self.interpolation)

            # Convert to QImage and QPixmap
            bytes_per_line = resized.strides[0]
            image = QImage(resized.data, new_width, new_height,
                           bytes_per_line, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(image)
            self.setPixmap(pixmap)

    def set_image(self, image):
        self.original_image = image
        if image is not None:
            height, width = image.shape
            bytes_per_line = width
            qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
            self.original_pixmap = QPixmap.fromImage(qimage)
            self.update_zoom()

    def set_zoom(self, factor):
        if factor != self.zoom_factor:
            self.zoom_factor = factor
            self.update_zoom()


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Quality Analyzer")
        self.setGeometry(100, 100, 1200, 800)

        self.input_image = None
        self.output1_image = None
        self.output2_image = None
        self.active_output = "Output 1"

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Image display area
        display_layout = QHBoxLayout()

        # Input viewport
        input_group = QGroupBox("Input Image")
        input_layout = QVBoxLayout()
        self.input_label = ImageLabel(self)
        self.input_label.setMinimumSize(300, 300)
        input_layout.addWidget(self.input_label)
        input_group.setLayout(input_layout)

        # Output viewport with selection
        output_group = QGroupBox("Output Image")
        output_layout = QVBoxLayout()
        
        # Add output selection combo box
        self.output_selector = QComboBox()
        self.output_selector.addItems(["Output 1", "Output 2"])
        self.output_selector.currentTextChanged.connect(self.switch_output_display)
        output_layout.addWidget(self.output_selector)
        
        # Single output label
        self.output_label = ImageLabel(self)
        self.output_label.setMinimumSize(300, 300)
        output_layout.addWidget(self.output_label)
        output_group.setLayout(output_layout)

        display_layout.addWidget(input_group)
        display_layout.addWidget(output_group)

        # Controls
        controls_layout = QHBoxLayout()

        # Add Histogram button to file controls
        file_controls = QGroupBox("File Controls")
        file_layout = QVBoxLayout()
        load_btn = QPushButton("Load Image")
        load_btn.clicked.connect(self.load_image)
        show_histogram_btn = QPushButton("Show Histogram")
        show_histogram_btn.clicked.connect(self.show_histogram_dialog)
        file_layout.addWidget(load_btn)
        file_layout.addWidget(show_histogram_btn)
        file_controls.setLayout(file_layout)

        # Zoom controls
        zoom_controls = QGroupBox("Zoom Controls")
        zoom_layout = QVBoxLayout()

        # Zoom method selection
        zoom_layout.addWidget(QLabel("Zoom Method:"))
        self.zoom_method = QComboBox()
        self.zoom_method.addItems(["Region", "Center"])
        self.zoom_method.currentTextChanged.connect(self.change_zoom_method)
        zoom_layout.addWidget(self.zoom_method)

        # Interpolation method selection
        zoom_layout.addWidget(QLabel("Interpolation:"))
        self.interpolation = QComboBox()
        self.interpolation.addItems(["Nearest Neighbor", "Bilinear", "Bicubic", "Lanczos"])
        self.interpolation.currentTextChanged.connect(self.change_interpolation)
        zoom_layout.addWidget(self.interpolation)

        # Zoom factor control
        zoom_layout.addWidget(QLabel("Zoom Factor:"))
        self.zoom_spinbox = QDoubleSpinBox()
        self.zoom_spinbox.setRange(0.1, 5.0)
        self.zoom_spinbox.setSingleStep(0.1)
        self.zoom_spinbox.setValue(1.0)
        self.zoom_spinbox.valueChanged.connect(self.update_zoom_all)
        zoom_layout.addWidget(self.zoom_spinbox)

        # Reset zoom button
        reset_zoom_btn = QPushButton("Reset Zoom")
        reset_zoom_btn.clicked.connect(self.reset_zoom)
        zoom_layout.addWidget(reset_zoom_btn)

        zoom_controls.setLayout(zoom_layout)

        # SNR controls
        snr_controls = QGroupBox("SNR Controls")
        snr_layout = QVBoxLayout()

        self.noise_type = QComboBox()
        self.noise_type.addItems(["Gaussian", "Salt & Pepper", "Speckle"])

        add_noise_btn = QPushButton("Add Noise")
        add_noise_btn.clicked.connect(self.add_noise)

        self.filter_type = QComboBox()
        self.filter_type.addItems(["Mean", "Median", "Gaussian", "Lowpass", "Highpass"])

        apply_filter_btn = QPushButton("Apply Filter")
        apply_filter_btn.clicked.connect(self.apply_filter)

        measure_snr_btn = QPushButton("Measure SNR")
        measure_snr_btn.clicked.connect(self.measure_snr)

        clear_roi_btn = QPushButton("Clear ROIs")
        clear_roi_btn.clicked.connect(self.clear_rois)

        snr_layout.addWidget(QLabel("Noise Type:"))
        snr_layout.addWidget(self.noise_type)
        snr_layout.addWidget(add_noise_btn)
        snr_layout.addWidget(QLabel("Filter Type:"))
        snr_layout.addWidget(self.filter_type)
        snr_layout.addWidget(apply_filter_btn)
        snr_layout.addWidget(measure_snr_btn)
        snr_layout.addWidget(clear_roi_btn)
        snr_controls.setLayout(snr_layout)

        # CNR controls
        cnr_controls = QGroupBox("CNR Controls")
        cnr_layout = QVBoxLayout()

        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(-100, 100)
        self.contrast_slider.setValue(0)

        apply_bc_btn = QPushButton("Apply Brightness/Contrast")
        apply_bc_btn.clicked.connect(self.apply_brightness_contrast)

        self.contrast_method = QComboBox()
        self.contrast_method.addItems(["Histogram Equalization", "CLAHE", "Adaptive Gamma"])

        apply_contrast_btn = QPushButton("Apply Contrast Method")
        apply_contrast_btn.clicked.connect(self.apply_contrast_adjustment)

        measure_cnr_btn = QPushButton("Measure CNR")
        measure_cnr_btn.clicked.connect(self.measure_cnr)

        cnr_layout.addWidget(QLabel("Brightness:"))
        cnr_layout.addWidget(self.brightness_slider)
        cnr_layout.addWidget(QLabel("Contrast:"))
        cnr_layout.addWidget(self.contrast_slider)
        cnr_layout.addWidget(apply_bc_btn)
        cnr_layout.addWidget(QLabel("Contrast Method:"))
        cnr_layout.addWidget(self.contrast_method)
        cnr_layout.addWidget(apply_contrast_btn)
        cnr_layout.addWidget(measure_cnr_btn)
        cnr_controls.setLayout(cnr_layout)

        # Add all controls to layout
        controls_layout.addWidget(file_controls)
        controls_layout.addWidget(zoom_controls)
        controls_layout.addWidget(snr_controls)
        controls_layout.addWidget(cnr_controls)

        # Add all layouts to main layout
        main_layout.addLayout(display_layout)
        main_layout.addLayout(controls_layout)

        # # Connect output page clicks to set active output
        # self.output1_label.mousePressEvent = lambda event: self.set_active_output("Output 1")
        # self.output2_label.mousePressEvent = lambda event: self.set_active_output("Output 2")

    def switch_output_display(self, output_selection):
        """Switch the displayed output based on combo box selection"""
        self.active_output = output_selection
        if output_selection == "Output 1" and self.output1_image is not None:
            self.output_label.set_image(self.output1_image)
        elif output_selection == "Output 2" and self.output2_image is not None:
            self.output_label.set_image(self.output2_image)

    def set_active_output(self, output):
        """Set the active output page."""
        self.active_output = output
        print(f"Active output set to: {output}")

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                   "Image Files (*.png *.jpg *.bmp *.tif)")
        if file_name:
            self.input_image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
            self.input_label.set_image(self.input_image)
            self.clear_rois()

    def change_zoom_method(self, method):
        for label in [self.input_label, self.output1_label, self.output2_label]:
            label.set_zoom_method(method)

    def change_interpolation(self, method):
        for label in [self.input_label, self.output1_label, self.output2_label]:
            label.set_interpolation(method)

    def update_zoom_spinbox(self, sender):
        self.zoom_spinbox.setValue(sender.zoom_factor)

    def update_zoom_all(self, value):
        for label in [self.input_label, self.output1_label, self.output2_label]:
            if label.original_image is not None:
                label.set_zoom(value)

    def reset_zoom(self):
        self.zoom_spinbox.setValue(1.0)
        self.update_zoom_all(1.0)

    def add_noise(self):
        if self.input_image is None:
            return

        noise_type = self.noise_type.currentText()
        noisy_image = self.input_image.copy()

        if noise_type == "Gaussian":
            noise = np.random.normal(0, 25, self.input_image.shape)
            noisy_image = np.clip(self.input_image + noise, 0, 255).astype(np.uint8)
        elif noise_type == "Salt & Pepper":
            prob = 0.05
            rnd = np.random.random(self.input_image.shape)
            noisy_image[rnd < prob / 2] = 0
            noisy_image[rnd > 1 - prob / 2] = 255
        elif noise_type == "Speckle":
            noise = np.random.normal(0, 1, self.input_image.shape)
            noisy_image = np.clip(self.input_image + self.input_image * noise * 0.2, 0, 255).astype(np.uint8)

        if self.active_output == "Output 1":
            self.output1_image = noisy_image
        else:
            self.output2_image = noisy_image
        
        self.output_label.set_image(noisy_image)

    def apply_filter(self):
        if self.input_image is None:
            return

        source_image = self.output1_image if self.active_output == "Output 1" else self.output2_image
        if source_image is None:
            QMessageBox.warning(self, "Warning", "No image available in the active output.")
            return

        filter_type = self.filter_type.currentText()

        if filter_type == "Mean":
            filtered_image = cv2.blur(source_image, (5, 5))
        elif filter_type == "Median":
            filtered_image = cv2.medianBlur(source_image, 5)
        elif filter_type == "Gaussian":
            filtered_image = cv2.GaussianBlur(source_image, (5, 5), 0)
        elif filter_type == "Lowpass":
            kernel = np.ones((5, 5), np.float32) / 25
            filtered_image = cv2.filter2D(source_image, -1, kernel)
        elif filter_type == "Highpass":
            kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
            filtered_image = cv2.filter2D(source_image, -1, kernel)

        if self.active_output == "Output 1":
            self.output1_image = filtered_image
        else:
            self.output2_image = filtered_image
            
        self.output_label.set_image(filtered_image)

    def apply_brightness_contrast(self):
        if self.input_image is None:
            return

        brightness = self.brightness_slider.value()
        contrast = self.contrast_slider.value() / 100.0 + 1.0

        adjusted = cv2.convertScaleAbs(self.input_image, alpha=contrast, beta=brightness)

        if self.active_output == "Output 1":
            self.output1_image = adjusted
        else:
            self.output2_image = adjusted
            
        self.output_label.set_image(adjusted)

    def apply_contrast_adjustment(self):
        if self.input_image is None:
            return

        method = self.contrast_method.currentText()
        adjusted = None

        if method == "Histogram Equalization":
            adjusted = cv2.equalizeHist(self.input_image)
        elif method == "CLAHE":
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            adjusted = clahe.apply(self.input_image)
        elif method == "Adaptive Gamma":
            mean = np.mean(self.input_image)
            gamma = 1.0
            if mean < 128:
                gamma = 0.8  # Brighten dark images
            else:
                gamma = 1.2  # Darken bright images

            lookup_table = np.array([((i / 255.0) ** gamma) * 255
                                     for i in np.arange(0, 256)]).astype("uint8")
            adjusted = cv2.LUT(self.input_image, lookup_table)

        if self.active_output == "Output 1":
            self.output1_image = adjusted
            self.output1_label.set_image(adjusted)
        else:
            self.output2_image = adjusted
            self.output2_label.set_image(adjusted)

    def measure_snr(self):
        if self.input_image is None or len(self.input_label.rois) < 2:
            QMessageBox.warning(self, "Warning", "Please select at least two ROIs on the input image")
            return

        rois_img = self.convert_rois_to_image_coords(self.input_label)
        signal_roi1 = self.get_roi_data(self.input_image, rois_img[0])
        signal_roi2 = self.get_roi_data(self.input_image, rois_img[1])

        # Calculate SNR for both signal regions
        signal_mean1 = np.mean(signal_roi1)
        signal_mean2 = np.mean(signal_roi2)
        noise_std = np.std(signal_roi1)  # Using first ROI's standard deviation as noise

        snr1 = signal_mean1 / noise_std if noise_std != 0 else float('inf')
        snr2 = signal_mean2 / noise_std if noise_std != 0 else float('inf')

        QMessageBox.information(self, "SNR Measurement",
                              f"Signal 1 Mean: {signal_mean1:.2f}\n"
                              f"Signal 2 Mean: {signal_mean2:.2f}\n"
                              f"Noise StdDev: {noise_std:.2f}\n"
                              f"SNR (Signal 1): {snr1:.2f}\n"
                              f"SNR (Signal 2): {snr2:.2f}")

    def measure_cnr(self):
        if self.input_image is None or len(self.input_label.rois) != 3:
            QMessageBox.warning(self, "Warning", "Please select three ROIs on the input image")
            return

        rois_img = self.convert_rois_to_image_coords(self.input_label)
        signal1_roi = self.get_roi_data(self.input_image, rois_img[0])
        signal2_roi = self.get_roi_data(self.input_image, rois_img[1])
        noise_roi = self.get_roi_data(self.input_image, rois_img[2])

        signal1_mean = np.mean(signal1_roi)
        signal2_mean = np.mean(signal2_roi)
        noise_std = np.std(noise_roi)

        if noise_std == 0:
            cnr = float('inf')
        else:
            cnr = abs(signal1_mean - signal2_mean) / noise_std

        QMessageBox.information(self, "CNR Measurement",
                                f"Signal 1 Mean: {signal1_mean:.2f}\n"
                                f"Signal 2 Mean: {signal2_mean:.2f}\n"
                                f"Noise StdDev: {noise_std:.2f}\n"
                                f"CNR: {cnr:.2f}")

    def convert_rois_to_image_coords(self, label):
        if not label.pixmap() or not self.input_image is not None:
            return []

        pixmap_size = label.pixmap().size()
        image_size = (self.input_image.shape[1], self.input_image.shape[0])

        scale_x = image_size[0] / pixmap_size.width()
        scale_y = image_size[1] / pixmap_size.height()

        image_rois = []
        for roi_start, roi_end in label.rois:
            x1 = int(min(roi_start.x(), roi_end.x()) * scale_x)
            y1 = int(min(roi_start.y(), roi_end.y()) * scale_y)
            x2 = int(max(roi_start.x(), roi_end.x()) * scale_x)
            y2 = int(max(roi_start.y(), roi_end.y()) * scale_y)

            x1 = max(0, min(x1, image_size[0] - 1))
            y1 = max(0, min(y1, image_size[1] - 1))
            x2 = max(0, min(x2, image_size[0] - 1))
            y2 = max(0, min(y2, image_size[1] - 1))

            image_rois.append((x1, y1, x2, y2))

        return image_rois

    def get_roi_data(self, image, roi):
        x1, y1, x2, y2 = roi
        return image[y1:y2, x1:x2]

    def show_histogram_dialog(self):
        if self.input_image is None:
            return

        plt.figure(figsize=(10, 4))

        # Plot input image histogram
        plt.subplot(131)
        plt.hist(self.input_image.ravel(), 256, [0, 256])
        plt.title('Input Image')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')

        # Plot output1 histogram if available
        if self.output1_image is not None:
            plt.subplot(132)
            plt.hist(self.output1_image.ravel(), 256, [0, 256])
            plt.title('Output 1')
            plt.xlabel('Pixel Value')

        # Plot output2 histogram if available
        if self.output2_image is not None:
            plt.subplot(133)
            plt.hist(self.output2_image.ravel(), 256, [0, 256])
            plt.title('Output 2')
            plt.xlabel('Pixel Value')

        plt.tight_layout()
        plt.show()

    def plot_histogram(self, image, title):
        plt.figure()
        plt.hist(image.ravel(), 256, [0, 256])
        plt.title(title)
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.show()

    def clear_rois(self):
        self.input_label.rois = []
        self.input_label.roi_start = None
        self.input_label.roi_end = None
        self.input_label.update()

    def pan_image(self, delta):
        if self.sender() == self.input_label and self.input_image is not None:
            self.input_label.update_zoom()
        elif self.sender() == self.output1_label and self.output1_image is not None:
            self.output1_label.update_zoom()
        elif self.sender() == self.output2_label and self.output2_image is not None:
            self.output2_label.update_zoom()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())