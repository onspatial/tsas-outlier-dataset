
import utils.files.path as path_utils
def get_seed():
    seed = 1234
    return seed

def get_number_of_agents_list(which='final_decision'):
    if which == 'final_decision':
        number_of_agents_list = [1000]
    elif which == 'large':
        number_of_agents_list = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
    else:
        number_of_agents_list = [1000,5000,10000]
    return number_of_agents_list

def get_maps(which='final_decision'):
    if which == 'large':
        maps = ['atl','brln','bjng' 'gmu', 'nola', 'sfco',' atl-metro']
    elif which == 'final_decision':
        maps = ['atl', 'nola','gmu','bjng','atl-metro']
    else:
        maps = ['atl']
    return maps

def get_ticks_per_day():
    ticks_per_day = 288
    return ticks_per_day

def get_outlier_start_tick(start_day=450):
    outlier_start_tick =  get_ticks_per_day()*start_day
    return outlier_start_tick

def get_outlier_end_tick(duration_days=450, start_tick=get_outlier_start_tick()):
    outlier_end_tick = start_tick +  get_ticks_per_day()*duration_days + get_outlier_warmup_days() * get_ticks_per_day()
    return outlier_end_tick

def get_outlier_warmup_days():
    outlier_warmup_days = 0
    return outlier_warmup_days
def get_spread_days():
    spread_days = 1000
    return spread_days
def get_infection_degrees(which='final_decision'):
    if which == 'final_decision':
        infection_degree = [0.01,0.05]#,0.1,0.5,1.0]
    else:
        infection_degree = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5]
    return infection_degree

def get_total_number_of_outliers():
    total_number_of_outliers = 1000
    return total_number_of_outliers

def get_initial_infections(which='final_decision'):
    if which == 'final_decision':
        number_of_initial_infections = [10]
    else:
        number_of_initial_infections = [5,10,15,20,25,30,35,40,45,50]
    return number_of_initial_infections

def get_infection_configs(which='final_decision',cid=""):
    city_id = get_city_id('city_infectious', 
                          cid)
    number_of_initial_infections = get_initial_infections(which)
    infection_degree = get_infection_degrees(which)
    return city_id, number_of_initial_infections, infection_degree


def get_centralized_configs(cid="", which='final_decision'):
    city_id = get_city_id('city_centralized', cid)
    outlier_levels = ['RED', 'ORANGE', 'YELLOW']
    return city_id, outlier_levels

def get_global_configs(cid="", which='final_decision'):
    city_id = get_city_id('city_global', cid)
    if which == 'final_decision':
        outlier_levels = ['RED', 'ORANGE', 'YELLOW']
    elif which == 'global':
        outlier_levels = ['RED_HUNGER', 'RED_WORK', 'RED_SOCIAL', 'ORANGE_HUNGER', 'ORANGE_WORK', 'ORANGE_SOCIAL', 'YELLOW_HUNGER', 'YELLOW_WORK', 'YELLOW_SOCIAL']
    return city_id, outlier_levels

def get_location_configs(cid="", which='final_decision'):
    city_id = get_city_id('city_location', cid)
    ranks_lists = [[1]]
    infection_degrees = get_infection_degrees(which)
    manipulation_methods = ['infectPopularPub','infectNearestPub']
    return city_id, ranks_lists, infection_degrees, manipulation_methods   

def get_city_id(string,cid):
    city_id = f'{string}_{cid}'
    return city_id

def get_config_path(city_id, *args):
    run_id = f'{city_id}/{"_".join(map(str,args))}'
    run_id = path_utils.get_absolute_path(run_id)
    return run_id

def get_outlier_degrees_list():
    outlier_degrees_list = [1.0, 0.5, 0.2]
    return outlier_degrees_list