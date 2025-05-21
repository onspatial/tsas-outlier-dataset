
import utils.files.json as json_utils


def get_number_of_agents(folder):
    number_of_agents = 1000
    return number_of_agents

def get_initial_infected(folder):
    initial_infected = 10
    return initial_infected

def get_agents_infectious(folder):
    statistics = json_utils.get_json(f"{folder}/statistics.json")
    agents_infectious = statistics['agents_infectious']
    return agents_infectious

def get_agents_susceptible(folder):
    statistics = json_utils.get_json(f"{folder}/statistics.json")
    agents_susceptible = statistics['agents_susceptible']
    return agents_susceptible

def get_agents_recovered(folder):
    statistics = json_utils.get_json(f"{folder}/statistics.json")
    agents_recovered = statistics['agents_recovered']
    return agents_recovered

def get_agents_exposed(folder):
    statistics = json_utils.get_json(f"{folder}/statistics.json")
    agents_exposed = statistics['agents_exposed']
    return agents_exposed

def get_infection_rate(folder):
    if 'infectious' in folder:
        infection_rate = folder.split('/')[-1].split('_')[1]
        infection_rate = float(infection_rate)
    elif 'location' in folder:
        infection_rate = folder.split('/')[-1].split('_')[3]
        infection_rate = float(infection_rate)
    else:
        infection_rate = 0.0
    return infection_rate

def get_simulation_start_time(folder):
    processes_status = json_utils.get_json(f"{folder}/process_status.json")
    simulation_start_time = processes_status['simulation_start_time']
    return simulation_start_time

def get_train_start_time(folder):
    processes_status = json_utils.get_json(f"{folder}/process_status.json")
    train_start_time = processes_status['train_start_time']
    return train_start_time

def get_train_end_time(folder):
    processes_status = json_utils.get_json(f"{folder}/process_status.json")
    train_end_time = processes_status['train_end_time']
    return train_end_time

def get_test_start_time(folder):
    processes_status = json_utils.get_json(f"{folder}/process_status.json")
    test_start_time = processes_status['test_start_time']
    return test_start_time

def get_test_end_time(folder):
    processes_status = json_utils.get_json(f"{folder}/process_status.json")
    test_end_time = processes_status['test_end_time']
    return test_end_time

def get_map_name(folder):
    folder_name = folder.split('/')[-1]
    map_name = folder_name.split('_')[0]
    return map_name

def get_outlier_type(folder):
    folder_name = folder.split('/')[-1]
    outlier_type = folder_name.split('_')[-2]
    return outlier_type

def get_injection_method(folder):
    injection_method = folder.split('/')[-2]
    if injection_method == 'centralized':
        injection_method = 'central manipulation'

    elif injection_method == 'infectious':
        injection_method = 'infectious disease spread'
    elif injection_method == 'location':
        injection_method = 'location-based infection'
    else:
        injection_method = 'unknown'
    return injection_method