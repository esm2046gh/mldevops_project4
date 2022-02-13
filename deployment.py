import commons_proj as cproj

#%% global variables & constants


#%% Functions
def store_into_deployment_dir():
    # copy model to deployment_dir
    cproj.copy_files('output_model_path', 'trainedmodel.pkl', 'prod_deployment_path')
    # copy latestscore to deployment_dir
    cproj.copy_files('output_model_path', 'latestscore.txt', 'prod_deployment_path')
    # copy ingestedfiles.txt
    cproj.copy_files('output_folder_path', 'ingestedfiles.txt', 'prod_deployment_path')

#%%
if __name__ == '__main__':
    store_into_deployment_dir()   
        

