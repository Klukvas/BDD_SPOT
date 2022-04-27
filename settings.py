import os
import json


def set_env_variables():
    path_to_env_file: str = os.path.join(
        os.path.dirname(
            os.getcwd()
        ),
        '.env'
    )
    with open(path_to_env_file, 'r') as f:
        for item in f.readlines():
            if "=" in item:
                variable_name, variable_data = item.split('=')
                os.environ[variable_name] = str(variable_data)


cert_name = os.environ.get('cert_name', "NOT_SET")
cert_pass = os.environ.get('cert_pass', "NOT_SET")

if cert_pass == "NOT_SET" or cert_name == "NOT_SET":
    set_env_variables()

try:
    with open('settings.json') as f:
        data = json.load(f)
except FileNotFoundError:
    path_to_env_file = os.path.join(
        os.path.dirname(
            os.getcwd()
        ),
        'settings.json'
    )
    with open(path_to_env_file, 'r') as f:
        data = json.load(f)

envs = data['env'].keys()
test_data_seted = False

for env in envs:
    if data['env'][env]['is_actual']:
        data = data['env'][env]['test_data']
        test_data_seted = True
        break

if not test_data_seted:
    raise 'Can not set settings. All "is_actual" fields are eql to false'

circle_email = data['circle_test']['email']
circle_password = data['circle_test']['password']
circle_client_id = data['circle_test']['client_id']
circle_my_bank_account_id = data['circle_test']['my_bank_account_id']
circle_not_my_bank_account_id = data['circle_test']['not_my_bank_account_id']
circle_deleted_bank_account_id = data['circle_test']['deleted_bank_account_id']
circle_invalid_bank_account_id = data['circle_test']['invalid_bank_account_id']
circle_empty_bank_accounts_email = data['circle_test']['empty_bank_accounts_email']
circle_empty_bank_accounts_password = data['circle_test']['empty_bank_accounts_password']
circle_empty_bank_accounts_client_id = data['circle_test']['empty_bank_accounts_client_id']

autoinvest_email = data['autoinvest_test']['email']
autoinvest_password = data['autoinvest_test']['password']
autoinvest_client_id = data['autoinvest_test']['client_id']
autoinvest_wallet_id = data['autoinvest_test']['wallet_id']

me_tests_email = data['me_tests']['email']
me_tests_password = data['me_tests']['password']
me_tests_client_id = data['me_tests']['client_id']
me_tests_from_phone_number = data['me_tests']['from_phone_number']
me_tests_transfer_to_phone = data['me_tests']['transfer_to_phone']
me_tests_receive_email = data['me_tests']['receive_email']
me_tests_circle_test_currency = data['me_tests']['circle_test_currency']

db_connection_string = data['db_connection_string']

#Имейл на который прихоят письма
template_tests_email = data['template_tests']['email']
template_tests_client_id = data['template_tests']['client_id']
template_tests_password = data['template_tests']['password']
template_tests_fee_amoutn = data['template_tests']['fee_amount']

template_tests_to_phone_transfer = data['template_tests']['to_phone_transfer']

auth_tests_email_for_change_password = data['auth_tests']['email_for_change_password']
auth_tests_password_for_change_password = data['auth_tests']['password_for_change_password']
auth_tests_repeat_count = data['auth_tests']['repeat_count']

url_candles = data['urls']['candles']
url_verify = data['urls']['verify']
url_auth = data['urls']['auth']
url_wallet_history = data['urls']['wallet_history']
url_wallet = data['urls']['wallet']
url_signalR = data['urls']['signalR']
url_swap = data['urls']['swap']
url_invest = data['urls']['invest']
url_trading = data['urls']['trading']
url_transfer = data['urls']['transfer']
url_blockchain = data['urls']['blockchain']
url_circle = data['urls']['circle']
url_debug = data['urls']['debug']
url_simplex = data['urls']['simplex'] 
# используються для создания квоты свопа с fixed False
balance_asssets = {
    'LTC': 1.3,
    'BTC': 0.06,
    'ETH': 0.07,
    'USD': 300,
    'EUR': 265,
    'BCH': 0.5,
    'XLM': 1500
}
# используються для создания квоты свопа с fixed True
to_balance = {
    'LTC': 0.45,
    'BTC': 0.005,
    'ETH': 0.04,
    'USD': 100,
    'EUR': 95,
    'BCH': 0.5
}

chart_data = {
    "DAY": {
        "type": 0,
        "dateFromDifferetn": 2,
        "mergeCount": 15,
        "expected_count": 96
    },
    "WEEK": {
        "type": 1,
        "dateFromDifferetn": 7,
        "mergeCount": 2,
        "expected_count": 84
    },
    "MOUNTH": {
        "type": 1,
        "dateFromDifferetn": 30,
        "mergeCount": 8,
        "expected_count": 90
    },
    "YEAR": {
        "type": 2,
        "dateFromDifferetn": 365,
        "mergeCount": 4,
        "expected_count": 92
    }
}

