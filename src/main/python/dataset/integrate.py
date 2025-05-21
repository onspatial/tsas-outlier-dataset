# util functions for file operations

import os
import sys
import subprocess
import pandas
import utils.files.path as path_utils
import utils.files.check as check_utils

def check_sorted_column(file_path, time_column=0):
    data = get_dataframe(file_path,sample=20000000)
    print(data.head())  
    column = data.iloc[:, time_column]
    column = column.dropna()
    print(f"Checking if column {time_column} is sorted...")
    print(column.head())
    result = True
    result = column == sorted(column)
    result_check = all(result == True)
    print(f"Column {time_column} is sorted: {result_check}")

    print(f'number of true values: {result.sum()}')
    print(f'number of false values: {len(result) - result.sum()}')

    return result

def get_sub_dirs(path):
    path = path_utils.get_absolute_path(path)
    dirs = [f.path for f in os.scandir(path) if f.is_dir()]
    return dirs
def get_files_in_folder(folder_path):
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

def integrate_log_files(log_dir, file_prefix, appended_file, command='cat',remove_original=False, mock=False, time_column=1):
    if mock:
        return appended_file
    log_files = find(log_dir, file_prefix)
    log_files = fix_number_in_names(log_files, accuracy=3)
    log_files.sort()
    appended_file = new_file(appended_file)
    for log_file in log_files:
        if get_file_extension(log_file) == '.zip':
            unzipped_file = unzip(log_file)
            print(f"Unzipped {log_file} to {unzipped_file}")
            appended_file = append(unzipped_file, appended_file, command=command)
            remove(unzipped_file)
            print(f"Appended {unzipped_file} to {appended_file}")
        else:
            appended_file = append(log_file, appended_file, command=command)
            print(f"Appended {log_file} to {appended_file}")
    
    check_sorted_column(appended_file, time_column=time_column)
    if remove_original:
        for log_file in log_files:
            remove(log_file)
    return appended_file

def zip(file):
    file = path_utils.get_absolute_path(file)
    if not exists(file):
        print(f"{file} does not exist...")
        return
    if file.endswith(".zip"):
        print(f"{file} is already a zip file...")
        return file
    os.system(f"cd {get_file_path(file)} && zip -r {get_file_name(file).split('.')[0]}.zip {get_file_name(file)}")
    return f"{get_file_path(file)}/{get_file_name(file)}.zip"
def get_file_list(path):
    path = path_utils.get_absolute_path(path)
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list
def unzip(file):
    file = path_utils.get_absolute_path(file)
    if not exists(file):
        print(f"{file} does not exist...")
        return
    if file.endswith(".zip"):
        output_dir_path = f"{get_file_path(file)}/tmp"
        os.system(f"rm -rf {output_dir_path}")
        os.system(f"mkdir -p {output_dir_path}")
        os.system(f"unzip {file} -d {output_dir_path}")
        check_utils.wait_until_folder_is_not_empty(output_dir_path)
        temp_name = get_file_list(f"{output_dir_path}")[0]
        print(f"Unzipped {file} to {temp_name}")

        return temp_name
    else:
        print(f"{file} is not a zip file...")
        return file
def new_file(file):
    file = path_utils.get_absolute_path(file)
    os.system(f"cat /dev/null > {file}")
    return file
def append(temp, target, new=False, command='cat'):
    print(f"Appending {temp} to {target}...")
    check_safety(target)
    temp = path_utils.get_absolute_path(temp)
    target = path_utils.get_absolute_path(target)
    if not exists(temp):
        print(f"{temp} does not exist...")
        return
    if new:
        os.system(f"{command} {temp} > {target}")
    else:
        os.system(f"{command} {temp} >> {target}")
    return target

def remove(file, verbose=True):
    file = path_utils.get_absolute_path(file)
    if not exists(file):
        print(f"{file} does not exist...")
        return
    if verbose:
        print(f"Removing {file}...")
    os.remove(file)
    return file

def find(path, text):
    path = path_utils.get_absolute_path(path)
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if text in file:
                file_list.append(os.path.join(root, file))
    return file_list

def fix_number_in_names(files, accuracy=3):
    new_files = []
    for file in files:
        new_files += [fix_number_in_name(file, accuracy)]
    return new_files

def fix_number_in_name(file, accuracy=3):
    file = path_utils.get_absolute_path(file)
    if not exists(file):
        print(f"{file} does not exist...")
        return
    file_name = get_file_name(file)
    file_path = get_file_path(file)
    new_file_name = get_zero_filled(file_name, accuracy)
    new_file = os.path.join(file_path, new_file_name)
    return rename(file, new_file)

def get_zero_filled(file_name, accuracy=3):
    numbers = get_numbers_from_name(file_name)
    for number in numbers:
        new_number = str(number).zfill(accuracy)
        file_name = file_name.replace(str(number), new_number)
    return file_name

