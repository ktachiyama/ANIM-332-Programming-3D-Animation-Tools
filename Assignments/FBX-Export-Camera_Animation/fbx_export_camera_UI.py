'''
Krysten Tachiyama

This script provides a UI that allows a user to export a camera
as a fbx file in the desired path. 

Make sure this file is properly imported to your Maya scripts.
Then, run this code inside of Maya:

try:
    dialog.close()
    dialog.deleteLater()
except:
    pass

dialog = fbx_export_camera_UI.ExportFBXCameraDialog()
dialog.show()

'''
import pymel.core
from PySide2 import QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI


def get_maya_window():
    maya_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()

    # converts a pointer to  a long and then
    # creates an instance of it that's a QWidget

    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)


def export_fbx_cam_anim(filename):
    # export selected camera as fbx to filename

    pymel.core.loadPlugin("fbxmaya.mll", quiet=True)
    pymel.core.mel.FBXResetExport()
    pymel.core.mel.FBXExportInAscii(v=True)
    pymel.core.mel.FBXExportUpAxis("y")
    pymel.core.mel.FBXExportAnimationOnly(v=False)
    pymel.core.mel.FBXExportCameras(v=True)
    pymel.core.mel.FBXExport(s=True, f=filename)


def export_selected_cam_anim(camera, filename):
    # selects camera and tries to call export_fbx_cam_anim()
    # if funciton cannot be called, throw error

    pymel.core.select(camera, r=True)
    try:
        export_fbx_cam_anim(filename)
    except:
        QtWidgets.QMessageBox.critical(
            get_maya_window(), "ERROR", "Something went wrong, cannot export camera")


class ExportFBXCameraDialog(QtWidgets.QDialog):

    dlg_instance = None

    # ensures that there is only 1 instance of the ExportFBXCameraDialog
    # at a time. Also allows UI to come to front if its behind another object

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = ExportFBXCameraDialog()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()

        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow

    def __init__(self):
        # get maya window
        maya_main = get_maya_window()

        # parent dialog to parent window
        super(ExportFBXCameraDialog, self).__init__(maya_main)

        # set title, height, and width of UI box
        self.setWindowTitle("Export Camera to FBX")
        self.setMinimumHeight(200)
        self.setMinimumWidth(700)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # initialize camera input label and button
        self.cam_text = QtWidgets.QLabel("      Camera      ")
        self.cam_line_edit = QtWidgets.QLineEdit()
        self.cam_browse_btn = QtWidgets.QPushButton("<<")

        # initialize save path input label and button
        self.exported_file_text = QtWidgets.QLabel(" Save Filename")
        self.exported_file_line_edit = QtWidgets.QLineEdit()
        self.exported_file_browse_btn = QtWidgets.QPushButton()
        self.exported_file_browse_btn.setIcon(QtGui.QIcon(":fileOpen.png"))

        # initialize run, reset, and cnacel buttons
        self.run_btn = QtWidgets.QPushButton("Run")
        self.reset_btn = QtWidgets.QPushButton("Reset")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        # make camera and save path inputs are read-only
        self.cam_line_edit.setReadOnly(True)
        self.exported_file_line_edit.setReadOnly(True)

        # make sure the browse buttons are not scalable
        self.cam_browse_btn.setMaximumWidth(50)
        self.exported_file_browse_btn.setMaximumWidth(50)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # camera input layout
        self.cam_layout = QtWidgets.QHBoxLayout(self)
        self.cam_layout.addWidget(self.cam_text)
        self.cam_layout.addWidget(self.cam_line_edit)
        self.cam_layout.addWidget(self.cam_browse_btn)

        # save directory layout
        self.save_layout = QtWidgets.QHBoxLayout(self)
        self.save_layout.addWidget(self.exported_file_text)
        self.save_layout.addWidget(self.exported_file_line_edit)
        self.save_layout.addWidget(self.exported_file_browse_btn)

        # run, reset, and cancel button layout
        self.btn_layout = QtWidgets.QHBoxLayout(self)
        self.btn_layout.addWidget(self.run_btn)
        self.btn_layout.addWidget(self.reset_btn)
        self.btn_layout.addWidget(self.cancel_btn)

        # main layout
        self.main_layout.addLayout(self.cam_layout)
        self.main_layout.addLayout(self.save_layout)
        self.main_layout.addLayout(self.btn_layout)

    def create_connections(self):
        # connect buttons to actions

        self.cam_browse_btn.clicked.connect(self.get_selected_object)

        self.exported_file_browse_btn.clicked.connect(
            self.exported_file_browse)

        self.run_btn.clicked.connect(self.export_camera)

        self.reset_btn.clicked.connect(self.clear_text)

        self.cancel_btn.clicked.connect(self.close)

    def clear_text(self):
        # clear the camera and save path inputs
        self.cam_line_edit.setText("")
        self.exported_file_line_edit.setText("")

    def exported_file_browse(self):
        # only .fbx files can be exported
        exported_file = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save as...", None, "FBX Files (*.fbx)")

        # try to set save path input, throw error if invalid
        try:
            self.exported_file_line_edit.setText(exported_file[0])
        except:
            QtWidgets.QMessageBox.critical(get_maya_window(
            ), "File error", "Path input was invalid, select a valid filepath")

    def close(self):
        # close dialog
        super(ExportFBXCameraDialog, self).close()

    def get_selected_object(self):

        # get list of selected objects
        selected_list = pymel.core.selected()

        # if no objects were selected, throw an error
        if len(selected_list) == 0:
            QtWidgets.QMessageBox.critical(
                get_maya_window(), "Selection Error", "Nothing was selected")
            return

        # if multiple objects were selected, throw an error
        elif len(selected_list) > 1:
            QtWidgets.QMessageBox.critical(
                get_maya_window(), "Selection Error", "Please select a single camera or transform with a camera shape")
            return

        # get selected object
        selected = selected_list[0]

        camera_shape = None

        # from the selected object, get the top level transform
        transform = selected.getParent() if (
            selected.getParent() is not None) else selected

        # get the first camera shape child of the transform if it exists
        child_list = transform.getChildren()
        for child in child_list:
            if(pymel.core.objectType(child, isType='camera')):
                camera_shape = child
                break

        # if a camera shape child exists, assign its transform name as the camera input.
        # if no camera shape exists, throw error
        if camera_shape is None:
            QtWidgets.QMessageBox.critical(get_maya_window(
            ), "Node Type Error", "Selected Item was neither a camera or a transform with a camera shape.")

        else:
            self.cam_line_edit.setText(str(transform))

    def export_camera(self):

        # Throw error if either camera or save path inputs are not filled
        if not self.cam_line_edit.text() or not self.exported_file_line_edit.text():
            QtWidgets.QMessageBox.critical(
                get_maya_window(), "Input Error", "Please input all feilds")
            return

        cam_name = self.cam_line_edit.text()
        exported_file = self.exported_file_line_edit.text()

        # export camera
        export_selected_cam_anim(cam_name, exported_file)

        # clear inputs and close dialog
        self.clear_text()
        self.close()
