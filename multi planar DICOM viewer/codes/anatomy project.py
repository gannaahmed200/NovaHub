import sys
import os
import numpy as np
import vtk
import nibabel as nib
import pydicom
from PyQt5 import QtWidgets, QtCore
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util import numpy_support


class MedicalImageViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Medical Image Viewer")
        self.setGeometry(100, 100, 1600, 900)
        self.image_data, self.orientation = None, ['Sagittal', 'Coronal', 'Axial']
        self.current_slice, self.total_slices, self.playing = [0] * 3, [0] * 3, False
        self.timer, self.marks = QtCore.QTimer(), []
        self.timer.timeout.connect(self.play_slices)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)
        views_layout, controls_layout = QtWidgets.QHBoxLayout(), QtWidgets.QHBoxLayout()
        self.renderers, self.vtk_widgets = [], []

        # إعداد 3 Views
        for _ in range(3):
            vtk_widget = QVTKRenderWindowInteractor(self)
            renderer = vtk.vtkRenderer()
            vtk_widget.GetRenderWindow().AddRenderer(renderer)
            self.renderers.append(renderer)
            self.vtk_widgets.append(vtk_widget)
            views_layout.addWidget(vtk_widget)
            vtk_widget.GetRenderWindow().GetInteractor().AddObserver("LeftButtonPressEvent", self.on_left_button_press)

        # إضافة 3D View
        vtk_widget_3d = QVTKRenderWindowInteractor(self)
        renderer_3d = vtk.vtkRenderer()
        vtk_widget_3d.GetRenderWindow().AddRenderer(renderer_3d)
        self.renderers.append(renderer_3d)
        self.vtk_widgets.append(vtk_widget_3d)
        views_layout.addWidget(vtk_widget_3d)
        vtk_widget_3d.GetRenderWindow().GetInteractor().AddObserver("LeftButtonPressEvent", self.on_left_button_press)

        load_button = QtWidgets.QPushButton("Load Image")
        load_button.clicked.connect(self.load_image)
        self.contrast_slider, self.brightness_slider = self.create_slider(), self.create_slider()

        play_button = QtWidgets.QPushButton("Play")
        play_button.setCheckable(True)
        play_button.clicked.connect(self.toggle_play)

        controls_layout.addWidget(load_button)
        controls_layout.addWidget(QtWidgets.QLabel("Contrast"))
        controls_layout.addWidget(self.contrast_slider)
        controls_layout.addWidget(QtWidgets.QLabel("Brightness"))
        controls_layout.addWidget(self.brightness_slider)
        controls_layout.addWidget(play_button)

        self.sliders = [self.create_slider(vertical=True) for _ in range(3)]
        for i, slider in enumerate(self.sliders):
            slider.valueChanged.connect(lambda value, idx=i: self.on_slider_change(idx, value))
            controls_layout.addLayout(self.create_slider_layout(slider, self.orientation[i]))

        layout.addLayout(views_layout)
        layout.addLayout(controls_layout)
        self.contrast_slider.valueChanged.connect(self.update_window_level)
        self.brightness_slider.valueChanged.connect(self.update_window_level)
        self.setup_interactor_styles()

    def create_slider(self, vertical=False):
        slider = QtWidgets.QSlider(QtCore.Qt.Vertical if vertical else QtCore.Qt.Horizontal)
        slider.setMinimum(-100 if not vertical else 0)
        slider.setMaximum(100 if not vertical else 100)
        slider.setValue(0)
        return slider

    def create_slider_layout(self, slider, label_text):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel(label_text), alignment=QtCore.Qt.AlignHCenter)
        layout.addWidget(slider)
        return layout

    def load_image(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Medical Image", "",
                                                             "NIfTI Files (*.nii *.nii.gz);;DICOM Directory (*.dcm);;All Files (*)")
        if file_path:
            try:
                self.image_data = (nib.load(file_path).get_fdata() if file_path.endswith(('.nii', '.nii.gz'))
                                   else self.load_dicom_directory(file_path))
                if self.image_data.dtype != np.uint16:
                    self.image_data = self.normalize_to_uint16(self.image_data)
                self.setup_views()
                for i in range(3):
                    self.sliders[i].setMaximum(self.image_data.shape[i] - 1)
                    self.sliders[i].setValue(self.current_slice[i])

                # ضبط السطوع والتباين الافتراضي
                self.contrast_slider.setValue(20)  # قيمة تباين متوسطة
                self.brightness_slider.setValue(30)  # قيمة سطوع متوسطة
                self.update_window_level()  # تحديث المستوى بعد تعيين القيم الجديدة

            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load image:\n{str(e)}")

    def normalize_to_uint16(self, data):
        data_min, data_max = np.min(data), np.max(data)
        return np.zeros(data.shape, dtype=np.uint16) if data_max - data_min == 0 else \
            ((data - data_min) / (data_max - data_min) * 65535).astype(np.uint16)

    def load_dicom_directory(self, directory):
        files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.dcm')]
        if not files:
            raise ValueError("No DICOM files found in the directory.")
        dicoms = sorted([pydicom.dcmread(f) for f in files],
                        key=lambda x: float(
                            x.ImagePositionPatient[2]) if 'ImagePositionPatient' in x else x.InstanceNumber)
        return np.stack([d.pixel_array for d in dicoms], axis=-1)

    def numpy_to_vtk_image(self, data):
        vtk_data_array = numpy_support.numpy_to_vtk(data.flatten(order='F'), deep=True,
                                                    array_type=vtk.VTK_UNSIGNED_SHORT)
        image = vtk.vtkImageData()
        image.SetDimensions(data.shape)
        image.GetPointData().SetScalars(vtk_data_array)
        return image

    def setup_views(self):
        if self.image_data is None:
            return
        self.total_slices = self.image_data.shape
        self.current_slice = [dim // 2 for dim in self.total_slices]
        for renderer in self.renderers:
            renderer.RemoveAllViewProps()
        vtk_image = self.numpy_to_vtk_image(self.image_data)
        self.planes = [self.create_image_reslice(vtk_image, i) for i in range(3)]
        self.actors = self.setup_actors()

        # إعداد الـ 3D View
        self.setup_3d_view(vtk_image)

    def create_image_reslice(self, vtk_image, i):
        reslice = vtk.vtkImageReslice()
        reslice.SetInputData(vtk_image)
        reslice.SetInterpolationModeToLinear()
        reslice.SetOutputDimensionality(2)
        axes = vtk.vtkMatrix4x4()
        axes.DeepCopy((0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1) if i == 0 else
                      (1, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 1) if i == 1 else
                      (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1))
        reslice.SetResliceAxes(axes)
        reslice.SetResliceAxesOrigin(*(self.current_slice[i] if j == i else 0 for j in range(3)))
        reslice.Update()
        return reslice

    def setup_actors(self):
        actors = []
        for i, renderer in enumerate(self.renderers[:-1]):  # exclude the last renderer for 3D
            mapper = vtk.vtkImageMapToColors()
            mapper.SetInputConnection(self.planes[i].GetOutputPort())
            actor = vtk.vtkImageActor()
            actor.GetMapper().SetInputConnection(mapper.GetOutputPort())
            renderer.AddActor(actor)
            renderer.ResetCamera()
            actors.append(actor)
        self.update_all_views()
        return actors

    def setup_3d_view(self, vtk_image):
        volume = vtk.vtkVolume()
        volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
        volume_mapper.SetInputData(vtk_image)

        volume_property = vtk.vtkVolumeProperty()
        volume_property.SetColor(self.create_volume_color())
        volume_property.SetScalarOpacity(self.create_volume_opacity())

        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)

        self.renderers[-1].AddVolume(volume)  # Add to the last renderer (3D)
        self.renderers[-1].ResetCamera()

    def create_volume_color(self):
        color_func = vtk.vtkColorTransferFunction()
        color_func.AddRGBPoint(0, 0, 0, 0)  # Black
        color_func.AddRGBPoint(255, 1, 1, 1)  # White
        return color_func

    def create_volume_opacity(self):
        opacity_func = vtk.vtkPiecewiseFunction()
        opacity_func.AddPoint(0, 0.0)  # Fully transparent
        opacity_func.AddPoint(255, 1.0)  # Fully opaque
        return opacity_func

    def update_all_views(self):
        for i in range(3):
            self.update_view(i)
        for renderer in self.renderers:
            renderer.GetRenderWindow().Render()

    def update_view(self, view_index):
        if self.image_data is None:
            return
        origin = [0, 0, 0]
        origin[view_index] = self.current_slice[view_index]
        self.planes[view_index].SetResliceAxesOrigin(origin)
        self.planes[view_index].Update()

    def update_window_level(self):
        if self.image_data is None:
            return

        contrast = self.contrast_slider.value() / 100.0
        brightness = self.brightness_slider.value()  # Adjust as necessary

        for i in range(3):
            lut = vtk.vtkLookupTable()
            lut.SetRange(0, 65535)  # Assuming normalized data is in this range
            lut.SetValueRange(0, 1)  # Color range

            for j in range(256):
                # Calculate adjusted value (you can customize this if needed)
                adjusted_value = (j - 128) * (1 + contrast) + brightness + 128
                adjusted_value = max(0, min(255, adjusted_value))  # Clamp to [0, 255]

                # Set the color to white
                if adjusted_value > 128:  # Set bright values to white
                    lut.SetTableValue(j, 1.0, 1.0, 1.0, 1.0)  # White color
                else:
                    lut.SetTableValue(j, 0.0, 0.0, 0.0, 1.0)  # Black for darker values

            lut.Build()
            mapper = vtk.vtkImageMapToColors()
            mapper.SetLookupTable(lut)
            mapper.SetInputConnection(self.planes[i].GetOutputPort())
            self.actors[i].GetMapper().SetInputConnection(mapper.GetOutputPort())

        self.update_all_views()

    def toggle_play(self, checked):
        self.playing = checked
        if checked:
            self.timer.start(100)
        else:
            self.timer.stop()

    def play_slices(self):
        for i in range(3):
            self.current_slice[i] = (self.current_slice[i] + 1) % self.total_slices[i]
            self.sliders[i].setValue(self.current_slice[i])
        self.update_all_views()

    def on_slider_change(self, view_index, value):
        self.current_slice[view_index] = value
        self.update_view(view_index)
        self.update_window_level()  # Ensure the window level is updated if needed

    def on_left_button_press(self, obj, event):
        interactor = obj.GetRenderWindow().GetInteractor()
        interactor.SetInteractorStyle(vtk.vtkInteractorStyleImage())  # Set image style to prevent rotation

        click_pos = interactor.GetEventPosition()
        picker = vtk.vtkPropPicker()
        picker.Pick(click_pos[0], click_pos[1], 0, interactor.GetRenderWindow().GetRenderers().GetFirstRenderer())

        click_position = picker.GetPickPosition()
        if click_position:
            voxel = self.convert_world_to_voxel(click_position)
            if voxel:
                self.marks.append(voxel)
                self.update_marks()

        # Re-enable the default interaction style after handling the click
        interactor.SetInteractorStyle(vtk.vtkInteractorStyleImage())

    # Add this method to ensure interaction style is set properly when initializing
    def setup_interactor_styles(self):
        for vtk_widget in self.vtk_widgets:
            interactor = vtk_widget.GetRenderWindow().GetInteractor()
            interactor.SetInteractorStyle(vtk.vtkInteractorStyleImage())  # Set to prevent rotation

    def get_click_position(self, interactor):
        click_pos = interactor.GetEventPosition()
        picker = vtk.vtkPropPicker()
        picker.Pick(click_pos[0], click_pos[1], 0, interactor.GetRenderWindow().GetRenderers().GetFirstRenderer())
        return picker.GetPickPosition()

    def convert_world_to_voxel(self, pos):
        voxel = [int(round(p)) for p in pos]
        return voxel if all(0 <= v < self.image_data.shape[i] for i, v in enumerate(voxel)) else None

    def update_marks(self):
        for renderer in self.renderers:
            for mark in self.marks:
                sphere = vtk.vtkSphereSource()
                sphere.SetCenter(*mark)
                sphere.SetRadius(2)
                mapper = vtk.vtkPolyDataMapper()
                mapper.SetInputConnection(sphere.GetOutputPort())
                actor = vtk.vtkActor()
                actor.SetMapper(mapper)
                actor.GetProperty().SetColor(1, 0, 0)
                renderer.AddActor(actor)
        for renderer in self.renderers:
            renderer.GetRenderWindow().Render()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MedicalImageViewer()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
