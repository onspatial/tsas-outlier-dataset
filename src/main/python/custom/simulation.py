
import utils.files.json as json_utils
import utils.files.text as text_utils
import utils.files.bash as bash_utils 

def get_configured_simulation(run_id, run_string, manipulation_json=None, properties=None):
    if manipulation_json:
        json_utils.save_json(manipulation_json, f'{run_id}/manipulations.json')
    if properties:
        text_utils.save_text(properties, f'{run_id}/modified.properties')
    bash_utils.save_bash_string_to_file(run_string, f'{run_id}/run.sh')
    run_sh_path = f'{run_id}/run.sh'
    return run_sh_path