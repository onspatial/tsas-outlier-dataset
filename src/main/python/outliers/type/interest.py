import outliers.type.utils as type_utils
import outliers.json as json_utils

def get_manipulation_json(outlier_agents_dict, outlier_start_tick, outlier_end_tick=None):
    results = []
    for label, ids in outlier_agents_dict.items():
          
        for agent_id in ids:
            shiftInterest_value = type_utils.get_interest_value(label)
            change_ticks = type_utils.get_interest_change_ticks(label, outlier_start_tick, outlier_end_tick)
            for start_tick in change_ticks:
                shiftInterest_dict = json_utils.get_shiftInterest_dict(agent_id, start_tick, shiftInterest_value)
                results.append(shiftInterest_dict)
    return results
