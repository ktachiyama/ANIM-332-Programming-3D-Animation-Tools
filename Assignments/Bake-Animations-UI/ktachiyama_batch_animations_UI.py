from apply_batch_anim import batch_animations
from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI


def get_maya_window():

    maya_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()

    # converts a pointer to  a long and then
    # creates an instance of it that's a QWidget
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)


class BatchAnimDialogue(QtWidgets.QDialog):

    # constructor
    def __init__(self):

        # get maya window
        maya_main = get_maya_window()

        # parent dialog to parent window
        super(BatchAnimDialogue, self).__init__(maya_main)

        # Set title, height, and width of UI box
        self.setWindowTitle('Batch Animation Onto Character')
        self.setMinimumHeight(400)
        self.setMinimumWidth(1000)

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

        # create button
        self.batch_btn = QtWidgets.QPushButton('Batch')

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.char_layout = QtWidgets.QHBoxLayout(self)
        self.char_layout.addWidget(self.char_file_text)
        self.char_layout.addWidget(self.char_file_input)
        self.char_layout.addWidget(self.char_file_input_btn)

        self.anim_layout = QtWidgets.QHBoxLayout(self)
        self.anim_layout.addWidget(self.anim_file_text)
        self.anim_layout.addWidget(self.anim_file_input)
        self.anim_layout.addWidget(self.anim_file_input_btn)

        self.save_layout = QtWidgets.QHBoxLayout(self)
        self.save_layout.addWidget(self.save_file_text)
        self.save_layout.addWidget(self.save_file_input)
        self.save_layout.addWidget(self.save_file_input_btn)

        self.btn_layout = QtWidgets.QHBoxLayout(self)
        self.btn_layout.addWidget(self.batch_btn)

        self.main_layout.addLayout(self.char_layout)
        self.main_layout.addLayout(self.anim_layout)
        self.main_layout.addLayout(self.save_layout)
        self.main_layout.addLayout(self.btn_layout)

    def browse_char_path(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self)[0]
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

    def batch_animation(self):
        char_dir = self.char_file_input.text()
        anim_dir = self.anim_file_input.text()
        save_dir = self.save_file_input.text()

        batch_animations(char_dir, anim_dir, save_dir)
        self.close()

    def create_connections(self):
        self.char_file_input_btn.clicked.connect(self.browse_char_path)
        self.anim_file_input_btn.clicked.connect(self.browse_anim_dir)
        self.save_file_input_btn.clicked.connect(self.browse_save_dir)

        self.batch_btn.clicked.connect(self.batch_animation)


if __name__ == '__main__':
    try:
        dialog.close()
        dialog.deleteLater()
    except:
        pass

    dialog = BatchAnimDialogue()
    dialog.show()
