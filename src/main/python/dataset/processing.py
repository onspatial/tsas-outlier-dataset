import utils.files.json as json_utils
import utils.files.check as check_utils
import pandas

def add_labels(input_df, labels_dict={}):
    input_df['Label'] = 0
    if not labels_dict:
        return input_df
    for agent_id, label_info in labels_dict.items():
        label = label_info['label']
        start_time = label_info['start_time']
        end_time = label_info['end_time']
        input_df.loc[(input_df['AgentID'] == int(agent_id)) & (input_df['Time'] >= start_time) & (input_df['Time'] < end_time), 'Label'] = int(label)

    return input_df

def get_split_df(input_df, start_time, end_time):
    input_df = input_df[(input_df['Time'] >= start_time) & (input_df['Time'] < end_time)]
    return input_df

def get_labels_dict(folder_path):
    root_path = '/'.join(folder_path.split('/')[:-1])
    number_of_agents = int(folder_path.split('/')[-1].split('_')[1])
    outlier_type = folder_path.split('/')[-1].split('_')[-2]
    meta_info_json = get_meta_json(root_path, number_of_agents, outlier_type)
    if meta_info_json is not None:
        labels_dict = get_labels(meta_info_json, outlier_type)
    else:
        log_dir = f"{folder_path}/logs/logs"
        disease_report_df = get_DiseaseReports_df(log_dir)
        labels_dict = get_calculated_labels(disease_report_df)
    return labels_dict
def get_statistics_dict(log_dir):
    statistics = get_statistic(get_DiseaseReports_df(log_dir))
    return statistics
   
def get_calculated_labels(disease_report_df):

    infected_agents_df = disease_report_df[disease_report_df['diseaseStatus'] == 'Infectious']
    infected_agents_df.drop_duplicates(subset=['agentId'])
    recovered_agents_df = disease_report_df[disease_report_df['diseaseStatus'] == 'Recovered']
    recovered_agents_df.drop_duplicates(subset=['agentId'])
    outlier_agents_df = infected_agents_df[['agentId', 'outlierType', 'outlierDegree', 'time']]
    outlier_agents_df.rename(columns={'time': 'start_time'}, inplace=True)
    outlier_agents_df = add_end_time_column(outlier_agents_df, recovered_agents_df)
    labels_dict = get_labels_dict_from_df(outlier_agents_df)
    return labels_dict

def add_end_time_column(outlier_agents_df, recovered_agents_df):

    outlier_agents_df['end_time'] = None
    for index, row in outlier_agents_df.iterrows():
        agent_id = row['agentId']
        end_time = recovered_agents_df[recovered_agents_df['agentId'] == agent_id]['time']
        if len(end_time) > 0:
            outlier_agents_df.at[index, 'end_time'] = end_time.values[0]    
    return outlier_agents_df

def get_labels_dict_from_df(outlier_agents_df):
    labels_dict = {}
    for index, row in outlier_agents_df.iterrows():
        label = get_outlier_code(row['outlierType'].lower()) + get_degree_code(row['outlierDegree'])
        start_time = row['start_time']
        end_time = row['end_time']
        labels_dict[row['agentId']] = get_label_dict(label, start_time, end_time)
    return labels_dict

def get_DiseaseReports_df(log_dir):
    if check_utils.exists(f"{log_dir}/DiseaseReports.tsv"):
        try:
            disease_report_df = pandas.read_csv(f"{log_dir}/DiseaseReports.tsv", sep=r'\t',engine='python')

            disease_report_df[['diseaseStatus', 'byAgentID', 'outlierType', 'outlierDegree', 'time', 'location', 'checkin']] = disease_report_df['[diseaseStatus,byAgentID,outlierType,outlierDegree,time,location,checkin]'].str.split(',', expand=True)

            disease_report_df['diseaseStatus'] = disease_report_df['diseaseStatus'].str.replace('[','')
            disease_report_df['checkin'] = disease_report_df['checkin'].str.replace(']','')
            disease_report_df = disease_report_df[['agentId', 'diseaseStatus','outlierType', 'outlierDegree', 'time']]

            return disease_report_df
        except Exception as e:
            print(f"Error in reading DiseaseReports.tsv: {e}")
            return None
    else:
        return None

def get_statistic(disease_report_df, print_statistic=False):
    statistics = {}
    if disease_report_df is None:
        statistics = {
            'agents_infectious': 0, 
            'agents_susceptible': 0,    
            'agents_recovered': 0,  
            'agents_exposed': 0,    
        }
    else:
        agents_infectious = disease_report_df[disease_report_df['diseaseStatus'] == 'Infectious']
        agents_susceptible = disease_report_df[disease_report_df['diseaseStatus'] == 'Susceptible']
        agents_recovered = disease_report_df[disease_report_df['diseaseStatus'] == 'Recovered']
        agents_exposed = disease_report_df[disease_report_df['diseaseStatus'] == 'Exposed']

        statistics = {
            'agents_infectious': len(agents_infectious),
            'agents_susceptible': len(agents_susceptible),
            'agents_recovered': len(agents_recovered),
            'agents_exposed': len(agents_exposed)
        }
    if print_statistic:
        print(statistics)
    return statistics

def get_meta_json(root_path, number_of_agents, outlier_type):
    meta_path = f"{root_path}/meta/{number_of_agents}"
    meta_file_path = get_meta_file_path(meta_path=meta_path, outlier_type=outlier_type)
    if meta_file_path is not None:
        return json_utils.get_json(meta_file_path)
    else:
        return None

def get_meta_file_path(meta_path, outlier_type):
    if outlier_type == 'combined':
        json_file_path = get_combined_outliers_info_path(meta_path=meta_path)
    else:
        json_file_path = get_common_info_path(meta_path=meta_path)
    return json_file_path

def get_combined_outliers_info_path(meta_path):  
    expected_path=f"{meta_path}/combined_outliers_info.json"
    if not check_utils.exists(expected_path):
        return None        
    return expected_path

def get_common_info_path(meta_path):
    expected_path=f"{meta_path}/common_info.json"
    if not check_utils.exists(expected_path):
        return None
    return expected_path

def get_labels(outliers_info, outlier_type):
    labels_dict = {}
    if outlier_type == 'combined':
        for outlier_type, info in outliers_info.items():
            labels_dict.update(get_labels(info, outlier_type))
    else:
        for level, agent_ids in outliers_info.items():
            for agent_id in agent_ids:
                label =get_code(level, outlier_type)
                labels_dict[agent_id] = get_label_dict(label)
                    
    return labels_dict

def get_label_dict(label, start_time="2000-01-29T00:00:00", end_time="3000-01-29T00:00:00"):
    dict = {
    "label": label,
    "start_time":start_time,
    "end_time": end_time
    }
    return dict
def get_code(level, outlier_type):
    code = get_outlier_code(outlier_type)
    code += get_level_code(level)
    return code
    
def get_outlier_code(outlier_type):
    if outlier_type == 'hunger':
        return  '1'
    elif outlier_type == 'work':
        return  '2'
    elif outlier_type == 'social':
        return  '3'
    elif outlier_type == 'interest':
        return  '4'
    else :
        return  '0'
    
def get_level_code(level):
    if level == 'RED':
        return  '1'
    elif level == 'ORANGE':
        return  '2'
    elif level == 'YELLOW':
        return  '3'
    else :
        return '0'

def get_degree_code(degree):
    if degree == '1.0':
        return  '1'
    elif degree == '0.5':
        return  '2'
    elif degree == '0.2':
        return  '3'
    else:
        return '0'


