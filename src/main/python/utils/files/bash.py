
import utils.files.path as path_utils    
import utils.files.check as check_utils
def save_run_paths_to_file(run_paths, file, parallel=8, append=False):
    tracker=0
    with open(file, 'a' if append else 'w') as f:
        for line in run_paths:
            tracker+=1
            folder = ('/').join(line.split('/')[0:-1])
            run_sh = line.split('/')[-1]
            f.write(f'cd {folder}\n')
            f.write(f'echo "Processing {folder}"\n')
            f.write(f'touch run.lock\n')
            f.write(f'bash {run_sh} >run.log.txt 2>&1 && touch run.unlock & \n')
            f.write(f'cd {path_utils.get_project_path()}\n')
            if tracker%parallel==0:
                f.write(f'echo waiting for {parallel} to finish\n')
                f.write(f'wait\n')
            f.write('\n')
        f.write(f'wait\n')
        f.write(f'# shutdown -h now\n')


def save_bash_string_to_file(bash_string, file_path):
    file_path = path_utils.get_absolute_path(file_path)
    check_utils.is_safe(file_path, new=True, dir=False)    
    if not file_path.endswith('.sh'):
        file_path = file_path + '.sh'
    
    with open(file_path, 'w') as f:
        f.write(bash_string)
