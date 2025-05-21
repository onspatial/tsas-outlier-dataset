
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
    city_id, ranks_lists, infection_degrees, manipulation_methods = constants_utils.get_location_configs(cid="1")
    outlier_degrees_list= constants_utils.get_outlier_degrees_list()
    for number_of_agents, map, ranks_list, manipulation_method, infection_degree in loop_utils.product(number_of_agents_list, maps, ranks_lists, manipulation_methods, infection_degrees):
        ranks_string = '_'.join([str(rank) for rank in ranks_list])
        run_path_id = constants_utils.get_config_path(city_id, map, number_of_agents, manipulation_method, ranks_string,infection_degree)
        print(f'Processing {run_path_id}')

        properties = custom_string.get_properties_dict(number_of_agents=number_of_agents, map=map, total_number_of_outliers=number_of_agents, max_num_of_disease_days=spread_days, place_to_agent=True)

        agents_to_be_outliers = agents_util.get_outliers_agents(number_of_agents, len(ranks_list))

        output_json = []

        hunger_parameters_options = ('Hunger', outlier_degrees_list, infection_degree, ranks_list)
        hunger_outliers_json = manipulations_utils.get_method_manipulations_json_by_options(hunger_parameters_options, agent_ids = agents_to_be_outliers['hunger_agents'], actor='PUB', steps=outlier_start_tick, method_name=manipulation_method)
        
        work_parameters_options = ('Work', outlier_degrees_list, infection_degree, ranks_list)
        work_outliers_json = manipulations_utils.get_method_manipulations_json_by_options(work_parameters_options, agent_ids = agents_to_be_outliers['work_agents'], actor='PUB', steps=outlier_start_tick, method_name=manipulation_method)

        social_parameters_options = ('Social', outlier_degrees_list, infection_degree, ranks_list)
        social_outliers_json = manipulations_utils.get_method_manipulations_json_by_options(social_parameters_options, agent_ids = agents_to_be_outliers['social_agents'], actor='PUB', steps=outlier_start_tick, method_name=manipulation_method)

        interest_parameters_options = ('Interest', outlier_degrees_list, infection_degree, ranks_list)
        interest_outliers_json = manipulations_utils.get_method_manipulations_json_by_options(interest_parameters_options, agent_ids = agents_to_be_outliers['interest_agents'], actor='PUB', steps=outlier_start_tick, method_name=manipulation_method)

        combined_outliers_json = hunger_outliers_json + work_outliers_json + social_outliers_json + interest_outliers_json

        json_utils.save_json(agents_to_be_outliers, f'{city_id}/meta/{number_of_agents}/outliers.json')
        
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

