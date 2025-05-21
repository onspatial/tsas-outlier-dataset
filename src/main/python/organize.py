import utils.files.check as check_utils
import utils.files.search as search_utils
import utils.files.basics as file_basics
import utils.files.path as path_utils
import utils.data.list as list_utils
import utils.files.json as json_utils

def file_for_dataset():
    
    folders_all = path_utils.get_folders(['city_centralized_1','city_infectious_1','city_location_1'], path=True)
    # remove the folders that has /meta in them
    # filter_strings = ['meta','brln','interest_outliers','combined_outliers','infectPopularPub','0.01','0.1']
    filter_strings = ['meta']
    filtered_folders = list_utils.filter(folders_all, filter_strings, verbose=True)
    for folder in filtered_folders:
        old_path = f'{folder}/generated_dataset'
        new_path = folder.replace('city_','').replace('_1/','/').replace('_1000_','_').replace('atl','atlanta').replace('brln','berlin')
        new_path = f'generated_dataset/{new_path}'
        print(f'Copying {old_path} to {new_path}')
        file_basics.copy(old_path, new_path)
    
    
    print(f'all folders: {len(folders_all)} and filtered folders: {len(filtered_folders)}')

def file_for_plot():
    
    # Files needed for plots
    # For central outliers: Checkin.tsv and meta folder
    # For agent2agent: DiseaseReports.tsv
    # For place2agent: DiseaseReports.tsv, run.log.txt, Checkin.tsv and 2024-08-07/AgentStateTable-001.tsv.zip only for one folder(atl_1000_infectNearestPub_1_0.1_combined_outliers)
    center_outliers_file_patters = ['Checkin.tsv']
    agent2agent_file_patters = ['DiseaseReports.tsv']
    place2agent_file_patters = ['Checkin.tsv','DiseaseReports.tsv','run.log.txt','AgentStateTable-001.tsv.zip']
    
    for file_pattern in place2agent_file_patters:
        files_needed = search_utils.get_matching_files('./city_location_1',file_pattern,regex=False)
        # copy them to temp directory witht he same structure and directory name
        for file in files_needed:
            folder_name = file.split('/')[4]
            file_name = '/'.join(file.split('/')[5:])
            des = f'Reports/{folder_name}/{file_name}'
            file_basics.copy(file, des)

def rest_info_files():
    files_needed = search_utils.get_matching_files('/run/media/amiri/amirih/outlier_dataset/','labels.json',regex=False)
    for file in files_needed:
            folder_name = file.split('/')[4]
            file_name = '/'.join(file.split('/')[5:])
            des = f'MISSING/{folder_name}/{file_name}'
            file_basics.copy(file, des)

def fix_labels_bug():
    files_needed = search_utils.get_matching_files('generated_dataset/centralized','labels.json',regex=False)
    for labels_file in files_needed:
        info_file = labels_file.replace('labels.json','info.json')
        labels_json = json_utils.get_json(labels_file)
        info_json = json_utils.get_json(info_file)
        for agent_id, detail in labels_json.items():
            detail['start_time']=info_json['test_start_time']
            detail['end_time'] = info_json['test_end_time']
        json_utils.save_json(labels_json, labels_file)
        print(f'Fixed {labels_file}')
    json_utils.format('generated_dataset/centralized')

if __name__ == '__main__':
    fix_labels_bug()