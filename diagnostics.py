
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
    return predicted 

# get NA-percents for all columns in a dataframe
def na_percent_summary(df):
    percent_missing = df.isnull().sum() * 100 / len(df)
    cols_na_percent = pd.DataFrame({'column_name': df.columns,
                                     'percent_missing': percent_missing}) 
    return cols_na_percent
 
# get numeric-inputs statistics
def numeric_inputs_summary(df, numeric_cols):
    stats_dict = {}
    for each_input in numeric_cols:
        stats_dict[each_input] = ['min', 'max', 'mean', 'median', 'std']
        
    cols_stats = df.agg(stats_dict)
    return cols_stats

# get summary statistics
def dataframe_summary():
    df = cproj.load_dataframe('output_folder_path', 'finaldata.csv')
    
    # get numeric columns statistics
    numeric_cols = cproj.input_features
    numeric_cols.append(cproj.output_feature)
    numeric_cols_stats = numeric_inputs_summary(df, numeric_cols)
    
    # get NA-percentages for each column
    cols_na_percent = na_percent_summary(df)
    
    return numeric_cols_stats, cols_na_percent

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

# def get_package_versions(package):
#     import pkg_resources
#     import requests
#     installed_version = pkg_resources.get_distribution(package).version
#     response = requests.get(f'https://pypi.org/pypi/{package}/json')
#     latest_version = response.json()['info']['version']
#     return package, installed_version, latest_version

#%%
if __name__ == '__main__':
    # #model_predictions()
    # stats, na = dataframe_summary()
    # print(stats)
    # print(na)
    # execution_times = execution_time()
    # print(execution_times)
    #outdated_packages_list()
    pack, inst, latest = get_package_versions('cycler')
    print(f"pack: {pack}, inst: {inst}, latest: {latest}")
    
    
    
   

  
