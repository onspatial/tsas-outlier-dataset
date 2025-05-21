import os
import json
import utils.files.check as check_utils
def get_json(file,verbose=False):
    if verbose:
        print(f'Getting JSON from {file}')
    with open(file, 'r') as f:
        return json.load(f)
    
def save_json(data, file):
    check_utils.is_safe(file, new=True, dir=False)
    with open(file, 'w') as f:
        json.dump(data, f)

def format(folder, pattern="**/*.json"):    
    os.system(f"cd {folder} && npx prettier --write {pattern} && cd -")