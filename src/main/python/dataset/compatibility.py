import pandas
def get_compatible_name(name):
    name_pool = get_name_pool()
    for key, value in name_pool.items():
        if name in value:
            return key
    return name

def get_name_pool():
    name_pool = {
        'AgentID': ['agentId','UserId','from'],
        'Time': ['simulationTime','time','timestamp', 'CheckinTime'],
        'Latitude': ['X','latitude','lat'],
        'Longitude': ['Y','longitude','lon'],
        'FriendID': ['to']
    }
    return name_pool

def rename_columns(input_df):
    input_df_columns = input_df.columns
    for name in input_df_columns:
        compatible_name = get_compatible_name(name)
        input_df = input_df.rename(columns={name:compatible_name})
    return input_df

def reorder_columns(input_df):
    input_df_columns = input_df.columns
    name_pool = get_name_pool()
    new_df = pandas.DataFrame()
    for key, value in name_pool.items():
        if key in input_df_columns:
            new_df[key] = input_df[key]
            input_df = input_df.drop(key, axis=1)
    
    rest_columns = input_df.columns
    for column in rest_columns:
        new_df[column] = input_df[column]
        
    return new_df

def get_compatible_df(input_df):
    input_df = rename_columns(input_df)
    input_df = reorder_columns(input_df)
    return input_df