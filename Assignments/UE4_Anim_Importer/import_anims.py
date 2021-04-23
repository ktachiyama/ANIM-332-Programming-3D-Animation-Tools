import unreal
import os

def get_inputs_from_folder(shot_folder, skeleton, destination_path):
    # creates a list of fbx files from the given shot_folder
    anim_files = [os.path.join(shot_folder, f) for f in os.listdir(
        shot_folder) if (os.path.exists(os.path.join(shot_folder, f)) and f.endswith('.fbx'))]
    
    # for each file in anim_files, import the animation
    for a in anim_files:
        import_skeletal_animations(skeleton, a, destination_path)


def import_skeletal_animations(skeleton, input_path, destination_path):

    # setting animation section options

    anim_seq_import_data = unreal.FbxAnimSequenceImportData()
    anim_seq_import_data.set_editor_property("animation_length", unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    anim_seq_import_data.set_editor_property("convert_scene", True)
    anim_seq_import_data.set_editor_property("use_default_sample_rate", True)
    anim_seq_import_data.set_editor_property("import_bone_tracks", True)
    anim_seq_import_data.set_editor_property("import_meshes_in_bone_hierarchy", False)
    anim_seq_import_data.set_editor_property("import_custom_attribute", False)
    anim_seq_import_data.set_editor_property("remove_redundant_keys", False)

    # setting import options

    ui_import_options = unreal.FbxImportUI()
    ui_import_options.reset_to_default()
    ui_import_options.set_editor_property("automated_import_should_detect_type", False)
    ui_import_options.set_editor_property("create_physics_asset", False)
    ui_import_options.set_editor_property("import_animations", True)
    ui_import_options.set_editor_property("import_as_skeletal", False)
    ui_import_options.set_editor_property("import_materials", False)
    ui_import_options.set_editor_property("import_mesh", False)
    ui_import_options.set_editor_property("import_rigid_mesh", False)
    ui_import_options.set_editor_property("import_textures", False)
    ui_import_options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
    ui_import_options.set_editor_property("skeleton", skeleton)
    ui_import_options.set_editor_property("anim_sequence_import_data", anim_seq_import_data)

    # import animation w/ option, input path, and destination path

    asset_import_task = unreal.AssetImportTask()
    asset_import_task.set_editor_property("automated", True)
    asset_import_task.set_editor_property("destination_path", destination_path)
    asset_import_task.set_editor_property("filename", input_path)
    asset_import_task.set_editor_property("options", ui_import_options)
    asset_import_task.set_editor_property("save", True)

    tasks = [asset_import_task]

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    unreal.AssetTools.import_asset_tasks(asset_tools, tasks)

'''
Attempted challenge #1, didn't quite get there


def get_or_add_possessable_in_sequence_asset(sequence_path, actor):
    sequence_asset = unreal.LevelSequence.cast(unreal.load_asset(sequence_path))
    possessable = sequence_asset.add_possessable(object_to_possess=actor)
    return possessable

def add_skeletal_animation_track_on_possessable(animation_path, possessable):
    # Get Animation
    animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animation_path))
    params = unreal.MovieSceneSkeletalAnimationParams()
    params.set_editor_property('Animation', animation_asset)
    # Add track
    animation_track = possessable.add_track(track_type=unreal.MovieSceneSkeletalAnimationTrack)
    # Add section
    animation_section = animation_track.add_section()
    animation_section.set_editor_property('Params', params)
    animation_section.set_range(0, animation_asset.get_editor_property('sequence_length'))


def add_skeletal_animation_track_on_actor():
    sequence_path = '/ktach_wk10_anim_importer/test_seq'
    animation_path = '/Game/Animations/SKP_0240_Character'
    actor_in_world =  unreal.EditorLevelLibrary().get_actor_reference('/wk10_sample_content/character')
    possessable_in_sequence = get_or_add_possessable_in_sequence_asset(sequence_path, actor_in_world)
    add_skeletal_animation_track_on_possessable(animation_path, possessable_in_sequence)
'''