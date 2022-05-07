import json
from requests_pkcs12 import post
import settings
from API.Main import MainObj
from API.Exceptions import *


class Swap(MainObj):

    def __init__(self) -> None:
        super().__init__()
        self.main_url = settings.url_swap

    def get_quote(self, token, _from, to, fromToVol, fix, recurringBuy=False, specific_case=False) -> dict or int:
        url = f"{self.main_url}get-quote"
        payload = {"fromAsset": _from, "toAsset": to}
        if fix:
            payload['isFromFixed'] = True
            payload["fromAssetVolume"] = fromToVol
        else:
            payload['isFromFixed'] = False
            payload['toAssetVolume'] = fromToVol
        if recurringBuy:
            payload['recurringBuy'] = recurringBuy
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers, json=payload)

        return self.parse_response(r, specific_case)

    def execute_quote(self, token, body, specific_case=False) -> dict or int or list:
        url = f"{self.main_url}execute-quote"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers, json=body)

        return self.parse_response(r, specific_case)
