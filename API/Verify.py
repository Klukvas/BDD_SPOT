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

    def verify_email(self, token, code):
        url = f"{self.main_url}email-verification/verify"

        payload = json.dumps({
                "code": f"{code}"
            })
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers, data=payload)

        try:
            parse_resp = json.loads(r.text)
            try:
                return {"data": parse_resp['result']}
            except Exception as err:
                raise CanNotFindKey(r.url, err)
        except Exception as err:
            raise CantParseJSON(r.url, r.text, r.status_code, err)
    
    def client_data(self, token):
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

        try:
            parse_resp =  json.loads(r.text)
            try:
                return {"data": parse_resp['data'] }
            except Exception as err:
                raise CanNotFindKey(r.url, err)
        except Exception as err:
            raise CantParseJSON(r.url, r.text, r.status_code, err)

    def verify_withdrawal(self, token, withdrawalProcessId):
        url = f"{self.main_url}withdrawal-verification/verify?brand=simple&withdrawalProcessId={withdrawalProcessId}&code=000000"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        r = get(url,
            pkcs12_filename=self.cert_name,
            pkcs12_password=self.cert_pass,
            verify=False,
            headers=headers)
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.find('title').text
            return title
        except Exception as err:
            raise ParsingError(
                f"Error of parsing response from: withdrawal-verification/verify Error: {err}"
            )
    
    def verify_transfer(self, token, code):
        url = f"{self.main_url}transfer-verification/verify?transferProcessId={code}&code=000000&brand=simple"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = get(url,
                pkcs12_filename=self.cert_name,
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers)
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.find('title').text
            return title
        except Exception as err:
            raise ParsingError(
                f"Error of parsing response from: withdrawal-verification/verify Error: {err}"
            )
