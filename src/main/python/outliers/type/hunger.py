import outliers.json as json_utils
import outliers.type.utils as type_utils

def get_manipulation_json(outlier_agents_dict, outlier_start_tick, outlier_end_tick=None):
    results = []
    for label, ids in outlier_agents_dict.items():
        keepingFullTimeInMinutes_value = type_utils.get_keepingFullTimeInMinutes_value(label)
        fullnessDecreasePerStep_value = type_utils.get_fullnessDecreasePerStep_value(label)
        for id in ids:        
            keepingFullTimeInMinutes_dict= json_utils.get_keepingFullTimeInMinutes_dict(id, outlier_start_tick,keepingFullTimeInMinutes_value)
            fullnessDecreasePerStep_dict= json_utils.get_fullnessDecreasePerStep_dict(id, outlier_start_tick, fullnessDecreasePerStep_value)
            results.append(keepingFullTimeInMinutes_dict)
            results.append(fullnessDecreasePerStep_dict)
        
    return results
