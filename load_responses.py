import commons_proj as cproj
import json

if __name__ == "__main__":  
    apireturns = cproj.load_json_file('apireturns.json')
    print(json.dumps(apireturns, indent=4, sort_keys=True))
