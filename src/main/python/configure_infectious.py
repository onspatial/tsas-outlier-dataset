
import outliers.agents as agents_util
import outliers.print as print_utils
import outliers.manipulations as manipulations_utils
import utils.loops  as loop_utils
import utils.files.json as json_utils
import utils.files.bash as bash_utils 
import custom.string as custom_string
import utils.constants as constants_utils
import custom.simulation as custom_simulation

if __name__ == '__main__':
     # common configurations:
    number_of_agents_list = constants_utils.get_number_of_agents_list()
    maps= constants_utils.get_maps()
    outlier_start_tick = constants_utils.get_outlier_start_tick()
    outlier_end_tick = constants_utils.get_outlier_end_tick()
    spread_days = constants_utils.get_spread_days()
    
    print_utils.info(outlier_start_tick=outlier_start_tick, outlier_end_tick=outlier_end_tick, spread_days=spread_days)

    run_string = custom_string.get_run_bash_script(finish_tick=(4*7+4*7+12*7)*288)
    run_sh_paths = []

    # specific configurations:
    city_id, number_of_initial_infections, infection_degrees = constants_utils.get_infection_configs(cid="2", which='final_decision')

    for number_of_agents, map, infection_degree, number_of_initial_infection in loop_utils.product(number_of_agents_list, maps, infection_degrees, number_of_initial_infections):
                    
        run_path_id = constants_utils.get_config_path(city_id, map, number_of_agents, infection_degree, number_of_initial_infection)
        print(f'Processing {run_path_id}')
        properties = custom_string.get_properties_dict(number_of_agents=number_of_agents, map=map, spread_chance=infection_degree, infection_chance=infection_degree, total_number_of_outliers=number_of_agents, max_num_of_disease_days=spread_days, agent_to_agent=True)


        infectious_outlier_info = agents_util.get_outliers_agents(number_of_agents, number_of_initial_infection)

        hunger_outliers_json = manipulations_utils.get_method_manipulations_json(infectious_outlier_info['hunger_agents'], steps=outlier_start_tick, method_name='setInitialOutlier', parameters='Hunger')

        work_outliers_json = manipulations_utils.get_method_manipulations_json(infectious_outlier_info['work_agents'], steps=outlier_start_tick, method_name='setInitialOutlier', parameters='Work')

        social_outliers_json = manipulations_utils.get_method_manipulations_json(infectious_outlier_info['social_agents'], steps=outlier_start_tick, method_name='setInitialOutlier', parameters='Social')
        
        interest_outliers_json = manipulations_utils.get_method_manipulations_json(infectious_outlier_info['interest_agents'], steps=outlier_start_tick, method_name='setInitialOutlier', parameters='Interest')
        combined_outliers_json = hunger_outliers_json + work_outliers_json + social_outliers_json + interest_outliers_json

        json_utils.save_json(infectious_outlier_info, f'{city_id}/meta/{number_of_agents}/agents_info.json')
        
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
            
    bash_utils.save_run_paths_to_file(run_sh_paths, f'{'city_id'}.sh', parallel=5, append=True)