def get_numbers_from_name(file_name):
    numbers=[]
    number=""
    for char in file_name:
        if char >= "0" and char <= "9":
            number += char
        else:
            if number:
                numbers.append(number)
                number=""
    if number:
        numbers.append(number)
    return numbers

def rename(old, new):
    old = path_utils.get_absolute_path(old)
    new = path_utils.get_absolute_path(new)
    os.rename(old, new)
    return new


def get_file_name(path, extension=True):
    name= os.path.basename(path)
    if extension:
        return name
    return name.split(".")[0]

def get_file_path(path):
    return os.path.dirname(path)

def get_file_extension(path):
    return os.path.splitext(path)[1]

def get_file_size(path):
    return os.path.getsize(path)

def get_dataframe(path, sep="\t", sample=0):
    if sample>0:
        return pandas.read_csv(path, sep=sep, nrows=sample)
    return pandas.read_csv(path, sep=sep)
def get_number_of_lines(path):
    path = path_utils.get_absolute_path(path)
    if not exists(path):
        print(f"{path} does not exist...")
        return
    number_of_lines = int(subprocess.check_output(f"wc -l {path}", shell=True).split()[0])
    return number_of_lines

def log_print(message, file="log.txt"):  
    file = path_utils.get_absolute_path(file)
    check_safety(file)
    if not os.path.exists(file):
        os.makedirs(os.path.dirname(file), exist_ok=True)
    print(message)
    with open(f"{file}", "+a") as f:
        f.write(message + "\n")

def save_json(data, path):
    path = path_utils.get_absolute_path(path)
    from json import dump
    check_safety(path)
    with open(path, "w") as f:
        dump(data, f)

def load_json(path):
    path = path_utils.get_absolute_path(path)
    # print(f"Loading data from {path}")
    from json import load
    with open(path) as f:
        data = load(f)
    return data

def exists(path):
    path = path_utils.get_absolute_path(path)
    return os.path.exists(path)

def get_dir(path):
    path = path_utils.get_absolute_path(path)
    return os.path.dirname(path)

def get_stat_path(path):
    path = path_utils.get_absolute_path(path)
    return os.path.join(get_dir(path), "stat.json")

def read_json(path):
    path = path_utils.get_absolute_path(path)
    from json import load
    with open(path) as f:
        data = load(f)
    return data

def create_mock_pol(path):
    path = path_utils.get_absolute_path(path)
    with open(path, "w") as f:
        f.write("UserId\tCheckinTime\tVenueId\tVenueType\tX\tY\n")
        f.write("154	2019-07-01T06:20:00	322	Restaurant	-1513863.3847658467	1.529611305334078E7\n")
        f.write("80	2019-07-01T06:25:00	322	Restaurant	-1513863.3847658467	1.529611305334078E7\n")
        f.write("14	2019-07-01T06:35:00	322	Restaurant	-1513863.3847658467	1.529611305334078E7\n")

def get_parent(path):
    path = path_utils.get_absolute_path(path)
    parent = None
    if os.path.isabs(path):
        parent = os.path.dirname(path)
        return parent
    current = os.getcwd()
    absolute_path = os.path.join(current, path)
    parent = os.path.dirname(absolute_path)
    return parent

def make_dir(path):
    path = path_utils.get_absolute_path(path)
    os.makedirs(path, exist_ok=True)

def check_safety(path):
    path = path_utils.get_absolute_path(path)
    if not exists(path):
        make_dir(get_parent(path))
    if not exists(path):
        with open(path, "w") as f:
            f.write("")
    

def save_properties_to_file(properties, path="tmp/modified.properties"):
    check_safety(path)
    string = ""
    for key in properties.keys():
        string += f"{key} = {properties[key]}\n"
    with open(path, "w") as f:
        f.write(string)


def save_string_to_file(string, path="tmp/run.sh"):
    check_safety(path)
    with open(path, "w") as f:
        f.write(string)

def get_project_path():
    current_path = os.path.abspath(__file__)
    project_path = current_path.split("/code")[0]
    return project_path

def get_python_path():
    python_path = f'python3'
    return python_path

def delete_file(path, trash=True):
    path = path_utils.get_absolute_path(path)
    import time
    if exists(path):
        print(f"Deleting {path}...")
        if trash:
            timestamp = int(time.time())
            destination = f'trash/t{timestamp}/{path}'
            check_safety(destination)
            os.system(f"mv {path} {destination}")
        else:
            os.remove(path)

def delete_folder(dir, trash=True):
    dir = path_utils.get_absolute_path(dir)
    import time
    if exists(dir):
        print(f"Deleting {dir}...")
        if trash:
            timestamp = int(time.time())
            destination = f'trash/t{timestamp}/{dir}'
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            os.system(f"mv {dir} {destination}")
        else:
            os.system(f"rm -rf {dir}")
    else:
        print(f"{dir} does not exist...")

