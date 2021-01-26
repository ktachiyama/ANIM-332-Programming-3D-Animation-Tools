'''
Krysten Tachiyama


'''

import maya.cmds
import os


def create_file_namespace(file_path):
    '''
    takes in a file path and returns the name of
    the file as the namespace
    '''

    if not os.path.exists(file_path):
        maya.cmds.error('File does not exist: {0}'.format(file_path))
        return

    file_name = os.path.split(file_path)[1]
    namespace = os.path.splitext(file_name)[0]

    return namespace


def create_reference(file_path, namespace):
    '''
    takes in a file path and the reference's namespace
    and creates a reference to the file
    '''

    if not os.path.exists(file_path):
        maya.cmds.error('File path does not exist: {0}'.format(file_path))
        return

    maya.cmds.file(file_path, r=True, ns=namespace)


# returns joints from a given namesapce

get_joints_from_namespace = lambda ns: maya.cmds.ls('{0}:*'.format(ns), type='joint')


def connect_anim(src, dst, src_ns, dst_ns):
    diff_list = get_namespace_diff_list(src, dst)
    for src_transform in src:
        if src_transform.split(":")[-1] in diff_list:
            continue
        dst_transform = src_transform.replace(src_ns, dst_ns)
        if not maya.cmds.objExists(dst_transform):
            continue
        maya.cmds.parentConstraint(src_transform, dst_transform, mo = True)


def batch_animation(rig_path, anim_path, destination_path):
    # create new scene
    maya.cmds.file(new=True, force=True)

    # create rig and anim namespace
    rig_ns = create_file_namespace(rig_path)
    anim_ns = create_file_namespace(anim_path)

    # bring in rig skeleton and animation
    create_reference(rig_path, rig_ns)
    create_reference(anim_path, anim_ns)

    # grab joints from skeleton and animation
    maya.cmds.select(cl = True)
    rig_joints = get_joints_from_namespace(rig_ns)
    anim_joints = get_joints_from_namespace(anim_ns)


    # We want the current framerate and the referenced
    # animation framerates to match
    first_keyframe = maya.cmds.findKeyframe(anim_joints[0], which="first")
    maya.cmds.playbackOptions(animationStartTime=first_keyframe, minTime=first_keyframe)
    maya.cmds.currentTime(first_keyframe)

    # connect joints from skeleton to animation
    connect_joints(anim_joints, rig_joints, rig_ns)

    # Shake 'n Bake animation bones to character bones
    start_time = maya.cmds.playbackOptions(q=True, min=True)
    end_time = maya.cmds.playbackOptions(q=True, max=True)   
    
    maya.cmds.select(cl=True)
    maya.cmds.select(rig_joints)
    maya.cmds.bakeResults(simulation = True,
                        time = (start_time, end_time),
                        sampleBy = 1,
                        oversamplingRate= 1,
                        disableImplicitControl = True,
                        preserveOutsideKeys = True,
                        sparseAnimCurveBake = False,
                        removeBakedAnimFromLayer = False,
                        bakeOnOverrideLayer = False,
                        minimizeRotation = True,
                        controlPoints = False,
                        shape = True)
    
    # Remove animation reference
    maya.cmds.file(anim_path, rr=True)

                        

if __name__ == '__main__':
    rig_path = r'C:\Users\k_tac\OneDrive\Documents\LMU\ANIM-332-Programming-3D-Animation-Tools\Assignments\Bake-Animations\files\character.mb'.replace(
        '\\', '/')
    anim_path = r'C:\Users\k_tac\OneDrive\Documents\LMU\ANIM-332-Programming-3D-Animation-Tools\Assignments\Bake-Animations\files\animations\char_01_01.ma'.replace(
        '\\', '/')
    destination_path = r'C:\Users\k_tac\OneDrive\Documents\LMU\ANIM-332-Programming-3D-Animation-Tools\Assignments\Bake-Animations\save_here'.replace(
        '\\', '/')

    batch_animation(rig_path, anim_path, destination_path)
    