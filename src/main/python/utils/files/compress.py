import utils.files.path as path_utils
import utils.files.basics as basics_utils
import utils.files.check as check_utils

import os

def zip(input_path, dir=False, verbose=True):
    if dir:
        return zip_dir(input_path,verbose)
    return zip_file(input_path, verbose)

def zip_file(input_file_path, verbose=True):
    input_file_path = path_utils.get_absolute_path(input_file_path)
    if not check_utils.exists(input_file_path):
        print(f"{input_file_path} does not exist...")
        return
    if input_file_path.endswith(".zip"):
        print(f"{input_file_path} is already a zip file...")
        return input_file_path
    if verbose:
        print(f'Zipping {input_file_path}')
    os.system(f"cd {path_utils.get_parent_folder(input_file_path,path=True)} && zip -r {path_utils.get_file_name(input_file_path).split('.')[0]}.zip {path_utils.get_file_name(input_file_path)}")
    return f"{path_utils.get_parent_folder(input_file_path,path=True)}/{path_utils.get_file_name(input_file_path)}.zip"

def zip_dir(output_dir, verbose=False):
    dir_name = os.path.basename(output_dir)
    files = basics_utils.get_files(output_dir)
    if verbose:
        print(f'Zipping {files} to {dir_name}.zip')
    os.system(f'cd {output_dir} && zip -r {dir_name}.zip {' '.join(files)}')
    return f'{output_dir}/{dir_name}.zip'


def unzip(input_path, dir=False, verbose=True):
    if dir:
        return unzip_dir(input_path,verbose)
    return unzip_file(input_path, verbose)

def unzip_file(input_file_path, verbose=True):
    input_file_path = path_utils.get_absolute_path(input_file_path)
    if not check_utils.exists(input_file_path):
        print(f"{input_file_path} does not exist...")
        return
    if not input_file_path.endswith(".zip"):
        print(f"{input_file_path} is not a zip file...")
        return input_file_path
    if verbose:
        print(f'Unzipping {input_file_path}')
    os.system(f"cd {path_utils.get_parent_folder(input_file_path,path=True)} && unzip {input_file_path}")
    return f"{path_utils.get_parent_folder(input_file_path,path=True)}/{path_utils.get_file_name(input_file_path).split('.')[0]}"

def unzip_dir(input_dir, verbose=False):
    dir_name = os.path.basename(input_dir)
    if verbose:
        print(f'Unzipping {dir_name}.zip to {input_dir}')
    os.system(f'cd {input_dir} && unzip {dir_name}.zip')
    return f'{input_dir}/{dir_name}'

