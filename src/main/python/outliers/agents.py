import random
import utils.constants as constants_utils
import utils.data.list as list_utils
import utils.debug as debug_utils


def get_random_ids(max_id, num_ids,start=0):
    seed = constants_utils.get_seed()
    random.seed(seed)
    ids =  random.sample(range(start, max_id), num_ids)
    return ids


def get_labeled_ids(ids, labels=['RED', 'ORANGE', 'YELLOW']):
    results = {}
    start = 0
    end = 0
    for label in labels:
        end = end + len(ids)//len(labels)
        if end > len(ids):
            end = len(ids)
        if label == labels[-1]:
            end = len(ids)
        results[label] = ids[start:end]
        start = end
    return results

def print_labeled_ids(labeled_ids):
    for label, ids in labeled_ids.items():
        print(f'{label}:\t{ids}')

def check_labeled_ids(input_ids,labeled_ids):
    length = 0
    for ids in labeled_ids.values():
        length = length + len(ids)
        for id in ids:
            if id not in input_ids:
                print(f'Error: {id} not in ids')
                return False
    if length != len(input_ids):
        print(f'Error: length of labeled_ids is not equal to length of ids: {length} != {len(input_ids)}')
        return False
    return True
    
def get_centralized_outliers_info(max_agent_id, total_outliers, labels=['RED', 'ORANGE', 'YELLOW'], test=True, verbose=False) -> dict:
    agent_ids  = get_random_ids(max_agent_id, total_outliers)
    labeled_agent_ids = get_labeled_ids(agent_ids,labels=labels)
    if test:
        assert check_labeled_ids(agent_ids, labeled_agent_ids)
    if verbose:
        print_labeled_ids(labeled_agent_ids)
    return labeled_agent_ids

def get_labeled_agent_ids(max_agent_id, total_outliers, labels=['RED', 'ORANGE', 'YELLOW'], test=True, verbose=False) -> dict:
    agent_ids  = get_random_ids(max_agent_id, total_outliers)
    labeled_agent_ids = get_labeled_ids(agent_ids,labels=labels)
    if test:
        assert check_labeled_ids(agent_ids, labeled_agent_ids)
    if verbose:
        print_labeled_ids(labeled_agent_ids)
    return labeled_agent_ids

def get_labeled_day_ids(start_day, end_day, how_many, labels=['RED', 'ORANGE', 'YELLOW'], test=True, verbose=False) -> dict:
    day_ids = get_random_ids(end_day, how_many, start=start_day)
    labeled_day_ids = get_labeled_ids(day_ids, labels=labels)
    if test:
        assert check_labeled_ids(day_ids, labeled_day_ids)
    if verbose:
        print_labeled_ids(labeled_day_ids)
    return labeled_day_ids

def get_outliers_agents(max_agent_id, count):
    list_of_agents = list(range(0,max_agent_id))
    hunger_agents = list_utils.get_random_elements(list_of_agents, count)
    work_agents = list_utils.get_random_elements(list_of_agents, count)
    social_agents = list_utils.get_random_elements(list_of_agents, count)
    interest_agents = list_utils.get_random_elements(list_of_agents, count)
    combined_agents = hunger_agents + work_agents + social_agents + interest_agents
    agents ={
        'hunger_agents': hunger_agents,
        'work_agents': work_agents,
        'social_agents': social_agents,
        'interest_agents': interest_agents,
        'combined_agents': combined_agents
    }

    return agents

def get_full_labeled_ids(labeled_ids_dict, start_day, end_day, default_label='NORMAL'):
    all_labeled_ids = {day: default_label for day in range(start_day, end_day)}
    for label, ids in labeled_ids_dict.items():
        for id in ids:
            all_labeled_ids[id] = label
    return all_labeled_ids

            
        