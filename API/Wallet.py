import json
from requests_pkcs12 import get
import settings
from API.Main import MainObj



class Wallet(MainObj):

    def __init__(self) -> None:
        super().__init__()
        self.main_url = settings.url_wallet
        self.signalrUrl = settings.url_signalR

    def balances(self, token) -> list[dict] or int:
        url = self.signalrUrl + 'wallet/wallet-balances'
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=headers)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            return parse_resp['data']['balances']
        else:
            return r.status_code
    
    def converter_map(self, asset,  token) -> list[dict] or int:
        url = f"{self.main_url}base-currency-converter-map/{asset}"
        payload={}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            return parse_resp['data']['maps']
        else:
            return r.status_code