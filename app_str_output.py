from flask import Flask, request, jsonify, session, redirect, url_for
#import pandas as pd
import numpy as np
# import pickle
# import create_prediction_model
# import diagnosis 
# import predict_exited_from_saved_model
import json
# import os

import subprocess
import commons_proj as cproj
from diagnostics import model_predictions
from diagnostics import numeric_inputs_summary
from diagnostics import na_percent_summary
from diagnostics import execution_time
from diagnostics import outdated_packages_list


#%% Set up variables for this script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

#http://127.0.0.1:8000/?user=aaa
@app.route('/')
def index():
    user = request.args.get('user')
    #session['user'] = user
    return "Hello " + user


#%% Prediction Endpoint
# http://127.0.0.1:8000/prediction?dirtype=test_data_path&filename=testdata.csv
# curl "http://127.0.0.1:8000/prediction?dirtype=test_data_path&filename=testdata.csv"
#@app.route("/prediction", methods=['POST','OPTIONS'])
@app.route("/prediction")
def predict():        
    #call the prediction function you created in Step 3
    # curl "http://127.0.0.1:8000/prediction?dirtype=test_data_path&filename=testdata.csv"

    # if 'user' not in session:
    #     return redirect(url_for("index"))

    dirtype  = request.args.get('dirtype', default='*', type=str)
    filename = request.args.get('filename', default='*', type=str)
    test_data = cproj.load_dataframe(dirtype, filename)
    predicted, _ = model_predictions(test_data)
    return str(predicted.tolist())

#%% Scoring Endpoint
#http://127.0.0.1:8000/scoring
#@app.route("/scoring", methods=['GET','OPTIONS'])
@app.route("/scoring")
def scoring():
    #check the score of the deployed model
    # if 'user' not in session:
    #     return redirect(url_for("index"))

    subprocess.run(['python', 'scoring.py'])
    f1_score = cproj.load_txt_file('output_model_path', 'latestscore.txt')
    f1_score = [w.replace('\n', '') for w in f1_score]
    return str(f1_score)


#%% Summary Statistics Endpoint
#http://127.0.0.1:8000/summarystats
# @app.route("/summarystats", methods=['GET','OPTIONS'])
@app.route("/summarystats")
def stats_num_inputs():
    #check the score of the deployed model
    # if 'user' not in session:
    #     return redirect(url_for("index"))

    numeric_inputs_stats = numeric_inputs_summary()
    return str(numeric_inputs_stats)

#%% Diagnostics Endpoint
#http://127.0.0.1:8000/diagnostics
#@app.route("/diagnostics", methods=['GET','OPTIONS'])
@app.route("/diagnostics")
def diags_summary():
    # if 'user' not in session:
    #     return redirect(url_for("index"))

    #check timing and percent NA values
    na_percent = na_percent_summary()
    exec_time = execution_time()
    outdated_df = outdated_packages_list()
    dict_all = {'na_percent': na_percent.values.tolist(),
                'exec_time':list(exec_time.items()),
                'packages': outdated_df.values.tolist()}

    return str(dict_all)

#%%
if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
