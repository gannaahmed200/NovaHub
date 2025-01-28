import sys
import os
import random
import string
import pydicom
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QLabel, QSlider, QWidget, QPushButton, QFileDialog,
                             QTableWidget, QTableWidgetItem, QTabWidget, QLineEdit,
                             QMessageBox, QListWidget, QSplitter, QInputDialog,QToolBar,QAction)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, QTimer
import matplotlib.pyplot as plt

class EnhancedDicomViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Advanced DICOM Viewer - M@D Edition')
        self.setGeometry(100, 100, 1600, 900)
        self.setStyleSheet("""
            QMainWindow { background-color: #2c3e50; }
            QPushButton { background-color: #3498db; color: white; border: none; padding: 8px; border-radius: 4px; }
            QPushButton:hover { background-color: #2980b9; }
            QLabel { color: black; }
            QTabWidget::pane { background-color: #34495e; border: 1px solid #2c3e50; }
        """)

        # Instance variables
        self.setup_ui()
        self.dicom_files = []
        self.current_index = -1  # Track the current DICOM file index
        self.pixel_array = None

        # Timer for cine mode
        self.cine_timer = QTimer()
        self.cine_timer.timeout.connect(self.update_cine_image)

    def setup_ui(self):
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Add a toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Tile Mode Icon in Toolbar
        tile_icon = QAction('Display Tiles', self)
        tile_icon.setToolTip("Display slices in tile mode")
        tile_icon.triggered.connect(self.display_tiles)
        self.toolbar.addAction(tile_icon)

        # Create main splitter for file list and viewer
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.file_list_widget = self.create_file_list_widget()
        self.viewer_widget = self.create_viewer_widget()

        # Add splitter to main layout
        self.main_splitter.addWidget(self.file_list_widget)
        self.main_splitter.addWidget(self.viewer_widget)
        main_layout.addWidget(self.main_splitter)

        self.slice_slider.setEnabled(False)
        self.cine_button.setEnabled(False)

    def create_file_list_widget(self):
        file_list_widget = QListWidget()
        file_list_widget.setStyleSheet("""
            QListWidget { background-color: #34495e; color: white; }
            QListWidget::item { padding: 5px; border-bottom: 1px solid #2c3e50; }
            QListWidget::item:selected { background-color: #3498db; }
        """)
        file_list_widget.itemClicked.connect(self.load_selected_dicom)
        return file_list_widget
    
    def create_viewer_widget(self):
        viewer_widget = QWidget()
        viewer_layout = QVBoxLayout()
        viewer_widget.setLayout(viewer_layout)

        # Top buttons layout
        top_buttons_layout = QHBoxLayout()
        self.create_buttons(top_buttons_layout)
        viewer_layout.addLayout(top_buttons_layout)

        # Create tab widget and image display tab
        self.tab_widget = QTabWidget()
        self.image_tab = self.create_image_tab()
        self.tags_tab = self.create_tags_tab()

        self.tab_widget.addTab(self.image_tab, "Image")
        self.tab_widget.addTab(self.tags_tab, "DICOM Tags")
        viewer_layout.addWidget(self.tab_widget)

        return viewer_widget

    def create_buttons(self, layout):
        upload_button = QPushButton('Upload DICOM Files')
        upload_button.clicked.connect(self.upload_dicom_files)
        layout.addWidget(upload_button)

        anonymize_button = QPushButton('Anonymize Selected')
        anonymize_button.clicked.connect(self.anonymize_dicom)
        layout.addWidget(anonymize_button)

    def create_image_tab(self):
        image_tab = QWidget()
        image_layout = QVBoxLayout()
        image_tab.setLayout(image_layout)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(800, 600)  # Fixed size for consistent display dimensions
        image_layout.addWidget(self.image_label)

        # Create Slider to scroll through images
        self.slice_slider = QSlider(Qt.Horizontal)
        self.slice_slider.setFixedHeight(20)
        self.slice_slider.valueChanged.connect(self.update_image)
        image_layout.addWidget(self.slice_slider)

        # Add Cine Mode button below the slider
        self.cine_button = QPushButton('Cine Mode')
        self.cine_button.setCheckable(True)
        self.cine_button.toggled.connect(self.toggle_cine_mode)
        image_layout.addWidget(self.cine_button)

        return image_tab

    def create_tags_tab(self):
        tags_tab = QWidget()
        tags_layout = QVBoxLayout()
        tags_tab.setLayout(tags_layout)

        search_layout = QHBoxLayout()
        self.tag_search_input = QLineEdit(placeholderText='Search DICOM Tag (e.g. PatientName)')
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.search_dicom_tag)
        search_layout.addWidget(self.tag_search_input)
        search_layout.addWidget(search_button)
        tags_layout.addLayout(search_layout)

        self.tags_table = QTableWidget(columnCount=3)
        self.tags_table.setHorizontalHeaderLabels(['Tag', 'VR', 'Value'])
        tags_layout.addWidget(self.tags_table)

        group_layout = QHBoxLayout()
        groups = ['Patient', 'Study', 'Modality', 'Physician', 'Image']
        for group in groups:
            group_btn = QPushButton(f'{group} Info')
            group_btn.clicked.connect(lambda checked, g=group: self.explore_group(g))
            group_layout.addWidget(group_btn)
        tags_layout.addLayout(group_layout)

        return tags_tab

    def toggle_cine_mode(self, checked):
        if checked:
            self.cine_button.setText("Stop Cine Mode")
            self.cine_timer.start(100)  # Adjust this for speed of cine mode (100 ms)
        else:
            self.cine_button.setText("Cine Mode")
            self.cine_timer.stop()

    def update_cine_image(self):
        if self.dicom_files or self.pixel_array is not None or self.pixel_array.ndim == 3:
            # Move to the next slice
            self.current_index = (self.current_index + 1) % self.pixel_array.shape[0]  # Wrap around using modulo
            self.slice_slider.setValue(self.current_index)
            self.update_image(self.current_index)  # Display the next slice

    def upload_dicom_files(self):
        file_dialog = QMessageBox.question(
            self, 'Select Input Type',
            'Do you want to select a single file or a folder?',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel)

        if file_dialog == QMessageBox.Yes:
            file_paths, _ = QFileDialog.getOpenFileNames(self, 'Open DICOM Files', '', 'DICOM Files (*.dcm)')
            if file_paths:
                self.process_file_paths(file_paths)
        
        elif file_dialog == QMessageBox.No:
            folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder', '')
            if folder_path:
                self.load_dicom_files_from_folder(folder_path)

    def load_dicom_files_from_folder(self, folder_path):
        self.dicom_files.clear()
        self.file_list_widget.clear()

        file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.dcm')]
        file_paths.sort()

        self.process_file_paths(file_paths)
    
    def process_file_paths(self, file_paths):
        for file_path in file_paths:
            try:
                dicom_data = pydicom.dcmread(file_path)
                self.dicom_files.append(dicom_data)
                patient_name = dicom_data.get('PatientName', 'Unknown')
                study_desc = dicom_data.get('StudyDescription', 'No Description')
                list_item = f"{patient_name} - {study_desc}"
                self.file_list_widget.addItem(list_item)
            except Exception as e:
                QMessageBox.warning(self, 'Warning', f'Failed to load {file_path}: {str(e)}')

        if self.dicom_files:
            self.file_list_widget.setCurrentRow(0)
            self.current_index = 0  # Reset the current index
            self.slice_slider.setRange(0, len(self.dicom_files) - 1)
            self.slice_slider.setValue(self.current_index)  # Start at first item
            self.load_selected_dicom(self.file_list_widget.item(0))
            self.slice_slider.setEnabled(True)
            self.cine_button.setEnabled(True)

    def load_selected_dicom(self, item):
        index = self.file_list_widget.row(item)
        self.current_index = index  # Set the current index based on selection
        self.current_dicom = self.dicom_files[index]
        self.process_dicom_images()
        self.populate_tags_table()

    def process_dicom_images(self):
        self.pixel_array = self.current_dicom.pixel_array
        
        # Handle the pixel array shape properly
        if self.pixel_array.ndim == 4 and self.pixel_array.shape[3] == 3:
            self.pixel_array = np.mean(self.pixel_array, axis=-1).astype(np.uint8)

        # Normalize if not already uint8
        if self.pixel_array.dtype != np.uint8:
            self.pixel_array = self.normalize_image(self.pixel_array)

        if self.pixel_array.ndim == 2:
            self.display_image()
        elif self.pixel_array.ndim == 3:
            self.display_m2d_images()
        else:
            QMessageBox.warning(self, 'Unsupported DICOM', 'Unsupported DICOM file format.')

    def display_image(self):
        height, width = self.pixel_array.shape
        q_image = QImage(self.pixel_array.data, width, height, width, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.slice_slider.setVisible(True)

    def display_m2d_images(self):
        depth, height, width = self.pixel_array.shape
        self.slice_slider.setRange(0, depth - 1)
        self.slice_slider.setValue(0)  # Initialize slider to the first slice
        self.slice_slider.setVisible(True)
        self.update_image(0)  # Display the first slice

    def display_tiles(self):
        """Display multiple DICOM files as tiles in a grid layout."""
        try:
            if not self.dicom_files:
                QMessageBox.warning(self, "Error", "No DICOM files loaded.")
                return

            # Prepare pixel arrays from all DICOM files
            slices = []
            for dicom_data in self.dicom_files:
                if hasattr(dicom_data, 'pixel_array'):
                    pixel_array = self.normalize_image(dicom_data.pixel_array)
                    slices.append(pixel_array)

            if not slices:
                QMessageBox.warning(self, "Error", "No image data found in DICOM files.")
                return

            # Arrange slices in a grid
            num_slices = len(slices)
            num_columns = min(5, num_slices)  # Limit to 5 columns
            num_rows = (num_slices + num_columns - 1) // num_columns

            fig, axs = plt.subplots(num_rows, num_columns, figsize=(15, num_rows * 3))
            axs = axs.flatten()  # Flatten axes for easy iteration

            for i, ax in enumerate(axs):
                if i < num_slices:
                    ax.imshow(slices[i], cmap='gray', aspect='auto')
                    ax.axis('off')
                    ax.set_title(f"Image {i + 1}")
                else:
                    ax.axis('off')  # Hide unused axes

            plt.tight_layout()
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error displaying tiles: {e}")


    def update_image(self,value):
        if self.pixel_array.ndim in [3,4]:
            current_slice = self.slice_slider.value()
            # Handle both 3D (many slices) and 4D (if color channels)
            display_image = self.pixel_array[current_slice] if self.pixel_array.ndim == 3 else self.pixel_array[current_slice, :, :]
            
            height, width = display_image.shape
            q_image = QImage(display_image.data, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.current_index = value
            self.load_selected_dicom(self.file_list_widget.item(self.current_index))

    def normalize_image(self, image):
        """Normalize the image to 8-bit for display"""
        image = image.astype(float)
        image_min = image.min()
        image_max = image.max()
        if image_max - image_min > 0:  # Avoid division by zero
            image = (image - image_min) / (image_max - image_min)  # Normalize to [0, 1]
        return (image * 255).astype(np.uint8)

    def populate_tags_table(self):
        self.tags_table.setRowCount(0)
        for elem in self.current_dicom:
            if elem.VR is not None:
                self.add_tag_row(str(elem.tag), str(elem.VR), str(elem.value))

    def add_tag_row(self, tag, vr, value):
        row_position = self.tags_table.rowCount()
        self.tags_table.insertRow(row_position)
        self.tags_table.setItem(row_position, 0, QTableWidgetItem(tag))
        self.tags_table.setItem(row_position, 1, QTableWidgetItem(vr))
        self.tags_table.setItem(row_position, 2, QTableWidgetItem(value))

    def search_dicom_tag(self):
        tag_name = self.tag_search_input.text().lower()
        self.tags_table.setRowCount(0)

        if not self.current_dicom:
            return

        for elem in self.current_dicom:
            if tag_name in str(elem.name).lower():
                self.add_tag_row(str(elem.tag), str(elem.VR), str(elem.value))
                

    def explore_group(self, group_name):
        groups = {
            'Patient': ['PatientName', 'PatientID', 'PatientBirthDate', 'PatientSex'],
            'Study': ['StudyInstanceUID', 'StudyDate', 'StudyDescription'],
            'Modality': ['Modality', 'BodyPartExamined', 'SeriesDescription'],
            'Physician': ['ReferringPhysicianName', 'PerformingPhysicianName'],
            'Image': ['SliceLocation', 'ImagePosition', 'PixelSpacing']
        }

        self.tags_table.setRowCount(0)
        if not self.current_dicom:
            return
            
        for tag_name in groups.get(group_name, []):
            try:
                elem = self.current_dicom[tag_name]
                self.add_tag_row(tag_name, str(elem.VR), str(elem.value))
            except KeyError:
                continue

    def anonymize_dicom(self):
        if not self.current_dicom:
            QMessageBox.warning(self, 'Warning', 'No DICOM file selected.')
            return

        # Prompt for prefix for anonymization
        prefix, ok = QInputDialog.getText(self, 'Anonymization', 'Enter prefix for anonymized data:')
        if not ok:
            return

        # Tags to anonymize
        tags_to_anonymize = [
            'PatientName', 'PatientID', 'PatientBirthDate',
            'PatientSex', 'ReferringPhysicianName'
        ]

        for tag in tags_to_anonymize:
            try:
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                anonymized_value = f"{prefix}{random_suffix}"
                self.current_dicom[tag].value = anonymized_value
            except KeyError:
                continue

        save_path, _ = QFileDialog.getSaveFileName(self, 'Save Anonymized DICOM', '', 'DICOM Files (*.dcm)')
        if save_path:
            try:
                self.current_dicom.save_as(save_path)
                QMessageBox.information(self, 'Success', f'Anonymized file saved to {save_path}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save anonymized file: {str(e)}')


def main():
    app = QApplication(sys.argv)
    viewer = EnhancedDicomViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()