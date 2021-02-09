import pymel.core
import os

###############  Helper Functions  ###############


def create_file_namespece(file_path):
    '''
    Creates a namespace based on the given file

        Parameter:
            file_path (string): Path of file that will be used to create the namespace
    '''
    if not os.path.exists(file_path):
        pymel.core.error('File does not exist: {}'.format(file_path))
        return

    file_fullname = os.path.split(file_path)[1]
    file_name = os.path.splitext(file_fullname)[0]
    return file_name


def create_reference(file_path, ns):
    '''
    Creates a reference from a file path and namespace

        Parameters:
            file_path (string): Path containing reference file
            ns (string): Name of reference namespace
    '''
    if not os.path.exists(file_path):
        pymel.core.error('File does not exist: {}'.format(file_path))
        return

    pymel.core.system.createReference(file_path, ns=ns)


def connect_joints(src_list, dst_list):
    '''
    Makes sure that the names of the joints from src_list 
    matches with the names of the joints from dst_list.
    Then connects the joints from src_list onto the joints
    of dst_list

        Parameters:
            src_list (list of strings): List containing joint names of animation
            dst_list (list of strings): List containing joint names of rig
   '''
    for src_joint in src_list:
        s = src_joint.split(":")[1]
        for dstJoint in dst_list:
            d = dstJoint.split(":")[1]
            if s == d:
                pymel.core.animation.parentConstraint(
                    src_joint, dstJoint, mo=True)
                break


##############  End of Helper Functions  ###############


def apply_animation(anim_file, char_file, save_dir):
    '''
    Takes the animation from anim_file and applies it to the character
    rig in char_file. Then saves the applied animation to the folder save_dir

        Parameters: 
            anim_file (string): Path (directory and file) that contains the animation
            char_file (string): Path (directory and file) that contains the character rig is
            save_dir (string): Directory where the applied animations will be saved
    '''
    # create new scene
    pymel.core.newFile(f=1)

    # create char and anim namespace
    char_ns = create_file_namespece(char_file)
    anim_ns = create_file_namespece(anim_file)

    # bring in character
    create_reference(char_file, char_ns)

    # bring in animation
    create_reference(anim_file, anim_ns)

    # Get a list of joints of both the anim and char
    anim_joints = pymel.core.ls('{}:*'.format(anim_ns), type='joint')
    char_joints = pymel.core.ls('{}:*'.format(char_ns), type='joint')

    # We want the current framerate and the referenced
    # animation framerates to match
    first_keyframe = pymel.core.findKeyframe(anim_joints[0], which='first')
    pymel.core.currentTime(first_keyframe)

    # Connect the joints of the animation & the character
    connect_joints(anim_joints, char_joints)

    # Shake 'n Bake animation bones to character bones
    start_time = pymel.core.playbackOptions(q=True, min=True)
    end_time = pymel.core.playbackOptions(q=True, max=True)

    pymel.core.select(cl=True)
    pymel.core.select(char_joints)
    pymel.core.bakeResults(simulation=True,
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

    # remove animation reference
    references = pymel.core.system.getReferences()
    references[anim_ns].remove()

    # Save files
    anim_filename = os.path.split(anim_file)[1]
    renamed_file = os.path.join(
        save_dir, 'characterrr_{}'.format(anim_filename))

    pymel.core.system.renameFile(renamed_file)
    pymel.core.system.saveFile(save=True, f=True)


def batch_animations():
    '''
    Defines the locations of the animations, character rig, and where the 
    applied animations will be saved. Then loops through the folder that 
    contains the animations and sends the animation, rig, and save directory
    to apply_animations() to be applied and saved.
    '''
    # File of character rig
    char_location = 'C:/Users/k_tac/OneDrive/Documents/LMU/ANIM-332-Programming-3D-Animation-Tools/Assignments/MEL-Bake-Animations/character.mb'

    # Location of folder containing all the animations that will be applied to the rig
    anim_location = 'C:/Users/k_tac/OneDrive/Documents/LMU/ANIM-332-Programming-3D-Animation-Tools/Assignments/MEL-Bake-Animations/animations'

    anim_files = [os.path.join(anim_location, f) for f in os.listdir(
        anim_location) if os.path.exists(os.path.join(anim_location, f))]

    # location where the applied animations will be saved
    save_dir = 'C:/Users/k_tac/OneDrive/Documents/LMU/ANIM-332-Programming-3D-Animation-Tools/Assignments/MEL-Bake-Animations/save_here'

    # For each animation file in anim_files, apply the animation to the character and save
    for a in anim_files:
        apply_animation(a, char_location, save_dir)


if __name__ == '__main__':
    batch_animations()
