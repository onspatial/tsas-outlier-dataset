import outliers.type.hunger as hunger_utils
import outliers.type.interest as interest_utils
import outliers.type.social as social_utils
import outliers.type.work as work_utils
import utils.data.dict as dict_utils
def get_manipulation_json(outlier_agents_dict, outlier_start_tick, outlier_end_tick=None):
    meta = {}
    results = []
    total_agents = get_total_agents(outlier_agents_dict)
    group_size = total_agents // (4*3)

    start = 0
    end = group_size
    hunger_outlier_agents = dict_utils.get_sliced_list_dict(outlier_agents_dict,start,end)
    meta['hunger'] = hunger_outlier_agents
    start = end
    end += group_size
    work_outlier_agents = dict_utils.get_sliced_list_dict(outlier_agents_dict,start,end)
    meta['work'] = work_outlier_agents

    start = end
    end += group_size
    social_outlier_agents = dict_utils.get_sliced_list_dict(outlier_agents_dict,start,end)
    meta['social'] = social_outlier_agents
    
    start = end
    end += group_size
    interest_outlier_agents = dict_utils.get_sliced_list_dict(outlier_agents_dict,start,end)
    meta['interest'] = interest_outlier_agents
    

    hunger_outliers = hunger_utils.get_manipulation_json(hunger_outlier_agents, outlier_start_tick, outlier_end_tick)
    work_outliers = work_utils.get_manipulation_json(work_outlier_agents, outlier_start_tick, outlier_end_tick)
    social_outliers = social_utils.get_manipulation_json(social_outlier_agents, outlier_start_tick, outlier_end_tick)
    interest_outliers = interest_utils.get_manipulation_json(interest_outlier_agents, outlier_start_tick, outlier_end_tick)

    results.extend(hunger_outliers)
    results.extend(work_outliers)
    results.extend(social_outliers)
    results.extend(interest_outliers)        
    return results, meta

def get_total_agents(outlier_agents_dict):
    total_agents = 0
    for ids in outlier_agents_dict.values():
        total_agents += len(ids)
    return total_agents
