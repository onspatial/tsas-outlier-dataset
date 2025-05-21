import outliers.type.utils as type_utils
def get_manipulation_json(outlier_agents_dict, outlier_start_tick, outlier_end_tick=None):
    results = type_utils.get_outlier_by_type(outlier_agents_dict, outlier_start_tick, outlier_type='Work')
    return results
