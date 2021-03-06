'''
Krysten Tachiyama

This script provides the user with a User Interface tool that
allows them to batch a series of animation files onto a character
rig and save the connected animations to a specified directory.

Make sure the file apply_batch_animations_MEL is added to your
Maya scripts so the file can be properly imported. Then, run this
code inside of Maya:

try:
        dialog.close()
        dialog.deleteLater()
except:
    pass

dialog = batch_animations_UI.BatchAnimDialog()
dialog.show()
'''

from apply_batch_animations_MEL import batch_animations
from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI
import os


def get_maya_window():

    maya_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()

    # converts a pointer to  a long and then
    # creates an instance of it that's a QWidget
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)


class BatchAnimDialog(QtWidgets.QDialog):

    # constructor
    def __init__(self):

        # get maya window
        maya_main = get_maya_window()

        # parent dialog to parent window
        super(BatchAnimDialog, self).__init__(maya_main)

        # Set title, height, and width of UI box
        self.setWindowTitle('Batch Animation Onto Character')
        self.setMinimumHeight(400)
        self.setMinimumWidth(700)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # get character file
        self.char_file_text = QtWidgets.QLabel()
        self.char_file_text.setText('Character File Path')

        self.char_file_input = QtWidgets.QLineEdit()
        self.char_file_input_btn = QtWidgets.QPushButton()
        self.char_file_input_btn.setIcon(QtGui.QIcon(':fileOpen.png'))

        # get animation folder
        self.anim_file_text = QtWidgets.QLabel()
        self.anim_file_text.setText('Animations Directory')

        self.anim_file_input = QtWidgets.QLineEdit()
        self.anim_file_input_btn = QtWidgets.QPushButton()
        self.anim_file_input_btn.setIcon(QtGui.QIcon(':fileOpen.png'))

        # get save directory
        self.save_file_text = QtWidgets.QLabel()
        self.save_file_text.setText('Save Directory')

        self.save_file_input = QtWidgets.QLineEdit()
        self.save_file_input_btn = QtWidgets.QPushButton()
        self.save_file_input_btn.setIcon(QtGui.QIcon(':fileOpen.png'))

        # create buttons
        self.batch_btn = QtWidgets.QPushButton('Batch')
        self.cancel_btn = QtWidgets.QPushButton('Cancel')

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # character file input layout
        self.char_layout = QtWidgets.QHBoxLayout(self)
        self.char_layout.addWidget(self.char_file_text)
        self.char_layout.addWidget(self.char_file_input)
        self.char_layout.addWidget(self.char_file_input_btn)

        # animation directory input layout
        self.anim_layout = QtWidgets.QHBoxLayout(self)
        self.anim_layout.addWidget(self.anim_file_text)
        self.anim_layout.addWidget(self.anim_file_input)
        self.anim_layout.addWidget(self.anim_file_input_btn)

        # save directory input layout
        self.save_layout = QtWidgets.QHBoxLayout(self)
        self.save_layout.addWidget(self.save_file_text)
        self.save_layout.addWidget(self.save_file_input)
        self.save_layout.addWidget(self.save_file_input_btn)

        # buttons layout
        self.btn_layout = QtWidgets.QHBoxLayout(self)
        self.btn_layout.addWidget(self.batch_btn)
        self.btn_layout.addWidget(self.cancel_btn)

        # add all layouts to main window
        self.main_layout.addLayout(self.char_layout)
        self.main_layout.addLayout(self.anim_layout)
        self.main_layout.addLayout(self.save_layout)
        self.main_layout.addLayout(self.btn_layout)

    def browse_char_path(self):
        path = QtWidgets.QFileDialog.getOpenFileName(
            self, self.tr("Select File"), "", self.tr("Maya Binary (*.mb);;Maya (*.ma *.mb);;Maya ASCII (*.ma);;All Files(*.*)"))[0]
        if path:
            self.char_file_input.setText(path)

    def browse_anim_dir(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self)
        if path:
            self.anim_file_input.setText(path)

    def browse_save_dir(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self)
        if path:
            self.save_file_input.setText(path)

    # connect buttons to actions
    def create_connections(self):
        self.char_file_input_btn.clicked.connect(self.browse_char_path)
        self.anim_file_input_btn.clicked.connect(self.browse_anim_dir)
        self.save_file_input_btn.clicked.connect(self.browse_save_dir)

        self.batch_btn.clicked.connect(self.execute_batch)
        self.cancel_btn.clicked.connect(self.close)

    # checks that all inputs are valid and then executes batching
    def execute_batch(self):

        char_file = self.char_file_input.text()
        anim_dir = self.anim_file_input.text()
        save_dir = self.save_file_input.text()

        # Make sure user inputs are valid
        if not char_file or not anim_dir or not save_dir:
            QtWidgets.QMessageBox.warning(
                self, "ERROR: All inputs are required")
            return

        if not os.path.exists(char_file):
            QtWidgets.QMessageBox.warning(
                self, "ERROR: Character file does not exist: {}".format(char_file))
            return

        if not os.path.exists(anim_dir):
            QtWidgets.QMessageBox.warning(
                self, "ERROR: Directory does not exist: {}".format(anim_dir))
            return

        if not os.path.exists(save_dir):
            QtWidgets.QMessageBox.warning(
                self, "ERROR: Directory does not exist: {}".format(save_dir))
            return

        # If all inputs are valid, go ahead and batch animations
        self.close()
        batch_animations(char_file, anim_dir, save_dir)
