import utils.files.path as path_utils
import utils.files.compress as compress_utils
import utils.files.basics as file_utils
import utils.files.check as check_utils
import utils.files.json as json_utils
import utils.data.list as list_utils
import utils.geo.convert as convert_utils
import utils.geo.info as geo_info_utils
import utils.string.time as time_utils
import dataset.compatibility as compatibility
import dataset.integrate as integrate
import dataset.processing as processing
import pandas
pandas.options.mode.copy_on_write = True
import sys

if __name__ == '__main__':

    city_dirs = ['city_infectious_1']#, 'city_infectious_1', 'city_location_1']
    test_duration_days = 28

    if len(sys.argv) == 2:
        city_dirs = sys.argv[1].split(',')
    elif len(sys.argv) == 3:
        city_dirs = sys.argv[1].split(',')
        test_duration_days = int(sys.argv[2])
    
    
    folders_paths = []
    for city_dir in city_dirs:
        folders_path = path_utils.get_sub_folders(city_dir, path=True)
        folders_path = list_utils.remove(folders_path, 'meta')
        folders_paths += folders_path

    simulation_start_time = '2024-01-01T00:00:00'
    train_start_time = time_utils.get_next_date(simulation_start_time, days=28)
    train_end_time = time_utils.get_next_date(train_start_time, days=28)
    test_start_time = train_end_time
    test_end_time = time_utils.get_next_date(test_start_time, days=test_duration_days)
    
    
    for folder_path in folders_paths:
        try:
            log_dir = f"{folder_path}/logs/logs"
            processed_data_dir = f"{folder_path}/generated_dataset"
            process_status_path = f"{processed_data_dir}/process_status.json"

            if check_utils.exists(process_status_path):
                process_status = json_utils.get_json(process_status_path)
                if process_status['completed']:
                    print(f"Skipping integrating log files from {folder_path} \n")
                    continue
            else:
                print(f"Integrating log files from {folder_path} \n")
                file_utils.remove(processed_data_dir, trash=False)

            map_name = folder_path.split('/')[-1].split('_')[0]
            crs_from = geo_info_utils.get_csr(map_name)
            labels_dict = processing.get_labels_dict(folder_path)
            statistics_dict = processing.get_statistics_dict(log_dir)
            json_utils.save_json(labels_dict, f"{processed_data_dir}/labels.json")
            json_utils.save_json(statistics_dict, f"{processed_data_dir}/statistics.json")

            stay_points_path = integrate.integrate_log_files(log_dir, 'Checkin',f'{processed_data_dir}/staypoints.tsv', mock=False,time_column=1)
            stay_points_df = pandas.read_csv(stay_points_path, sep='\t')
            stay_points_df = convert_utils.convert_to_gps(stay_points_df, lat_col=4, lon_col=5, crs_from=crs_from)
            stay_points_df = compatibility.get_compatible_df(stay_points_df)
            stay_points_train_df = processing.get_split_df(stay_points_df, train_start_time, train_end_time)
            stay_points_test_df = processing.get_split_df(stay_points_df, test_start_time, test_end_time)
            stay_points_train_df = processing.add_labels(stay_points_train_df)
            stay_points_test_df = processing.add_labels(stay_points_test_df, labels_dict)
            stay_points_train_path = f'{processed_data_dir}/staypoints_train.tsv'
            stay_points_test_path = f'{processed_data_dir}/staypoints_test.tsv'
            stay_points_train_df.to_csv(stay_points_train_path, index=False)
            stay_points_test_df.to_csv(stay_points_test_path, index=False)
            compress_utils.zip(stay_points_train_path)
            compress_utils.zip(stay_points_test_path)
            
            trajectories_path = integrate.integrate_log_files(log_dir, 'AgentStateTable',f'{processed_data_dir}/trajectories.tsv', command='cut -f 2-4', mock=False,time_column=0)
            trajectories_df = pandas.read_csv(trajectories_path, sep='\t')
            trajectories_df = convert_utils.convert_to_gps(trajectories_df, lat_col=1, lon_col=1, crs_from=crs_from)
            trajectories_df = compatibility.get_compatible_df(trajectories_df)
            trajectories_train_df = processing.get_split_df(trajectories_df, train_start_time, train_end_time)
            trajectories_test_df = processing.get_split_df(trajectories_df, test_start_time, test_end_time)
            trajectories_train_df = processing.add_labels(trajectories_train_df)
            trajectories_test_df = processing.add_labels(trajectories_test_df, labels_dict)
            trajectories_train_path = f'{processed_data_dir}/trajectories_train.tsv'
            trajectories_test_path = f'{processed_data_dir}/trajectories_test.tsv'
            trajectories_train_df.to_csv(trajectories_train_path, index=False)
            trajectories_test_df.to_csv(trajectories_test_path, index=False)
            compress_utils.zip(trajectories_train_path)
            compress_utils.zip(trajectories_test_path)

            social_links_path = integrate.integrate_log_files(log_dir,'SocialNetwork',f'{processed_data_dir}/social_links.tsv', mock=False,time_column=0)
            social_links_df = pandas.read_csv(social_links_path, sep=r'\s+')
            social_links_df = compatibility.get_compatible_df(social_links_df)
            social_links_train_df = processing.get_split_df(social_links_df, train_start_time, train_end_time)
            social_links_test_df = processing.get_split_df(social_links_df, test_start_time, test_end_time)
            social_links_train_df = processing.add_labels(social_links_train_df)
            social_links_test_df = processing.add_labels(social_links_test_df, labels_dict)
            social_links_train_path = f'{processed_data_dir}/social_links_train.tsv'
            social_links_test_path = f'{processed_data_dir}/social_links_test.tsv'
            social_links_train_df.to_csv(social_links_train_path, index=False)
            social_links_test_df.to_csv(social_links_test_path, index=False)
            compress_utils.zip(social_links_train_path)
            compress_utils.zip(social_links_test_path)


        
            file_utils.remove(stay_points_path, trash=False)
            file_utils.remove(trajectories_path, trash=False)
            file_utils.remove(social_links_path, trash=False)
            file_utils.remove(stay_points_train_path, trash=False)
            file_utils.remove(stay_points_test_path, trash=False)
            file_utils.remove(trajectories_train_path, trash=False)
            file_utils.remove(trajectories_test_path, trash=False)
            file_utils.remove(social_links_train_path, trash=False)
            file_utils.remove(social_links_test_path, trash=False)
            process_status ={
                'completed': True,
                'status_update_time': time_utils.get_current_date(),
                'simulation_start_time': simulation_start_time,
                'train_start_time': train_start_time,
                'train_end_time': train_end_time,
                'test_start_time': test_start_time,
                'test_end_time': test_end_time
            }
            json_utils.save_json(process_status, process_status_path)
            print(f"Done integrating log files from {folder_path} \n")

        except Exception as e:
            print(f"Error in integrating log files from {folder_path}: {e}")
            continue






