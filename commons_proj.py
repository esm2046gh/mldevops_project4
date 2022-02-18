import pandas as pd
import numpy as np
import pickle
import os
import json
import shutil


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
    dataset_csv_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    df = pd.read_csv(dataset_csv_path)
    return df

def prepare_data(data, input_features, output_feature):
   # X = data[input_features].values
   # y = data[output_feature].values
   X = data[input_features].copy()
   y = data[output_feature].copy()

   return X, y
 
#save the trained model as .pkl
def save_object(obj, folder_name, file_name):
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'wb') as a_file:
        pickle.dump(obj, a_file, pickle.HIGHEST_PROTOCOL)

# load pickle object    
def load_object(folder_name, file_name):
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'rb') as a_file:
        obj = pickle.load(a_file)

    return obj

# save value to file
def save_value(value, folder_name, file_name, append_to_file = False):
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'a+' if append_to_file == True else 'w') as a_file:
        a_file.write(str(value) + '\n')

# copy files
def copy_files(src_dir, src_file, dst_dir, dst_file=""):
    src = os.path.join(os.getcwd(), config[src_dir], src_file)
    dst = os.path.join(os.getcwd(), config[dst_dir], dst_file)
    #dst = dst[:-1] if dst_file == "" else dst
    shutil.copy2(src, dst)

# load text file
def load_txt_file(folder_name, file_name):
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'r') as a_file:
        text = a_file.read()

    return text

# load text file
def load_txt_file_as_list(folder_name, file_name):
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'r') as a_file:
        text = a_file.readlines()

    return text

def load_json_file(file_name, rel_dir_path=''):
    the_path = os.path.join(os.getcwd(),rel_dir_path, file_name)
    with open(the_path, 'r') as a_file:
        data = json.load(a_file)
    
    return data