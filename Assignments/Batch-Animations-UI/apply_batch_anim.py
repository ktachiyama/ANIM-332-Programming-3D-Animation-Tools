'''
Krysten Tachiyama

Make sure to add this file to your Maya scripts folder so Maya can find it.

This script bakes an animation onto a given skeleton rig.
To run, call batch_animations() with the appropriate arguments.
'''

import maya.cmds
import os


###############  Helper Functions  ###############


def create_file_namespace(file_path):
    '''
    Takes in a file path and returns the name of
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
    Takes in a file path and the reference's namespace
    and creates a reference to the file
    '''

    if not os.path.exists(file_path):
        maya.cmds.error('File path does not exist: {0}'.format(file_path))
        return

    maya.cmds.file(file_path, r=True, ns=namespace)


# Returns a list of joints from a given namesapce

def get_joints_from_namespace(ns): return maya.cmds.ls(
    '{0}:*'.format(ns), type='joint')


def connect_joints(src_joints_list, dst_joints_list, dst_ns):
    '''
    Makes sure that the destination namespace & names of
    the joints from src_joints_list matches with the joints 
    from dst_joints_list.
    Then connects the joints from src_joints_list onto 
    the joints from dst_joints_list.

        Parameters: 
            src_joints_list (list of strings): A list of joint names from our source file
            dst_joints_list (list of strings): A list of joint names from our destination file
            dst_ns (string): The name of our destination namespace
    '''

    for s in src_joints_list:
        src_joint = s.split(':')[1]
        dst_joint = '{}:{}'.format(dst_ns, src_joint)

        if dst_joint in dst_joints_list:
            maya.cmds.parentConstraint(s, dst_joint, mo=True)


def save_file(file_path):
    ''' Saves the current scene at the location of file_path'''
    maya.cmds.file(rename=file_path)
    maya.cmds.file(save=True, f=True)


##############  End of Helper Functions  ###############


def apply_animation(rig_path, anim_path, save_dir):
    # Create new scene
    maya.cmds.file(new=True, force=True)

    # Create rig and anim namespace
    rig_ns = create_file_namespace(rig_path)
    anim_ns = create_file_namespace(anim_path)

    # Bring in rig skeleton and animation
    create_reference(rig_path, rig_ns)
    create_reference(anim_path, anim_ns)

    # Grab joints from skeleton and animation
    maya.cmds.select(cl=True)
    rig_joints = get_joints_from_namespace(rig_ns)
    anim_joints = get_joints_from_namespace(anim_ns)

    # We want the current framerate and the referenced
    # animation framerates to match
    first_keyframe = maya.cmds.findKeyframe(anim_joints[0], which="first")
    maya.cmds.playbackOptions(
        animationStartTime=first_keyframe, minTime=first_keyframe)
    maya.cmds.currentTime(first_keyframe)

    # Connect joints from skeleton to animation
    connect_joints(anim_joints, rig_joints, rig_ns)

    # Shake 'n Bake animation bones onto character bones
    start_time = maya.cmds.playbackOptions(q=True, min=True)
    end_time = maya.cmds.playbackOptions(q=True, max=True)

    maya.cmds.select(cl=True)
    maya.cmds.select(rig_joints)
    maya.cmds.bakeResults(simulation=True,
                          time=(start_time, end_time),
                          sampleBy=1,
                          oversamplingRate=1,
                          disableImplicitControl=True,
                          preserveOutsideKeys=True,
                          sparseAnimCurveBake=False,
                          removeBakedAnimFromLayer=False,
                          bakeOnOverrideLayer=False,
                          minimizeRotation=True,
                          controlPoints=False,
                          shape=True)

    # Remove animation reference
    maya.cmds.file(anim_path, rr=True)

    # Save file
    new_filename = os.path.join(save_dir, 'character_{}'.format(anim_ns))

    save_file(new_filename)


def batch_animations(char_location, anim_location, save_dir):
    '''
    Defines the locations of the animations, character rig, and where the 
    applied animations will be saved. Then loops through the folder that 
    contains the animations and sends the animation, rig, and save directory
    to apply_animations() to be applied and saved.
    '''

    anim_files = [os.path.join(anim_location, f) for f in os.listdir(
        anim_location) if (os.path.exists(os.path.join(anim_location, f)) and f.endswith('.ma'))]

    # For each animation file in anim_files, apply the animation to the character and save
    for a in anim_files:
        apply_animation(char_location, a, save_dir)
