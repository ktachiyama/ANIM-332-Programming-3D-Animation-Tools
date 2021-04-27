import unreal
import os
from difflib import SequenceMatcher

'''
run these commands in ue4 outlook to reimport script without restarting unreal

from importlib import reload
import asset_importer
reload(asset_importer)
'''
 
def asset_data(filename='', destination='', options=None):
    ''' 
    Defines the data for the assets being imported 
    
    Parameters:
        filename (string): Path of folder containing the asset files
        destination (string): Path of where the assets will be imported
        options (object): Import options for the asset

    Returns:
        Object contining data for that assets being imported
    ''' 

    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('destination_path', destination)
    task.set_editor_property('filename', filename)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)
    task.set_editor_property('options', options)

    return task


def create_directory_if_no_exist(path):
    ''' 
    Checks if path exist, creates it if it doesn't

    Parameter:
        path (string): Directory path
    '''

    if not directory_exists(path):
        return unreal.EditorAssetLibrary.make_directory(directory_path=path)


def create_material_to_path_dic(materials_path_list):
    '''
    Creates a dictionary of material name keys to their corresponding path values
    i.e: {(material name : path to material)}

    Parameter:
        materials_path_list (list of strings): List containing all of the paths to material assets

    Returns:
        Dictionary of material names to paths
    '''
    result = dict()

    for m in materials_path_list:
        mat_name = m.split('/')[-1]
        result.update([(mat_name, m)])

    return result


def directory_exists(path):
    ''' 
    Returns True if path exists, False otherwise

    Paramteter:
        path (string): Directory path
    '''

    return unreal.EditorAssetLibrary.does_directory_exist(directory_path=path)


def execute_import_tasks_and_get_import_paths(tasks=[]):
    '''
    Imports assets into the project 

    Parameter:
        tasks (list): List of objects containing the data needed to import assets into the project

    Returns:
        A list containing the paths to the imported assets
    '''
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    imported_asset_paths = []
    for task in tasks:
        for path in task.get_editor_property('imported_object_paths'):
            imported_asset_paths.append(path)
    return imported_asset_paths


def get_fbx_from_folder(folder_path):
    ''' 
    Creates a list of fbx file paths from the given folder_path 

    Parameter:
        folder_path (string): path to folder containing the fbx files 

    Returns:
        a list of fbx files in folder_path
    '''

    fbx_files = [os.path.join(folder_path, f) for f in os.listdir(
        folder_path) if (os.path.exists(os.path.join(folder_path, f)) and f.endswith('.fbx'))]

    return fbx_files


def replace_meshes(asset_path_list, matName_to_path, set_to_closest_mat):
    '''
    Goes through asset_path_list to grab each asset's material slots and replaces them with 
    existing materials that match the slot names. 

    If a slot name does not match any existing mateials
        - If set_to_closest_mat is True, the program will find the closest-named material above a
            0.6 threshhold and set it to that slot
        - If set_to_closest_mat is False, then the material slot won't be changed

    Parameters:
        asset_path_list (list of strings): List of paths to assets
        matName_to_path (dictorionary): Dictionary mapping material names to their corresponding location in the project
        set_to_closest_mat (bool): True if we want to match nonexisting materials to their closest match, False otherwise 
    '''

    if(set_to_closest_mat):
        # get a list of material names from the matName_to_path dictionary
        mat_names = matName_to_path.keys()

    for asset_path in asset_path_list:
        
        # grab static mesh from asset_path
        asset = unreal.EditorAssetLibrary.load_asset(asset_path)
        
        # get material data from mesh
        material_data = asset.static_materials
        
        index = 0

        for m in material_data:
            materials_path = None
            slot_name = m.material_slot_name

            if(set_to_closest_mat == True):
                # initialize dictionary
                score_to_name = dict()

                # create the dictionary with score keys and material name values
                # { score : name, ... , score : name }
                for n in mat_names:
                    score = SequenceMatcher(None, str(slot_name), n).ratio()
                    score_to_name.update([(score, n)])

                best_score = max(sorted(score_to_name))
                
                # if the best score is similar enough, get its associated 
                # material name and path
                if(best_score > 0.6):
                    mat = score_to_name.get(best_score)
                    materials_path = matName_to_path.get(mat)

            else:
                # find path of material matching slot name
                # if there is no match, material_path will be set to None
                materials_path = matName_to_path.get(str(slot_name))

            if (materials_path is not None) and unreal.EditorAssetLibrary.does_asset_exist(materials_path):
                # load material asset and set it to mesh
                mat = unreal.EditorAssetLibrary.load_asset(materials_path)
                asset.set_material(index, mat)

            index += 1


def static_mesh_import_options(import_materials_and_textures):
    '''
    Sets the import options for the static mesh assets

    Parameter:
        import_materials_and_textures (bool): True if we want to import the materials/textures from the assets, False otherwise 

    Returns:
        Object containing data for the import options
    '''
    options = unreal.FbxImportUI()

    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', import_materials_and_textures)
    options.set_editor_property('import_materials', import_materials_and_textures)
    options.set_editor_property('import_as_skeletal', False)

    options.static_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)

    options.static_mesh_import_data.set_editor_property('combine_meshes', False)
    options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)

    return options


'''
    def skeletal_mesh_import_options():
        options = unreal.FbxImportUI()

        options.set_editor_property('import_mesh', True)
        options.set_editor_property('import_textures', False)
        options.set_editor_property('import_materials', False)
        options.set_editor_property('import_as_skeletal', True)  # Skeletal Mesh

        options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)

        return options
'''


def import_assets(fbx_directory, save_directory, materials_path_list, set_to_closest_mat, import_materials_and_textures):
    '''
    This function is the main driver for importing the assets and setting the materials

    Parameters:
        fbx_directory (Directory object): Object containing the path of fbx files
        save_directory (Directory object): Object containing the path to where assets will be imported
        materials_path_list (list of strings): List of all the paths to every material in form /path/material_name
        set_to_closest_mat (bool): True if we want to match nonexisting materials to their closest match, False otherwise
        import_materials_and_textures (bool): True if we want to import the materials/textures from the assets, False otherwise 
    '''

    assets = []

    # Must get paths (in string form) from directory objects
    fbx_dir_path = fbx_directory.path
    save_dir_path = save_directory.path

    # create the dictionary of materials to paths
    matName_to_path = create_material_to_path_dic(materials_path_list)

    # creates the directory if it doesnt yet exist
    create_directory_if_no_exist(save_dir_path)

    # get all fbx files from fbx_directory
    fbx_paths = get_fbx_from_folder(fbx_dir_path)

    # with these fbx files, create a list of necessary data to import each asset
    for f in fbx_paths:
        assets.append(asset_data(f, save_dir_path, static_mesh_import_options(import_materials_and_textures)))
    
    # import the assets and get a list of their paths in the project
    imported_asset_paths = execute_import_tasks_and_get_import_paths(assets)
    
    # replace the newly imported asset materials with already existing ones
    replace_meshes(imported_asset_paths, matName_to_path, set_to_closest_mat)
