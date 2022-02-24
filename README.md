# Project4 MLDevOps. A Dynamic Risk Assessment System
- Author: Ernesto Saavedra, February 2022

## Overview
In this project, we create, deploy, and monitor a risk assessment ML model that will estimate the attrition risk of a company's clients. We will set up regular monitoring of the model to ensure that it remains accurate and up-to-date. We will set up processes and scripts to re-train, re-deploy, monitor, and report on the obtained ML model, so that the company can get risk assessments that are as accurate as possible and minimize client attrition.

## Project Steps Overview
You'll complete the project by proceeding through 5 steps:  
1. **Data ingestion.** Automatically check a database for new data that can be used for model training. Compile all training data to a training dataset and save it to persistent storage. Write metrics related to the completed data ingestion tasks to persistent storage.  
2. **Training, scoring, and deploying.** Write scripts that train an ML model that predicts attrition risk, and score the model. Write the model and the scoring metrics to persistent storage.  
3. **Diagnostics.** Determine and save summary statistics related to a dataset. Time the performance of model training and scoring scripts. Check for dependency changes and package updates.  
4. **Reporting.** Automatically generate plots and documents that report on model metrics. Provide an API endpoint that can return model predictions and metrics.  
5. **Process Automation.** Create a script and cron job that automatically run all previous steps at regular intervals.


## Implementation
The scripts in this folder implement all requested steps defined in the Project Steps Overview.  
Following some explanations regarding the implementation:  
- To run all the scripts in mode 'practicemodels' or 'models' simply change the corresponding values in config.json and run the script fullprocess.py
- The files confusionmatrix.png, apireturns.json are generated automatically according to the settings in config.json  
    - confusionmatrix.png => practicemodels/confusionmatrix_practicemodel.png or models/confusionmatrix_models.png
    - apireturns.json -> practicemodels/apireturns_practicemodel.png or models/apireturns_models.png
- The file fullprocess.log contains time-based logs of fulprocess.py  

**Re-deployment**  
In the 'Model Deployment' part of project instructions it is stated that re-deployment should simply copy existing files. However, it might happen that a new model,   which does not perform well on test data, might overwrite the previous model with better performance. Therefore, before copying the files we first compare the latestscore from the last deployed model with the new model score, which is the score on test data. If the new score is higher then new files and models are copied to the deployment folder
