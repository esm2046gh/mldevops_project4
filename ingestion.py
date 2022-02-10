import pandas as pd
import numpy as np
import os
import json
from datetime import datetime




#%% Function for data ingestion
def merge_multiple_dataframe():

    # Load config.json and get input and output paths
    with open('config.json', 'r') as f:
        config = json.load(f)

    input_folder_path = '/' + config['input_folder_path'] + '/'
    output_folder_path = '/' + config['output_folder_path'] + '/'

    # get filenames with .csv in input folder
    filenames = []
    for file in os.listdir(os.getcwd() + input_folder_path):
        if file.endswith(".csv"):
            filenames.append(file)

    #get the list of dataframes
    df_list = []
    for each_filename in filenames:
        df = pd.read_csv(os.getcwd() + input_folder_path + each_filename)
        df_list.append(df)

    #check that all have same columns
    if all([set(df_list[0].columns) == set(df.columns) for df in df_list]):
        print('- All tables have the same columns')
    else:
        print('- Some table(s) have different columns')
        return None

    #merge the dataframes
    merged_dfs = pd.DataFrame(columns=df_list[0].columns.values.tolist())
    for each_dataframe in df_list:
        merged_dfs = merged_dfs.append(each_dataframe, ignore_index=True)

    #remove duplicates if present
    len0 = len(merged_dfs)
    merged_dfs.drop_duplicates(keep=False, inplace=True)

    print(f"- Duplicate rows being removed: {len0 - len(merged_dfs)}")

    # save merged_dfs as .csv
    merged_dfs.to_csv(os.getcwd() + output_folder_path + 'finaldata.csv', index=False)

    #save list of files
    textfile = open(os.getcwd() + output_folder_path + 'ingestedfiles.txt', "w")
    for element in filenames:
        textfile.write(element + "\n")
    textfile.close()
    
    return merged_dfs


#%%
if __name__ == '__main__':
    dataframes = merge_multiple_dataframe()
