import os
import json


def get_path(file_name):
    path = os.path.join(
        os.getcwd(),
        file_name
    )
    if os.path.exists(path):
        return path
    else:
        while not os.path.exists(path):
            path = os.path.join(
                os.path.dirname(
                    path
                ),
                file_name
            )
        return path


def set_env_variables():
    path_to_env_file: str = get_path('.env')
    with open(path_to_env_file, 'r') as f:
        for item in f.readlines():
            if "=" in item:
                variable_name, variable_data = item.split('=')
                os.environ[variable_name] = str(variable_data)


cert_name = os.environ.get('cert_name', "NOT_SET")
cert_pass = os.environ.get('cert_pass', "NOT_SET")

if cert_pass == "NOT_SET" or cert_name == "NOT_SET":
    set_env_variables()

working_directory = os.path.dirname(os.path.abspath(__file__))

openvpn_path = os.environ.get('openvpn_path', "NOT_SET")
openvpn_profile_name = os.environ.get('openvpn_profile_name', "NOT_SET")

if openvpn_path == "NOT_SET" or openvpn_profile_name == "NOT_SET":
    set_env_variables()

path_to_settings_file = get_path('settings.json')
with open(path_to_settings_file, 'r') as f:
    data = json.load(f)

envs = data['env'].keys()
test_data_seted = False

for env in envs:
    if data['env'][env]['is_actual']:
        data = data['env'][env]['test_data']
        test_data_seted = True
        break

if not test_data_seted:
    raise RuntimeError('Can not set settings. All "is_actual" fields are eql to false')

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

db_connection_string = data['db_connection_string']

base_user_data_email = data['base_user_data']['email']
base_user_data_client_id = data['base_user_data']['client_id']
base_user_data_password = data['base_user_data']['password']
base_user_data_to_phone_transfer = data['base_user_data']['to_phone_transfer']
base_user_data_fee_amount = data['base_user_data']['fee_amount']
base_user_data_referral_code = data['base_user_data']['referral_code']
base_user_data_from_phone_number = data['base_user_data']['from_phone_number']
base_user_data_transfer_to_phone = data['base_user_data']['transfer_to_phone']
base_user_data_receive_email = data['base_user_data']['receive_email']
base_user_data_circle_test_currency = data['base_user_data']['circle_test_currency']

scenarios_with_balance_change = data['scenarios_with_balance_change']

url_signalr = data['urls']['signalr']
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

