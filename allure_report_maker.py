# Put this file in the main folder of the project
# Change allure_reports_dir

import json
import os

allure_reports_dir = 'allureReport'
mypath = os.path.join(os.getcwd(), allure_reports_dir)

if not os.path.exists(mypath):
    os.makedirs(mypath)

files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f)) and '.json' in f]

for file in files:
    file_path = os.path.join(mypath, file)
    with open(file_path, 'r') as f:
        try:
            response = json.load(f)
            try:
                del response['parameters']
            except:
                continue
        except:
            print('Exception with file: ' + file)
            continue
    with open(file_path, 'w') as f:
        json.dump(response, f)
