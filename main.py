import json
import os
import subprocess

def start_tests():
    with open('settings.json') as f:
        data = json.load(f)
    if data['env']['UAT']['is_actual']:
        data = data['env']['UAT']['start_settings']
    elif data['env']['TEST']['is_actual']:
        data = data['env']['TEST']['start_settings']
    else:
        raise 'Can not find setting to start. All "is_actual" fields are eql false'

    for key, value in data.items():
        if value:
            subprocess.call(f"pytest -m '{key}' --alluredir=allureReport ", shell=True)
            break
    subprocess.call(f"python allure_report_maker.py", shell=True)
    subprocess.call(f"allure serve allureReport", shell=True)

    



if __name__ == "__main__":
    start_tests()