import outliers.json as json_utils
def get_outlier_by_type(outlier_agents_dict, outlier_start_tick, outlier_type):
    results =[]
    for label, ids in outlier_agents_dict.items():
        outlierDegree_value = get_outlierDegree_value(label)
        outlierType_value = outlier_type
        for id in ids:
            outlierDegree_dict= json_utils.get_outlierDegree_dict(id, outlier_start_tick, outlierDegree_value)
            outlierType_dict= json_utils.get_setOutlierType_dict(id, outlier_start_tick, outlierType_value)
            results.append(outlierDegree_dict)
            results.append(outlierType_dict)

    return results
def get_outlierDegree_value(label):
    if label == 'RED':
        outlierDegree_value = 1.0
    elif label == 'ORANGE':
        outlierDegree_value = 0.5
    elif label == 'YELLOW':
        outlierDegree_value = 0.2
    else:
        print('ERROR: label not found')
        return None
    return outlierDegree_value


def get_keepingFullTimeInMinutes_value(label):
    if label == 'RED':
        keepingFullTimeInMinutes_value = 0.0
    elif label == 'ORANGE':
        keepingFullTimeInMinutes_value = 0.5
    elif label == 'YELLOW':
        keepingFullTimeInMinutes_value = 0.75
    else:
        print('ERROR: label not found')
        return None
    return keepingFullTimeInMinutes_value

def get_fullnessDecreasePerStep_value(label):
    if label == 'RED':
        fullnessDecreasePerStep_value = 3.0
    elif label == 'ORANGE':
        fullnessDecreasePerStep_value = 2
    elif label == 'YELLOW':
        fullnessDecreasePerStep_value = 1.5
    else:
        print('ERROR: label not found')
        return None
    return fullnessDecreasePerStep_value

def get_interest_value(label=None):
    # interest is a category just need to be different
    interest_value = 1
    return interest_value

def get_interest_change_ticks(label, start_tick, end_tick):
    ticks = []
    each_day=288
    if label == 'RED':
        ticks = get_ticks_interval(start_tick, end_tick, each_day)
    elif label == 'ORANGE':
        ticks = get_ticks_interval(start_tick, end_tick, each_day*2)
    elif label == 'YELLOW':
        ticks = get_ticks_interval(start_tick, end_tick, each_day*7)
    return ticks


def get_ticks_interval(start_tick, end_tick, interval):
    ticks = []
    for i in range(start_tick, end_tick, interval):
        ticks.append(i)
    return ticks