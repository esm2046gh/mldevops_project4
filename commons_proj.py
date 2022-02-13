#from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
import json
#from sklearn import metrics
#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression


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

def load_dataframe(folder_name, file_name):
    dataset_csv_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    df = pd.read_csv(dataset_csv_path)
    return df

def prepare_data(data, input_features, output_feature):
   X = data[input_features].values
   y = data[output_feature].values
   return X, y
 
#save the trained model as .pkl
def save_object(obj, folder_name, file_name):
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'wb') as a_file:
        pickle.dump(obj, a_file, pickle.HIGHEST_PROTOCOL)
   
def load_object(folder_name, file_name):
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'rb') as a_file:
        obj = pickle.load(a_file)

    return obj

#save value to file
def save_value(value, folder_name, file_name, append_to_file = False):
    the_path = os.path.join(os.getcwd(), config[folder_name], file_name)
    with open(the_path, 'a+' if append_to_file == True else 'w') as a_file:
        a_file.write(str(value) + '\n')
        a_file.close()
   


