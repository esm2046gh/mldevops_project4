import logging
import sys
import os
import numpy as np
import subprocess
import commons_proj as cproj
from ingestion import merge_multiple_dataframes
from scoring import perform_scoring

#%%
THE_LOG_FILE = 'fullprocess.log'
logging.basicConfig(
    filename=THE_LOG_FILE,
    level=logging.INFO,
    #filemode='w',
    datefmt='%Y.%m.%dT%H:%M:%S',
    format='%(asctime)s | %(filename)s | %(lineno)s | %(levelname)s | %(message)s')
eol = ''


def msglogger(str_msg):
    script = "fullprocess.py"
    print(f"- {script}. {str_msg}") 
    logging.info(str_msg)



if __name__ == "__main__":   
    #%% Check and read new data
    # 1) read ingestedfiles.txt
    msglogger(f"Start script. ({cproj.config['output_model_path']}). See config. below >>>>>>>>{eol}")
    msglogger(f"config.json: {cproj.config}{eol}")
    
    msglogger(f"Getting list of ingested files so far. {eol}")
    ingested_files = cproj.load_txt_file_as_list('prod_deployment_path', 'ingestedfiles.txt') ##<--
    msglogger(f"Ingested files: {ingested_files}{eol}")
    
    # 2) determine whether the source data folder 
    # has files that aren't listed in ingestedfiles.txt
    
    # get input_folder_files with .csv in input folder
    full_input_folder_path = f"{os.getcwd()}/{cproj.config['input_folder_path']}/"
    msglogger(f"Check if new training files in: {full_input_folder_path}{eol}")
    input_folder_files = []
    for file in os.listdir(full_input_folder_path):
        if file.endswith(".csv"):
            input_folder_files.append(file)
    msglogger(f"Training files in {full_input_folder_path}: {input_folder_files}{eol}")
    
    
    # find the files to ingest
    msglogger(f"Get list of files to ingest{eol}")
    files_to_ingest = []
    for each_file in input_folder_files:
        if each_file not in ingested_files:
            files_to_ingest.append(each_file)
    msglogger(f"Files to ingest: {files_to_ingest}{eol}")
    
    
    #%% Deciding whether to proceed, part 1
    #if you found new data, you should proceed. 
    #otherwise, do end the process here
    if not files_to_ingest:
        msglogger(f"No files to ingest found in {full_input_folder_path}. Script ends <<<<<<<<{eol}")
        sys.exit()
    
    #%% Perform ingestion
    # saves finaldata.csv, ingestedfiles.txt in output_folder_path
    msglogger(f"Performing file ingestion{eol}")
    merge_multiple_dataframes() 
    
    #%% Checking for model drift
    # get latestscore.txt from the deployment directory prod_deployment_path
    msglogger(f"Model drift. Fetching latestscore{eol}")
    latestscore = cproj.load_txt_file('prod_deployment_path', 'latestscore.txt') ##<--
    latestscore = np.float_(latestscore)
    
    # Make predictions using the trainedmodel.pkl model in the /production_deployment
    # Use the most recent data obtained above
    msglogger(f"Model drift. Calculate driftscore using last model (trainedmodel.pkl) and new ingested data (finaldata.csv){eol}")
    driftscore = perform_scoring('output_folder_path', 'finaldata.csv', 
                               'prod_deployment_path', 'trainedmodel.pkl')
    
    msglogger(f"Model drift. latestscore: {latestscore}, driftscore: {driftscore}{eol}")   
    if (driftscore >= latestscore) and latestscore != 0:
        msglogger(f"Model drift. driftscore({driftscore}) >= latestscore({latestscore}). No need to re-train. Script ends <<<<<<<<{eol}") 
        sys.exit()
        
    msglogger(f"Model re-training will be performed{eol}") 
    
    # Re-training
    msglogger(f"Start Training{eol}")
    subprocess.run(['python', 'training.py'])
    msglogger(f"End Training{eol}")
    # Scoring
    msglogger(f"Start Scoring{eol}")
    subprocess.run(['python', 'scoring.py'])
    # Re-deployment
    # README !!
    # Do not perform deployment blindly. Otherwise a new model, which does not
    # perform well on test data, might overwrite the previous model with better
    # performance on test data. Therefore, first compare latestscore from the last 
    # deployed model with newmodel_score, which is the score on test data using the 
    # just trained model
    newmodel_score = cproj.load_txt_file('output_model_path', 'latestscore.txt')
    newmodel_score = np.float_(newmodel_score)
    msglogger(f"Scoring. newmodel_score: {newmodel_score} ,latestscore: {latestscore}{eol}")
    if (newmodel_score < latestscore):
        msglogger(f"Scoring. newmodel_score({newmodel_score}) < latestscore({latestscore}). NEW MODEL WON'T BE DEPLOYED{eol}")
    else:
        msglogger(f"Start Deployment{eol}")
        subprocess.run(['python', 'deployment.py'])
        
    # Reporting
    msglogger(f"Start Reporting{eol}")
    subprocess.run(['python', 'reporting.py'])
    # apicalls
    msglogger(f"Start Apicalls{eol}")
    subprocess.run(['python', 'apicalls.py'])
    
    msglogger(f"Script ended. <<<<<<<< {eol}")

    

