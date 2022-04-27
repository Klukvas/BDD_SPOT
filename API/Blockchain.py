import json
from requests_pkcs12 import post
import settings
from uuid import uuid4
from API.Main import MainObj
from API.Exceptions import *


class Blockchain(MainObj):
   
    def __init__(self):
        super().__init__()
        self.main_url = settings.url_blockchain
    
    def withdrawal(self, token, asset, amount, address, specific_case=False):
        url = f"{self.main_url}withdrawal"

        uniqId = uuid4()

        payload = {
                "requestId": f"{uniqId}",
                "assetSymbol": f"{asset}",
                "amount": amount,
                "toAddress": f"{address}",
                "lang": "En"
            }

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers, json=payload)

        return self.parse_response(r, specific_case)
