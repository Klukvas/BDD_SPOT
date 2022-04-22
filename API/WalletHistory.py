import json
from requests_pkcs12 import get
import settings
from API.Main import MainObj



class WalletHistory(MainObj):

    def __init__(self) -> None:
        super().__init__()
        self.main_url = settings.url_wallet_history

    def balance(self, token) -> list[dict] or int:
        url = f"{self.main_url}balance-history"
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers)

        if r.status_code == 200:
            parse_resp = json.loads(r.text)
            return parse_resp['data']
        else:
            return r.status_code

    def swap(self, token) -> list[dict] or int:
        url = f"{self.main_url}swap-history"
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
            hist =  parse_resp['data']
            if hist == None:
                return []
            else:
                return hist
        else:
            return r.status_code

    def trade(self, token) -> list[dict] or int:
        url = f"{self.main_url}trade-history"
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
            try:
                return parse_resp['data']
            except:
                return {'response': parse_resp}
        else:
            return r.status_code

    def operations_history(self, token, asset=None) -> dict or list[dict] or int:
        if asset:
            url = f"{self.main_url}operation-history?assetId={asset}"
        else:
            url = f"{self.main_url}operation-history"
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url,
                pkcs12_filename=self.cert_name,
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers)

        if r.status_code == 200:
            parse_resp = json.loads(r.text)
            try:
                return parse_resp['data']
            except:
                return {'response': parse_resp}
        else:
            return r.status_code
