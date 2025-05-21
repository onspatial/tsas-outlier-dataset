import os
import utils.files.check as file_check
import utils.files.path as path_utils
import utils.sync as sync_utils

def clean_up(folder, dir=True, trash=True):
    if file_check.exists(folder,dir=True):
        remove(folder,dir=dir,trash=trash,verbose=False)

def clone(src, dest, files=False, verbose=True):
    if files:
        return clone_files(src, dest, verbose)
    elif not files:
        return clone_folders(src, dest, verbose)
    else:
        raise Exception('Exception: files parameter must be a boolean')

def clone_folders(src, dest, verbose=False):
    if type(src) is list:
        for s in src:
            clone(s, dest, verbose)
        return dest
    if type(dest) is list:
        for d in dest:
            clone(src, d, verbose)
        return dest
    if verbose:
        print(f'Cloning {src} to {dest}')
    return copy(src, dest, verbose)

def clone_files(src, dest, verbose=False):
    if type(src) is list:
        for s in src:
            clone_files(s, dest, verbose)
        return dest
    if type(dest) is list:
        for d in dest:
            clone_files(src, d, verbose)
        return dest
    if verbose:
        print(f'Cloning files from {src} to {dest}')
    files = get_files(src,path=False,verbose=verbose)
    for file in files:
        copy(f'{src}/{file}', f'{dest}/{file}', verbose)
    return dest

def copy(src, dest, verbose=False):
    src = path_utils.get_absolute_path(src)
    if not file_check.exists(src):
        raise Exception(f'Exception: {src} does not exist')
    if verbose:
       print(f'Copying {src} to {dest}')
    os.system('mkdir -p ' + os.path.dirname(dest))
    if os.path.isdir(src):
        if verbose:
            print(f'Copying directory {src} to {dest}')
        os.system(f'cp -r "{src}" "{dest}"')
    else:
        if verbose:
            print(f'Copying file {src} to {dest}')
        os.system(f'cp "{src}" "{dest}"')
    return dest

def create(path, dir=False, verbose=False):
    if dir:
        if verbose: 
            print(f'Creating directory {path}')
        os.system('mkdir -p ' + path)
    else:
        if verbose:
            print(f'Creating file {path}')
        parent = os.path.dirname(path)
        if parent:
            os.system('mkdir -p ' + parent)
        os.system('touch ' + path)
    

def write(text, dest):
    os.system('mkdir -p ' + os.path.dirname(dest))
    with open(dest, 'w') as f:
        f.write(text)

def read(src):
    with open(src, 'r') as f:
        return f.read()

def remove(path, dir=True, trash=True,verbose=False):
    if trash:
        if verbose:
            print(f'Trashing {path}...')
        trash = f'trash/{sync_utils.get_timestamp(20)}/'
        os.system(f'mkdir -p {trash}')
        os.system(f'mv {path} {trash}')
        return
    if dir:
        if verbose:
            print(f'Removing directory {path}')
        os.system('rm -rf ' + path)
    else:
        if verbose:
            print(f'Removing file {path}')
        os.system('rm ' + path)

def get_files(folder_path,path=True,verbose=True):
    folder_path = path_utils.get_absolute_path(folder_path)
    if verbose:
        print(f'Getting all files in {folder_path}')
    files = os.popen(f'find {folder_path} -type f').read().split('\n')
    files = [f for f in files if f]
    if not path:
        files = [path_utils.get_file_name(f) for f in files]
    if verbose:
        print(f'Found {len(files)} files in {folder_path}')
        print(files[:5])
    return files

def get_folders(folder_path,path=True,verbose=True):
    folder_path = path_utils.get_absolute_path(folder_path)
    if verbose:
        print(f'Getting all directories in {folder_path}')
    folders = os.popen(f'find {folder_path} -type d').read().split('\n')
    folders = [f for f in folders if f]
    if not path:
        folders = [path_utils.get_file_name(f) for f in folders]
    if verbose:
        print(f'Found {len(folders)} directories in {folder_path}')
        print(folders[:5])
    return folders

def get_file_size(file_path):
    file_path = path_utils.get_absolute_path(file_path)
    return os.path.getsize(file_path)