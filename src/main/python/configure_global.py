
import outliers.agents as agents_utils
import outliers.manipulations as manipulations_utils
import outliers.print as print_utils
import utils.loops as loop_utils
import utils.files.json as json_utils
import utils.files.bash as bash_utils 
import custom.string as custom_string
import custom.simulation as custom_simulation
import utils.constants as constants_utils

if __name__ == '__main__':
    # common configurations:
    total_test_days = 600
    test_start_day = 450
    number_of_agents_list = constants_utils.get_number_of_agents_list()
    maps= constants_utils.get_maps()
    outlier_start_tick = constants_utils.get_outlier_start_tick(start_day=test_start_day)
    outlier_end_tick = constants_utils.get_outlier_end_tick(duration_days=total_test_days, start_tick=outlier_start_tick)
    outlier_end_day = outlier_end_tick // 288
    outlier_warmup_days = constants_utils.get_outlier_warmup_days()
    total_number_of_outliers = constants_utils.get_total_number_of_outliers()
    print_utils.info(outlier_start_tick=outlier_start_tick, outlier_end_tick=outlier_end_tick, outlier_warmup_days=outlier_warmup_days)
    run_string = custom_string.get_run_bash_script(finish_tick=outlier_end_tick)
    run_sh_paths = []
    city_id, outlier_levels = constants_utils.get_global_configs(cid="2", which='global')
    
    for number_of_agents, map in loop_utils.product(number_of_agents_list, maps):
        run_path_id = constants_utils.get_config_path(city_id, map, number_of_agents)
        print(f'Processing {run_path_id}')
        properties = custom_string.get_properties_dict(number_of_agents=number_of_agents, map=map)
        labeled_day_ids = agents_utils.get_labeled_day_ids(start_day=test_start_day,end_day=outlier_end_day, how_many=270, labels=outlier_levels, test=True, verbose=False)
        test_days_labeled = agents_utils.get_full_labeled_ids(labeled_day_ids, start_day=test_start_day, end_day=outlier_end_day)
        manipulations = manipulations_utils.get_global_manipulations_json(test_days_labeled)
        json_utils.save_json(test_days_labeled, f'{city_id}/meta/{number_of_agents}/agents_info.json')
        run_id = f'{run_path_id}_global_outliers'
        run_path = custom_simulation.get_configured_simulation(run_id,run_string, manipulations, properties)
        run_sh_paths.append(run_path)
            

        
  
    bash_utils.save_run_paths_to_file(run_sh_paths, f'{'city_id'}.sh', parallel=5, append=False)

