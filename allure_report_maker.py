# Put this file in the main folder of the project
# Change allure_reports_dir

import json
from os import listdir
from os.path import isfile, join
from pathlib import Path
allure_reports_dir = 'allureReport'
mypath = str(Path(__file__).parent.resolve()) + fr'\{allure_reports_dir}'

files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and '.json' in f]

for file in files:
    file_path = mypath + rf'\{file}'
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