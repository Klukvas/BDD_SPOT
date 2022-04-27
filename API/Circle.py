import json
from requests_pkcs12 import get, post
from requests import Response
import settings
from uuid import uuid4
from API.Main import MainObj
from API.Exceptions import *


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
                verify=False,
                headers=headers)

        try:
            parse_resp = json.loads(r.text)
            try:
                return {"data": parse_resp['data']}
            except Exception as err:
                raise CanNotFindKey(
                    f"Response from api/get-encryption-key is not contains all needen keys. Error: {err}"
                )
        except Exception as err:
            raise CantParseJSON(
                f"Can not parse response from api/get-encryption-key. Error: {err}"
            )

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
            parse_resp = json.loads(r.text)
            try:
                return {"data": parse_resp['data']}
            except Exception as err:
                raise CanNotFindKey(
                    f"Response from api/get-encryption-key is not contains all needen keys. Error: {err}"
                )
        except Exception as err:
            raise CantParseJSON(
                f"Can not parse response from api/get-encryption-key. Error: {err}"
            )
    
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
            except Exception as err:
                raise CanNotFindKey(
                    f"Response from api/get-encryption-key is not contains all needen keys. Error: {err}"
                )
        except Exception as err:
            raise CantParseJSON(
                f"Can not parse response from api/get-encryption-key. Error: {err}"
            )

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
            parse_resp = json.loads(r.text)
            try:
                return {"data": parse_resp['data']}
            except Exception as err:
                raise CanNotFindKey(
                    f"Response from api/get-encryption-key is not contains all needen keys. Error: {err}"
                )
        except Exception as err:
            raise CantParseJSON(
                f"Can not parse response from api/get-encryption-key. Error: {err}"
            )

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
            except Exception as err:
                raise CanNotFindKey(
                    f"Response from api/get-encryption-key is not contains all needen keys. Error: {err}"
                )
        except Exception as err:
            raise CantParseJSON(
                f"Can not parse response from api/get-encryption-key. Error: {err}"
            )
    
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
            except Exception as err:
                raise CanNotFindKey(
                    f"Response from api/get-encryption-key is not contains all needen keys. Error: {err}"
                )
        except Exception as err:
            raise CantParseJSON(
                f"Can not parse response from api/get-encryption-key. Error: {err}"
            )

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
            except Exception as err:
                raise CanNotFindKey(
                    f"Response from api/get-encryption-key is not contains all needen keys. Error: {err}"
                )
        except Exception as err:
            raise CantParseJSON(
                f"Can not parse response from api/get-encryption-key. Error: {err}"
            )

    def add_bank_account(self, token: str, bank_country: str, billing_country: str, account_number: str,
                         iban: str, routing_number: str, guid: str) -> dict:
        url = f"{self.main_url}add-bank-account"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        if bank_country == "null":
            bank_country = ''

        if billing_country == "null":
            billing_country = ''

        if account_number == "null":
            account_number = ''

        if iban == "null":
            iban = ''

        if routing_number == "null":
            routing_number = ''

        if guid == "unique":
            guid = uuid4()
        elif guid == "null":
            guid = ''

        payload = {
            "requestGuid": f'{guid}',
            "accountNumber": f'{account_number}',
            "bankAddressBankName": "test test",
            "bankAddressCity": "Niger",
            "bankAddressCountry": f'{bank_country}',
            "bankAddressDistrict": "MA",
            "bankAddressLine1": "test",
            "bankAddressLine2": "test",
            "billingDetailsCity": "Niger",
            "billingDetailsCountry": f"{billing_country}",
            "billingDetailsDistrict": "MA",
            "billingDetailsLine1": "test",
            "billingDetailsLine2": "test",
            "billingDetailsName": "test",
            "billingDetailsPostalCode": "01232",
            "iban": f'{iban}',
            "routingNumber": f'{routing_number}'
        }

        r = post(url,
            pkcs12_filename=self.cert_name,
            pkcs12_password=self.cert_pass,
            verify=False,
            headers=headers, json=payload)

        if isinstance(r, Response):
            if r.status_code == 200:
                try:
                    resp = r.json()
                except:
                    raise CantParseJSON
                return {'status': r.status_code, 'data': resp}
            else:
                raise RequestError(url, r.status_code)
        else:
            raise SomethingWentWrong

    def get_bank_account_all(self, token: str) -> dict:
        url = f"{self.main_url}get-bank-account-all"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = get(url,
                pkcs12_filename=self.cert_name,
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers)

        if isinstance(r, Response):
            if r.status_code == 200:
                try:
                    resp = r.json()
                except:
                    raise CantParseJSON
                return {'status': r.status_code, 'data': resp}
            else:
                raise RequestError(url, r.status_code)
        else:
            raise SomethingWentWrong

    def delete_bank_account(self, token: str, bank_account_id: str) -> dict:
        url = f"{self.main_url}delete-bank-account"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        if bank_account_id == 'null':
            bank_account_id = ''

        payload = {
            "bankAccountId": f"{bank_account_id}"
        }

        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=headers,
                 json=payload)

        if isinstance(r, Response):
            if r.status_code == 200:
                try:
                    resp = r.json()
                except:
                    raise CantParseJSON
                return {'status': r.status_code, 'data': resp}
            else:
                raise RequestError(url, r.status_code)
        else:
            raise SomethingWentWrong

    def get_bank_account(self, token: str, bank_account_id: str) -> dict:
        url = f"{self.main_url}get-bank-account"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        if bank_account_id == 'null':
            bank_account_id = ''

        payload = {
            "bankAccountId": f"{bank_account_id}"
        }

        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=headers,
                 json=payload)

        if isinstance(r, Response):
            if r.status_code == 200:
                try:
                    resp = r.json()
                except:
                    raise CantParseJSON
                return {'status': r.status_code, 'data': resp}
            else:
                raise RequestError(url, r.status_code)
        else:
            raise SomethingWentWrong