import json
from requests_pkcs12 import get
import settings
from API.Main import MainObj
from API.Exceptions import *


class Wallet(MainObj):

    def __init__(self) -> None:
        super().__init__()
        self.main_url = settings.url_wallet
        self.signalrUrl = settings.url_signalR

    def balances(self, token, specific_case=False) -> list[dict] or int:
        url = self.signalrUrl + 'wallet/wallet-balances'
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers)

        return self.parse_response(r, specific_case)

    def converter_map(self, asset,  token, specific_case=False) -> list[dict] or int:
        url = f"{self.main_url}base-currency-converter-map/{asset}"
        payload = {}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers, json=payload)

        return self.parse_response(r, specific_case)
