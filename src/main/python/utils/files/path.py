import os
import utils.files.basics as file_basics

def get_absolute_path(path,dir=False,verbose=False):
    
    if path[-1] == '/':
        path = path[0:-1]
    if not path.startswith("/"):
        root = get_project_path()
        path = f"{root}/{path}"
    if verbose:
        print(f'Getting absolute path of {path}')
    if dir:
        path = path + '/'
    return path

def join_path(*args):
    return os.path.join(*args)

def get_sub_folders(folder_path, path=True, verbose=False):
    folder_path = get_absolute_path(folder_path)
    if verbose:
        print(f'Getting sub folders in {folder_path}')
    folders = get_folders(folder_path)
    if path:
        return [join_path(folder_path, f) for f in folders]
    return folders

def get_parent_folders(files_path, path=True, verbose=False):
    folders= []
    for input_file_path in files_path:
        folder = get_parent_folder_path(input_file_path)
        if folder not in folders:
            folders.append(folder)
    return folders

def get_parent_folder(file_path, path=True, verbose=False):
    file_path = get_absolute_path(file_path)
    if verbose:
        print(f'Getting parent folder in {file_path}')
    parent_folder = get_parent_folder_path(file_path)
    if path:
        return parent_folder
    return get_folder_name(parent_folder)

def get_parent_folder_path(file_path):
    file_path = get_absolute_path(file_path)
    if file_path[-1] == '/':
        file_path = file_path[0:-1]
    parent_path = '/'.join(file_path.split('/')[0:-1])
    return parent_path


def get_file_name(file_path, extension=True):
    file_path = get_absolute_path(file_path)
    if extension:
        return file_path.split('/')[-1]
    else:
        return file_path.split('/')[-1].split('.')[0]
    
def get_folder_name(folder_path):
    folder_path = get_absolute_path(folder_path)
    return folder_path.split('/')[-1]

def get_list(folder):
    return os.listdir(folder)

def get_files(folder):
    return [f for f in get_list(folder) if os.path.isfile(os.path.join(folder, f))]

def get_folders(folders, path=False, verbose=False):
    if type(folders) != list:
        folders = [folders]
    if verbose:
        print(f'Getting all folders in {folders}')
    if not path:
        return [f for folder in folders for f in get_list(folder) if os.path.isdir(os.path.join(folder, f))]
    return [join_path(folder, f) for folder in folders for f in get_list(folder) if os.path.isdir(os.path.join(folder, f))]

def get_all_files(folder_path, path=True, verbose=False):
    if verbose:
        print(f'Getting all files in {folder_path}')
    return file_basics.get_files(folder_path)

def get_project_path():
    current_file_path = os.path.abspath(__file__)
    if 'src' in current_file_path:
        return '/'.join(current_file_path.split('src')[0].split('/')[0:-1])
    if 'code' in current_file_path:
        return '/'.join(current_file_path.split('code')[0].split('/')[0:-1])
    