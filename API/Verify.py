import json
from requests_pkcs12 import get, post
import settings
from bs4 import BeautifulSoup
from API.Main import MainObj
from API.Exceptions import *


class Verify(MainObj):

    def __init__(self):
        super().__init__()
        self.main_url = settings.url_verify

    def verify_email(self, token, code, specific_case=False):
        url = f"{self.main_url}email-verification/verify"

        payload = {
                "code": f"{code}"
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
    
    def client_data(self, token, specific_case=False):
        url = f"https://wallet-api-uat.simple-spot.biz/api/v1/info/session-info"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = get(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers)

        return self.parse_response(r, specific_case)

    def verify_withdrawal(self, token, withdrawalProcessId, specific_case=False):
        url = f"{self.main_url}withdrawal-verification/verify-code"
        payload = {
            "code": "000000",
            "operationId": withdrawalProcessId,
            "brand": "simple"
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
    
    def verify_transfer(self, token, operation_id, specific_case=False):
        url = f"{self.main_url}transfer-verification/verify-code"
        payload = {
          "code": "000000",
          "operationId": operation_id,
          "brand": "simple"
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
