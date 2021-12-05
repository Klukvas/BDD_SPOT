import os
import json
cert_name = os.environ['cert_name']
cert_pass = os.environ['cert_pass']
with open('settings.json') as f:
    data = json.load(f)

if data['env']['UAT']['is_actual']:
    data = data['env']['UAT']
elif data['env']['TEST']['is_actual']:
    data = data['env']['TEST']
else:
    raise 'Can not find setting to start. All "is_actual" fields are eql false'
me_tests_email = data['me_tests']['email']
me_tests_password = data['me_tests']['password']
me_tests_client_id = data['me_tests']['client_id']
me_tests_from_phone_number = data['me_tests']['from_phone_number']
me_tests_transfer_to_phone = data['me_tests']['transfer_to_phone']
me_tests_receive_email = data['me_tests']['receive_email']

#Имейл на который прихоят письма
template_tests_email = data['template_tests']['email']
template_tests_client_id = data['template_tests']['client_id']
template_tests_password = data['template_tests']['password']
template_tests_fee_amoutn = data['template_tests']['fee_amount']

template_tests_to_phone_transfer = data['template_tests']['to_phone_transfer']

url_verify =  data['urls']['verify']
url_auth = data['urls']['auth']
url_wallet_history = data['urls']['wallet_history']
url_wallet = data['urls']['wallet']
url_signalR = data['urls']['signalR']
url_swap = data['urls']['swap']
url_trading = data['urls']['trading']
url_transfer = data['urls']['transfer']
url_blockchain = data['urls']['blockchain']
url_circle = data['urls']['circle']
url_debug = data['urls']['debug']
        
# используються для создания квоты свопа с fixed False
balance_asssets = {
    'LTC': 1.3,
    'BTC': 0.06,
    'ETH': 0.07,
    'USD': 300,
    'EUR': 265,
    'BCH': 0.5
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
