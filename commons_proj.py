import pandas as pd
import numpy as np
import pickle
import os
import json
import shutil
from datetime import datetime


#%% global variables & constants
# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

# inputs and output labels
input_features = [
    "lastmonth_activity",
    "lastyear_activity",
    "number_of_employees"]

output_feature = "exited"

#%% Functions

# loa dataframe from file
def load_dataframe(folder_name, file_name):
    fname = 'load_dataframe'
    dataset_csv_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    df = pd.read_csv(dataset_csv_path)
    print(f"- {fname}. file_path: {dataset_csv_path}") 
    return df

def prepare_data(data, input_features, output_feature):
   # X = data[input_features].values
   # y = data[output_feature].values
   X = data[input_features].copy()
   y = data[output_feature].copy()

   return X, y
 
#save the trained model as .pkl
def save_object(obj, folder_name, file_name):
    fname = 'save_object'
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'wb') as a_file:
        pickle.dump(obj, a_file, pickle.HIGHEST_PROTOCOL)
    print(f"- {fname}. file_path: {the_path}") 

# load pickle object    
def load_object(folder_name, file_name):
    fname = 'load_object'
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'rb') as a_file:
        obj = pickle.load(a_file)

    print(f"- {fname}. file_path: {the_path}") 
    return obj

# save value to file
def save_value(value, folder_name, file_name, append_to_file = False):
    fname = 'save_value'
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'a+' if append_to_file == True else 'w') as a_file:
        a_file.write(str(value) + '\n')
    print(f"- {fname}. value: {value}, file_path: {the_path}") 

# copy files
def copy_files(src_dir, src_file, dst_dir, dst_file=""):
    fname = 'copy_files'
    src = os.path.join(os.getcwd(), config[src_dir], src_file)
    dst = os.path.join(os.getcwd(), config[dst_dir], dst_file)
    #dst = dst[:-1] if dst_file == "" else dst
    print(f"- {fname}. src: {src}") 
    print(f"- {fname}. dst: {dst}")
    shutil.copy2(src, dst)

# load text file
def load_txt_file(folder_name, file_name):
    fname = 'load_txt_file'
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'r') as a_file:
        text = a_file.read()

    print(f"- {fname}. file_path: {the_path}") 
    return text

# load text file
def load_txt_file_as_list(folder_name, file_name):
    fname = 'load_txt_file_as_list'
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'r') as a_file:
        #text = a_file.readlines() #this return \n at the end !!
        text = a_file.read().splitlines() 
    
    print(f"- {fname}. file_path: {the_path}")     
    return text

def load_json_file(file_name, rel_dir_path=''):
    fname = 'load_json_file'
    the_path = os.path.join(os.getcwd(),rel_dir_path, file_name)
    with open(the_path, 'r') as a_file:
        data = json.load(a_file)
    
    print(f"- {fname}. file_path: {the_path}") 
    return data

def time_based_file_name(file_name):
    chars_to_clean = '\\/:*?\"<>| '
    for a_char in chars_to_clean:
        file_name = file_name.replace(a_char, '_')

    now_str = datetime.now().strftime('%Y.%m.%d_%H.%M.%S')

    return now_str + '_' + file_name
