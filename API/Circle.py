import json
from requests_pkcs12 import get, post
import settings
from uuid import uuid4
from API.Main import MainObj


class Circle(MainObj):

    def __init__(self):
        super().__init__()
        self.main_url = settings.url_circle
        self.debug_url = settings.url_debug

    def get_encryption_key(self, token):
        url = f"{self.main_url}get-encryption-key"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = get(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=headers)

        try:
            parse_resp =  json.loads(r.text)
            try:
                return {"data": parse_resp['data']}
            except:
                return [parse_resp, r.status_code]
        except:
            return r.status_code

    def encrypt_data(self, token, enc_key):
        url = f"{self.debug_url}circle-encrypt-data"

        payload = json.dumps({
                "data": "{\"number\":\"4007400000000007\",\"cvv\": \"123\"}",
                "encryptionKey": f"{enc_key}"
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
                return {"data": parse_resp['data'] }
            except:
                return [parse_resp, r.status_code]
        except:
            return r.status_code
    
    def add_card(self, token, encryption_data, keyId):
        url = f"{self.main_url}add-card"
        requestGuid = uuid4()
        payload = json.dumps({
                "requestGuid": f"{requestGuid}",
                "cardName": "baseTests",
                "keyId": f"{keyId}",
                "encryptedData": f"{encryption_data}",
                "billingName": "Andrey Testovich 12",
                "billingCity": "Kyiv",
                "billingCountry": "UA",
                "billingLine1": "Khakov 56",
                "billingDistrict": "Kyiv",
                "billingPostalCode": "03146",
                "expMonth": 12,
                "expYear": 2024
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
                return {"data": parse_resp['data'] }
            except:
                return [parse_resp, r.status_code]
        except:
            return r.status_code

    def create_payment(self, token, encryption_data, keyId, cardId, currency='USD', amount=10):
        url = f"{self.main_url}create-payment"
        requestGuid = uuid4()
        payload = json.dumps({
            "requestGuid": str(requestGuid),
            "keyId": keyId,
            "cardId": cardId,
            "amount": amount,
            "currency": "USD",
            "encryptedData": encryption_data
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
                return {"data": parse_resp['data'] }
            except:
                return [parse_resp, r.status_code]
        except:
            return r.status_code

    def delete_card(self, token, cardId):
        url = f"{self.main_url}delete-card"
        payload = json.dumps({
                "cardId": f"{cardId}"
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
                return {"data": parse_resp['data'] }
            except:
                return [parse_resp, r.status_code]
        except:
            return r.status_code
    
    def get_card(self, token, cardId):
        url = f"{self.main_url}get-card"
        payload = json.dumps({
                "cardId": f"{cardId}"
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
                return {"data": parse_resp['data'] }
            except:
                return [parse_resp, r.status_code]
        except:
            return r.status_code

    def get_all_cards(self, token):
        url = f"{self.main_url}get-cards-all"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = get(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=headers)

        try:
            parse_resp =  json.loads(r.text)
            try:
                return {"data": parse_resp['data']}
            except:
                return [parse_resp, r.status_code]
        except:
            return r.status_code
