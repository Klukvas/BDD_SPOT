import json
from requests_pkcs12 import post
import settings
from API.Main import MainObj
from API.Exceptions import *

class Simplex(MainObj):

    def __init__(self) -> None:
        super().__init__()
        self.main_url = settings.url_simplex

    def create_payment(self, token: str, _from: str, to: str, amount: int, specific_case=False) -> dict or int:
        url = f"{self.main_url}payment"
        payload = {
            "fromCurrency": _from,
            "fromAmount": amount,
            "toAsset": to
            }
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=headers, json=payload)

        return self.parse_response(r, specific_case)

    