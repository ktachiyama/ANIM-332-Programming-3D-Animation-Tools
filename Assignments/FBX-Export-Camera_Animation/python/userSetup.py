'''
Krysten Tachiyama

This user setup adds a dropdown menu to the Maya menu bar. Clicking on
the menu calls the ktachiyama_fbx_export_camera file and instantiates a UI.
'''

import sys
import inspect
import maya.OpenMayaUI


def create_custom_menu():

    # setup menu
    menu_name = "fbx_export_camera"

    maya.cmds.menu(menu_name, label="Export Camera as FBX",
                   parent="MayaWindow", tearOff=True)

    maya.cmds.menuItem(parent=menu_name, divider=True)

    maya.cmds.menuItem(parent=menu_name,
                       label="Export Camera as FBX",
                       command=export_camera,
                       annotation="Export camera to FBX file")


def export_camera(*args):

    # import file into Maya and instantiate UI
    import fbx_export_camera_UI
    fbx_export_camera_UI.ExportFBXCameraDialog.show_dialog()


maya.cmds.evalDeferred("create_custom_menu()")
