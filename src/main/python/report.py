
import utils.files.path as path_utils   
import utils.data.list as list_utils
import utils.files.json as json_utils
import dataset.report as report_utils
import utils.files.check as check_utils
import utils.files.basics as file_utils
import utils.files.compress as compress_utils
import utils.files.tsv as tsv_utils
import time
def pwait(message):
    print(message)
    time.sleep(1)

def save_info_files(): 
    folders_all = path_utils.get_folders(['generated_dataset/centralized','generated_dataset/infectious','generated_dataset/location'], path=True)
    filter_strings = ['meta']
    filtered_folders = list_utils.filter(folders_all, filter_strings, verbose=True)
    table = []
    for folder in filtered_folders:
        print(f"processing {folder}")
        info = {}
        info['folder'] = folder
        info['map_name'] = report_utils.get_map_name(folder)
        info['number_of_agents'] = report_utils.get_number_of_agents(folder)
        info['outlier_type'] = report_utils.get_outlier_type(folder)
        info['injection_method'] = report_utils.get_injection_method(folder)
        if 'central' not in info['injection_method']:
            info['initial_infected'] = report_utils.get_initial_infected(folder)
            info['agents_infected'] = report_utils.get_agents_infectious(folder)
            info['agents_susceptible'] = report_utils.get_agents_susceptible(folder)
            info['agents_recovered'] = report_utils.get_agents_recovered(folder)
            info['agents_exposed'] = report_utils.get_agents_exposed(folder)
            info['infection_rate'] = report_utils.get_infection_rate(folder)
            info['total_outliers'] = info['agents_infected']
        else:
            info['total_outliers'] = 120
        assert info['total_outliers'] > report_utils.get_initial_infected(folder), f"total_outliers is {info['total_outliers']}"
        info['simulation_start_time'] = report_utils.get_simulation_start_time(folder)
        info['train_start_time'] = report_utils.get_train_start_time(folder)
        info['train_end_time'] = report_utils.get_train_end_time(folder)
        info['test_start_time'] = report_utils.get_test_start_time(folder)
        info['test_end_time'] = report_utils.get_test_end_time(folder)

        if not check_utils.exists(f"{folder}/trajectories_train.tsv"):
            compress_utils.unzip(f"{folder}/trajectories_train.zip")
        if not check_utils.exists(f"{folder}/trajectories_test.tsv"):
            compress_utils.unzip(f"{folder}/trajectories_test.zip")
        if not check_utils.exists(f"{folder}/staypoints_train.tsv"):
            compress_utils.unzip(f"{folder}/staypoints_train.zip")
        if not check_utils.exists(f"{folder}/staypoints_test.tsv"):
            compress_utils.unzip(f"{folder}/staypoints_test.zip")
        if not check_utils.exists(f"{folder}/social_links_train.tsv"):
            compress_utils.unzip(f"{folder}/social_links_train.zip")
        if not check_utils.exists(f"{folder}/social_links_test.tsv"):
            compress_utils.unzip(f"{folder}/social_links_test.zip")


        
        info['number_of_trajectories_train'] = tsv_utils.get_number_of_rows(f"{folder}/trajectories_train.tsv")
        info['number_of_trajectories_test'] = tsv_utils.get_number_of_rows(f"{folder}/trajectories_test.tsv")
        info['number_of_staypoints_train'] = tsv_utils.get_number_of_rows(f"{folder}/staypoints_train.tsv")
        info['number_of_staypoints_test'] = tsv_utils.get_number_of_rows(f"{folder}/staypoints_test.tsv")
        info['number_of_social_links_train'] = tsv_utils.get_number_of_rows(f"{folder}/social_links_train.tsv")
        info['number_of_social_links_test'] = tsv_utils.get_number_of_rows(f"{folder}/social_links_test.tsv")

        info['size_of_trajectories_train'] = file_utils.get_file_size(f"{folder}/trajectories_train.tsv")
        info['size_of_trajectories_test'] = file_utils.get_file_size(f"{folder}/trajectories_test.tsv")
        info['size_of_staypoints_train'] = file_utils.get_file_size(f"{folder}/staypoints_train.tsv")
        info['size_of_staypoints_test'] = file_utils.get_file_size(f"{folder}/staypoints_test.tsv")
        info['size_of_social_links_train'] = file_utils.get_file_size(f"{folder}/social_links_train.tsv")
        info['size_of_social_links_test'] = file_utils.get_file_size(f"{folder}/social_links_test.tsv")

        # remove the files
        # file_utils.remove(f"{folder}/trajectories_train.tsv")
        # file_utils.remove(f"{folder}/trajectories_test.tsv")
        # file_utils.remove(f"{folder}/staypoints_train.tsv")
        # file_utils.remove(f"{folder}/staypoints_test.tsv")
        # file_utils.remove(f"{folder}/social_links_train.tsv")
        # file_utils.remove(f"{folder}/social_links_test.tsv")


        json_utils.save_json(info, f"{folder}/info.json")
        table.append(info)
    json_utils.save_json(table, 'generated_dataset/info.json')
    json_utils.format('generated_dataset')
    return table


if __name__ == '__main__':
    save_info_files()
    