def run_shell(path, select=True):
    dir = get_parent(path)
    if select:
        os.system(f"sh {path} {path} 2>&1 >> {dir}/run.log.txt")
    else:
        command = f"sh {path} 2>&1 >> {dir}/run.log.txt"
        return subprocess.run(command, shell=True)    


def add_to_shell(path, output_path="tmp/run.sh", append=True, command=None):
    path = path_utils.get_absolute_path(path)
    output_path = path_utils.get_absolute_path(output_path)
    check_safety(output_path)
    execution_command = get_execution_command(path)
    os.system(f"echo '{execution_command}' > {output_path}")

    if append and command is not None:
        os.system(f"echo '{command}' >> {output_path}")
        execution_command = f'{execution_command} && {command}'

    return execution_command

def get_execution_command(path):
    run_dir = get_parent(path)
    log_dir = f"{run_dir}/logs/logs"
    integrated_checkin_path = get_integrated_checkin_path(path, integration=False)
    project_path = get_project_path()

    cd_dir = f"cd {run_dir}"
    touch_run_lock = "touch run.lock"
    run_sh = "sh run.sh 2>&1 > run.log.txt"
    touch_run_unlock = "touch run.unlock"
    python_integrate = f"{get_python_path()} {project_path}/code/integrate.py {log_dir} Checkin {integrated_checkin_path} 2>&1 > integrate.log.txt"
    python_scorer = f"{get_python_path()} {project_path}/code/scorer.py {integrated_checkin_path} 2>&1 > calculation.log.txt"
    touch_processed_done = f"touch processed.done"
    execution_command = f"{cd_dir} && {touch_run_lock} &&  {run_sh} && {touch_run_unlock} && {python_integrate} && {python_scorer} && {touch_processed_done} &"
    return execution_command

def add_wait_to_shell(output_path="tmp/run.sh"):
    output_path = path_utils.get_absolute_path(output_path)
    check_safety(output_path)
    os.system(f"echo 'wait' >> {output_path}")

def append_file_to(file, output_path):
    file = path_utils.get_absolute_path(file)
    output_path = path_utils.get_absolute_path(output_path)
    check_safety(output_path)
    with open(file , "r") as f:
        lines = f.readlines()
    with open(output_path, "a") as f:
        for line in lines:
            f.write(line)


def get_geolife_path(integration=False):
    return f"{get_project_path()}/data/geolife/data.tsv"

def get_raw_checkin_path(path):
    path = path_utils.get_absolute_path(path)
    run_dir = path.split("/run.sh")[0]
    return f"{run_dir}/logs/logs/Checkin.tsv"



def get_integrated_checkin_path(path, integration=False):
    path = path_utils.get_absolute_path(path)
    run_dir = path.split("/run.sh")[0]
    integrated_checkin_path = f"{run_dir}/Checkin.tsv"

    if integration == False:
        return integrated_checkin_path
    else:
        log_dir = f"{run_dir}/logs/logs"
        if exists(integrated_checkin_path):
            print(f"{integrated_checkin_path} exists...")
            return integrated_checkin_path
        return integrate_log_files(log_dir, "Checkin", integrated_checkin_path)
    
def get_files(pattern, folder=None,verbose=True):
    import os
    files_path = []
    extension = pattern.split(".")[-1]
    all_files_path = []
    project_path = get_project_path()
    if folder is None and "/" in pattern:
        folder = pattern.split("/")[0]
        file_name_pattern = pattern.split("/")[-1]
        if verbose:
            print(f'Searching in {folder} for {file_name_pattern}...')
    elif folder is None and "/" not in pattern:
        folder = ""
        file_name_pattern = pattern
   
    search_dir = f"{project_path}/{folder}"
    for root, dirs, files in os.walk(search_dir):
        for file in files:
            all_files_path.append(os.path.join(root, file))

    files_path = get_match_files(all_files_path,file_name_pattern)
    founded_paths = []  
    for file_path in files_path:
        if  extension in file_path:
           founded_paths.append(file_path)
    if verbose:
        print(f"Found {len(founded_paths)} files with extension {extension} in {search_dir}...")
    return founded_paths

def get_match_files(files, file_name_pattern):
    matches = []
    for file_path in files:
        if is_match(file_path, file_name_pattern):
            matches.append(file_path)
    return matches

def is_match(file_path, file_name_pattern):
    file_name_pattern = file_name_pattern.split("*")[0]
    if file_name_pattern in file_path:
        # print(f"{file_name_pattern} is in {file_path}")
        return True
    # print(f"{file_name_pattern} is not in {file_path}")
    return False