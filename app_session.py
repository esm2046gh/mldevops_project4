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

#%% http://127.0.0.1:8000/
@app.route('/')
def index():
    if 'user' in session:
        return f'Logged in as {session["user"]}\n', True
    return 'You are not logged in', False

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['user'] = request.form['user']
#         return redirect(url_for('index'))
#     return '''
#         <form method="post">
#             <p><input type=text name=user>
#             <p><input type=submit value=Login>
#         </form>
#     '''
#

#%% login - logout
#http://127.0.0.1:8000/login?user=esm
@app.route('/login')
def login():
    session['user'] = request.args.get('user', default='*', type=str)
    return redirect(url_for('index'))

#http://127.0.0.1:8000/logout
@app.route('/logout')
def logout():
    # remove the user from the session if it's there
    session.pop('user', None)
    return redirect(url_for('index'))


#%% Prediction Endpoint
# http://127.0.0.1:8000/prediction?dirtype=test_data_path&filename=testdata.csv
# curl "http://127.0.0.1:8000/prediction?dirtype=test_data_path&filename=testdata.csv"
#@app.route("/prediction", methods=['POST','OPTIONS'])
@app.route("/prediction")
def predict():        
    #call the prediction function you created in Step 3
    if 'user' not in session:
        return redirect(url_for("index"))

    dirtype  = request.args.get('dirtype', default='*', type=str)
    filename = request.args.get('filename', default='*', type=str)
    test_data = cproj.load_dataframe(dirtype, filename)
    predicted, _ = model_predictions(test_data)
    return jsonify(predicted.tolist())

#%% Scoring Endpoint
#http://127.0.0.1:8000/scoring
#@app.route("/scoring", methods=['GET','OPTIONS'])
@app.route("/scoring")
def scoring():
    #check the score of the deployed model
    if 'user' not in session:
        return redirect(url_for("index"))

    subprocess.run(['python', 'scoring.py'])

    f1_score = cproj.load_txt_file('output_model_path', 'latestscore.txt')
    f1_score = f1_score.split()
    return jsonify(list(np.float_(f1_score)))


#%% Summary Statistics Endpoint
#http://127.0.0.1:8000/summarystats
# @app.route("/summarystats", methods=['GET','OPTIONS'])
@app.route("/summarystats")
def stats_num_inputs():
    #check the score of the deployed model
    if 'user' not in session:
        return redirect(url_for("index"))

    numeric_inputs_stats = numeric_inputs_summary()
    json_var = numeric_inputs_stats.to_json() #(orient="split")
    parsed = json.loads(json_var)
    return parsed

#%% Diagnostics Endpoint
#http://127.0.0.1:8000/diagnostics
#@app.route("/diagnostics", methods=['GET','OPTIONS'])
@app.route("/diagnostics")
def diags_summary():
    if 'user' not in session:
        return redirect(url_for("index"))

    #check timing and percent NA values
    na_percent = na_percent_summary()
    exec_time = execution_time()
    outdated_df = outdated_packages_list()
    outdated_dict = outdated_df.to_dict()
    json_var1 = na_percent.to_json()
    dict_var2 = {'execution_times': exec_time}
    dict_var3 = {'outdated_packages': outdated_dict}

    json_all = json.loads(json_var1)
    json_all.update(dict_var2)
    json_all.update(dict_var3)

    return json_all

#%%
if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
