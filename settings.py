import os
cert_name = os.environ['cert_name']
cert_pass = os.environ['cert_pass']

email = os.environ['email']
password = os.environ['password']
client_Id = os.environ['client_Id']

#1 - uat / 2 - test
env = 2
#используються для создания квоты свопа с fixed False
balance_asssets = {
    'LTC': 1.3,
    'BTC': 0.06,
    'ETH': 0.07,
    'USD': 300,
    'EUR': 265,
    'BCH': 0.5
}
#используються для создания квоты свопа с fixed True
to_balance = {
    'LTC': 0.45,
    'BTC': 0.01,
    'ETH': 0.04,
    'USD': 100,
    'EUR': 95,
    'BCH': 0.2
}