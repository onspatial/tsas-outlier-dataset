
import utils.files.path as path_utils
import utils.files.json as json_utils
import utils.data.list as list_utils
import pandas

if __name__ == '__main__':
    city_dir = 'city_infectious_disease'
    folders_path = path_utils.get_sub_folders(city_dir, path=True)

    folders_path = list_utils.remove(folders_path, 'meta')

    for folder_path in folders_path:
        meta_id = '_'.join(folder_path.split('/')[-1].split('_')[1:4])
        outlier_id = '_'.join(folder_path.split('/')[-1].split('_')[4:5])
        if outlier_id.startswith('combined'):
            continue
        initial_meta_info = json_utils.get_json(city_dir + f'/meta/{meta_id}/{outlier_id}_agents.json')
        disease_report_df = pandas.read_csv(folder_path + '/logs/logs/DiseaseReports.tsv', sep='\t')
        disease_report_df = disease_report_df.iloc[:, [0, 1]]
        disease_report_df.columns = ['agent_id', 'disease_state']
        disease_report_df = disease_report_df[disease_report_df['disease_state'] != '[Susceptible,-1,,0.0,2019-07-01T00:00:00.000,,]']
        infected_agents = disease_report_df['agent_id'].unique().tolist()

        initial_agent_diff, infected_agent_diff = list_utils.diff(initial_meta_info, infected_agents)
        # if '' in meta_id:
        print(f'Chance to be infected/spread: {meta_id.split("_")[1]}')
        print(f'Outlier ID: {outlier_id}')
        print(f'Total initial infected agents: {len(initial_meta_info)}')
        print(f'Total infected agents: {len(infected_agents)}')
        print(f'Initial agent not in infected: {len(initial_agent_diff)} (this should be 0)')
        print(f'Infected agent not in initial: {len(infected_agent_diff)} (it shows how many agents got infected)')
        print('-------------------------------------------------------------------------------')
        
