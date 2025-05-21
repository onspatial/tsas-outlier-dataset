def get_run_bash_script(log_dir='logs', log_level='c01', jar_path='../../jar/pol.jar', properties_file_name='modified.properties', finish_tick=24192):
    run_string =f"""#!/bin/bash
if [ -f run.unlock ]; then
    echo "Unlock file exists, exiting"
else
    java -Dlog4j2.configurationFactory=pol.log.CustomConfigurationFactory -Dlog.rootDirectory={log_dir} -Dsimulation.test={log_level} -jar {jar_path} -configuration {properties_file_name} -until {finish_tick} 
fi"""
    return run_string


def get_properties_dict(seed=1,number_of_agents=1000, map='atl', manipulation_file_path='manipulations.json', spread_chance=0.00, infection_chance=0.00,total_number_of_outliers=0,max_num_of_disease_days=0, agent_to_agent=False,place_to_agent=False):
    properties = {
        'seed': seed,
        'numOfAgents': number_of_agents,
        'maps': f'../../life/maps/{map}/map',
        'initialManipulationFilePath': manipulation_file_path,
    }

    if spread_chance != 0.00:
        properties['spreadDegreePerStep'] = spread_chance

    if infection_chance != 0.00:
        properties['infectionDegreePerStep'] = infection_chance

    if total_number_of_outliers != 0:
        properties['maxNumOfInfectedAgents'] = total_number_of_outliers

    if max_num_of_disease_days != 0:
        properties['maxNumOfDiseaseDays'] = max_num_of_disease_days
    
    if agent_to_agent:
        properties['agentToAgentSpread'] = 'true'

    if place_to_agent:
        properties['placeToAgentSpread'] = 'true'

    return properties