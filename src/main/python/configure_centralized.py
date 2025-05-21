
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
    number_of_agents_list = constants_utils.get_number_of_agents_list()
    maps= constants_utils.get_maps()
    outlier_start_tick = constants_utils.get_outlier_start_tick()
    outlier_end_tick = constants_utils.get_outlier_end_tick()
    outlier_warmup_days = constants_utils.get_outlier_warmup_days()
    total_number_of_outliers = constants_utils.get_total_number_of_outliers()
    print_utils.info(outlier_start_tick=outlier_start_tick, outlier_end_tick=outlier_end_tick, outlier_warmup_days=outlier_warmup_days)

    run_string = custom_string.get_run_bash_script(finish_tick=(4*7+4*7+4*7)*288)
    run_sh_paths = []

    # specific configurations:
    city_id, outlier_levels = constants_utils.get_centralized_configs(cid="1")

    for number_of_agents, map in loop_utils.product(number_of_agents_list, maps):

        run_path_id = constants_utils.get_config_path(city_id, map, number_of_agents)
        print(f'Processing {run_path_id}')

        properties = custom_string.get_properties_dict(number_of_agents=number_of_agents, map=map)
        
        centralized_outliers_info = agents_utils.get_centralized_outliers_info(number_of_agents, total_number_of_outliers, labels=outlier_levels, test=True, verbose=False)

        hunger_outliers_json = manipulations_utils.get_hunger_outliers_json(centralized_outliers_info, outlier_start_tick)
        work_outliers_json = manipulations_utils.get_work_outliers_json(centralized_outliers_info, outlier_start_tick)
        social_outliers_json = manipulations_utils.get_social_outliers_json(centralized_outliers_info, outlier_start_tick)
        interest_outliers_json = manipulations_utils.get_interest_outliers_json(centralized_outliers_info, outlier_start_tick, outlier_end_tick)
        combined_outliers_json,combined_outliers_info = manipulations_utils.get_combined_outliers_json(centralized_outliers_info, outlier_start_tick,outlier_end_tick)

        json_utils.save_json(centralized_outliers_info, f'{city_id}/meta/{number_of_agents}/common_info.json')
        json_utils.save_json(combined_outliers_info, f'{city_id}/meta/{number_of_agents}/combined_outliers_info.json')

        run_id = f'{run_path_id}_hunger_outliers'
        run_path = custom_simulation.get_configured_simulation(run_id,run_string, hunger_outliers_json, properties)
        run_sh_paths.append(f'{run_id}/run.sh')

        run_id = f'{run_path_id}_work_outliers'
        run_path = custom_simulation.get_configured_simulation(run_id,run_string, work_outliers_json, properties)
        run_sh_paths.append(f'{run_id}/run.sh')

        run_id = f'{run_path_id}_social_outliers'
        run_path = custom_simulation.get_configured_simulation(run_id,run_string, social_outliers_json, properties)
        run_sh_paths.append(f'{run_id}/run.sh')

        run_id = f'{run_path_id}_interest_outliers'
        run_path = custom_simulation.get_configured_simulation(run_id,run_string, interest_outliers_json, properties)
        run_sh_paths.append(run_path)
        
        run_id = f'{run_path_id}_combined_outliers'
        run_path = custom_simulation.get_configured_simulation(run_id,run_string, combined_outliers_json, properties)
        run_sh_paths.append(run_path)
  
    bash_utils.save_run_paths_to_file(run_sh_paths, f'{'city_id'}.sh', parallel=5, append=False)

