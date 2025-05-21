import os
import utils.files.basics as file_basics
import time
def exists(path, dir=False):
    try:
        if dir:
            return os.path.isdir(path)
        else:
            return os.path.exists(path)
        
    except Exception as e:
        print(f'ERROR: {path} does not exist and the following error occurred: {e}')
        return False


def is_safe(path, new=False, dir=False):
    try:
        if new:
            if exists(path, dir):
                file_basics.remove(path,dir, trash=False)
            file_basics.create(path,dir)
            return True
        else:
            file_basics.create(path,dir)  
            return True
    except Exception as e:
        print(f'ERROR: {path} is not safe and the following error occurred: {e}')
        return False

            
def wait_until_file_exists(file_path, time_out=10, verbose=False):  
    while not exists(file_path):
        if verbose:
            print(f'Waiting for {file_path} to be written to disk...')
        wait_time = 0.1
        time.sleep(wait_time)
        wait_time *= 2
        if wait_time > time_out:
            break

def wait_until_folder_is_not_empty(folder_path, time_out=10, verbose=True):
    counter = 0
    while not any([not file.startswith('.') for file in os.listdir(folder_path)]):
        counter += 1
        if verbose:
            print(f'{counter}: waiting for {folder_path} to be written to disk...')
        wait_time = 0.1
        time.sleep(wait_time)
        wait_time *= 2
        if wait_time > time_out:
            break
