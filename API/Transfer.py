import json
import uuid

from requests_pkcs12 import post
from datetime import datetime
import settings
from API.Main import MainObj
from API.Exceptions import *


class Transfer(MainObj):

    def __init__(self):
        super().__init__()
        self.main_url = settings.url_transfer

    def create_transfer(self, token, request_id, phone, asset, amount, specific_case=False) -> dict or list:
        url = f"{self.main_url}by-phone"

        phone_code = phone[:3]
        phone_body = phone[3:]
        payload = {
            "requestId": request_id,
            "assetSymbol": asset,
            "amount": amount,
            "lang": "Ru",
            "toPhoneCode": phone_code,
            "toPhoneBody": phone_body,
            "toPhoneIso": "UKR"
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

    def get_transfer_info(self, token, transferId, specific_case) -> dict or list:
        url = f"{self.main_url}transfer-info"

        payload = {
            "transferId": transferId
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

    def cancel_transfer(self, token, transferId, specific_case=False) -> dict or list:
        url = f"{self.main_url}transfer-cancel"

        payload = {
            "transferId": transferId
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
