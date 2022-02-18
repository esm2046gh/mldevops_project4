
import pandas as pd
#import numpy as np
import timeit
import os
# import json
import commons_proj as cproj
import subprocess

#%% Functions 

# read the deployed model and a test dataset, calculate predictions
def model_predictions(test_df):
    model = cproj.load_object('prod_deployment_path', 'trainedmodel.pkl')
    # prepare data for model
    X, y = cproj.prepare_data(test_df, cproj.input_features, cproj.output_feature)
    # predict
    predicted = model.predict(X)
    return predicted, y 

# get NA-percents for all columns in a dataframe
def na_percent_summary():
    df = cproj.load_dataframe('output_folder_path', 'finaldata.csv')
    percent_missing = df.isnull().sum() * 100 / len(df)
    cols_na_percent = pd.DataFrame({'column_name': df.columns,
                                     'percent_missing': percent_missing}) 
    cols_na_percent.drop('column_name', axis = 1, inplace = True)
    return cols_na_percent
 
# get numeric-inputs statistics
def numeric_inputs_stats(df, numeric_cols):
    stats_dict = {}
    for each_input in numeric_cols:
        stats_dict[each_input] = ['min', 'max', 'mean', 'median', 'std']
        
    cols_stats = df.agg(stats_dict)
    return cols_stats

# get summary statistics
def numeric_inputs_summary():
    df = cproj.load_dataframe('output_folder_path', 'finaldata.csv')
    
    # get numeric columns statistics
    numeric_cols = cproj.input_features.copy()
    numeric_cols.append(cproj.output_feature)
    numeric_cols_stats = numeric_inputs_stats(df, numeric_cols)
    
    # # get NA-percentages for each column
    # cols_na_percent = na_percent_summary()
    # frames = [numeric_cols_stats, cols_na_percent.T]
    # result = pd.concat(frames)
    return numeric_cols_stats

#%% Function to get timings
def execute_script(script_file):
    starttime = timeit.default_timer()
    os.system(f"python3 {script_file}")
    timing=timeit.default_timer() - starttime
    return round(timing, 7)

def execution_time():
    execution_times = {}
    execution_times['ingestion.py'] = [execute_script('ingestion.py')]
    execution_times['training.py'] = [execute_script('training.py')]
   
    return execution_times

#%% Function to check dependencies
def outdated_packages_list():
    outdated = subprocess.check_output(['pip', 'list','--outdated', '--format=columns'])
    with open('outdated.txt', 'wb') as f:
        f.write(outdated)
  
    df = pd.read_csv('outdated.txt', sep=r'\s+', skiprows=[1])
    df.drop(['Type'], axis=1, inplace=True)
    return df
        

# def get_package_versions(package):
#     import pkg_resources
#     import requests
#     installed_version = pkg_resources.get_distribution(package).version
#     response = requests.get(f'https://pypi.org/pypi/{package}/json')
#     latest_version = response.json()['info']['version']
#     return package, installed_version, latest_version

#%%
if __name__ == '__main__':
    # df = cproj.load_dataframe('test_data_path', 'testdata.csv')
    # predicted, y = model_predictions(df)
    
    #stats_summary = numeric_inputs_summary()
    # print(stats)
    # print(na)
    # execution_times = execution_time()
    # print(execution_times)
    # outdated_df = outdated_packages_list()
    #pack, inst, latest = get_package_versions('cycler')
    #print(f"pack: {pack}, inst: {inst}, latest: {latest}")
    pass
    
    
    
   

  
