import json
from requests_pkcs12 import get
import settings
from API.Main import MainObj
from API.Exceptions import *


class WalletHistory(MainObj):

    def __init__(self) -> None:
        super().__init__()
        self.main_url = settings.url_wallet_history

    def balance(self, token, specific_case=False):
        url = f"{self.main_url}balance-history"
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url,
                pkcs12_filename=self.cert_name,
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers)

        return self.parse_response(r, specific_case)

    def swap(self, token, specific_case) -> list[dict] or int:
        url = f"{self.main_url}swap-history"
        payload={}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url,
                pkcs12_filename=self.cert_name,
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers, json=payload)

        return self.parse_response(r, specific_case)

    def trade(self, token, specific_case=False) -> list[dict] or int:
        url = f"{self.main_url}trade-history"
        payload={}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url,
                pkcs12_filename=self.cert_name,
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers, json=payload)

        return self.parse_response(r, specific_case)

    def operations_history(self, token, asset=None, specific_case=False) -> dict or list[dict] or int:
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

        return self.parse_response(r, specific_case)
