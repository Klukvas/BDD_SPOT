import json
from requests_pkcs12 import post
from datetime import datetime
import settings
from API.Main import MainObj


class Transfer(MainObj):

    def __init__(self):
        super().__init__()
        self.main_url = settings.url_transfer
    
    def create_transfer(self, token, phone, asset, amount) -> dict or list:
        url = f"{self.main_url}by-phone"

        uniqId = str(datetime.strftime(datetime.today(), '%m%d%H%s%f'))
        phone_code = phone[:3]
        phone_body = phone[3:]
        payload = json.dumps({
                "requestId": uniqId,
                "assetSymbol": asset,
                "amount": amount,
                "lang": "Ru",
                "toPhoneCode": phone_code,
                "toPhoneBody": phone_body,
                "toPhoneIso": "UKR"
            })

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=headers, data=payload)

        try:
            parse_resp =  json.loads(r.text)
            try:
                return {"operationId": parse_resp['data']['operationId'], "requestId": uniqId }
            except:
                return [parse_resp, r.status_code]
        except:
            return r.status_code

    def get_transfer_info(self, token, transferId) -> dict or list:
        url = f"{self.main_url}transfer-info"

        payload = json.dumps({
            "transferId": transferId
        })

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=headers, data=payload)

        parse_resp =  json.loads(r.text)
        try:
            return parse_resp['data']
        except:
            return [parse_resp, r.status_code]

    def cancel_transfer(self, token, transferId) -> dict or list:
        url = f"{self.main_url}transfer-cancel"

        payload = json.dumps({
            "transferId": transferId
        })

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=headers, data=payload)

        parse_resp =  json.loads(r.text)
        try:
            return parse_resp['data']
        except:
            return [parse_resp, r.status_code]
