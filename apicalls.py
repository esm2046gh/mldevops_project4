import requests
import subprocess
from subprocess import DEVNULL, STDOUT, check_call
import json

#Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:8000/"



#res1_greetings=subprocess.run(['curl', URL+'?user=esm'],capture_output=True).stdout
res1_greetings = subprocess.Popen('curl ' + URL +'?user=esm', shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]
print(f"- res1_greetings:\n{res1_greetings}")

#res2_prediction=subprocess.run(['curl', URL+'prediction?dirtype=test_data_path&filename=testdata.csv'],capture_output=True).stdout
res2_prediction = subprocess.Popen('curl ' + URL+'prediction?dirtype=test_data_path\&filename=testdata.csv', shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]
print(f"- res2_prediction:\n{res2_prediction}")

#res3_scoring=requests.get(URL+'scoring').content
res3_scoring = subprocess.Popen('curl ' + URL +'scoring', shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]
print(f"- res3_scoring:\n{res3_scoring}")

#res4_summarystats=requests.get(URL+'summarystats').content
res4_summarystats = subprocess.Popen('curl ' + URL +'summarystats', shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]
print(f"- res4_summarystats:\n{res4_summarystats}")

# res5_diagnostics=requests.get(URL+'diagnostics').content
res5_diagnostics = subprocess.Popen('curl ' + URL +'diagnostics', shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]
print(f"- res5_diagnostics:\n{res5_diagnostics}")

responses = {'greetings': res1_greetings,
             'prediction': res2_prediction,
             'scoring': res3_scoring,
             'summarystats': res4_summarystats,
             'diagnostics': res5_diagnostics
}

with open('apireturns.json', 'w') as fp:
    json.dump(responses, fp, indent=4)
