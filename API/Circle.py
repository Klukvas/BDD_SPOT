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

    def create_fast_deposit(self, token, uid, currency, amount) -> None:
        enc_key = self.get_encryption_key(token)['response']
        assert 'data' in enc_key.keys(), \
            f"Expected that 'data' key will be in response. But response is: {enc_key}"
        enc_data = self.encrypt_data(token, enc_key['data']['encryptionKey'])
        assert 'data' in enc_data.keys(), \
            f"Expected that 'data' key will be in response. But response is: {enc_data}"
        added_card = self.add_card(
            token,
            enc_data['data'],
            enc_key['data']['keyId']
        )['response']
        assert 'data' in added_card.keys(), \
            f"Expected that 'data' key will be in response. But response is: {added_card}"
        deposit_result = self.create_payment(
            token=token,
            requestGuid=uid,
            encryption_data=enc_data['data'],
            keyId=enc_key['data']['keyId'],
            cardId=added_card['data']['id'],
            currency=currency,
            amount=amount
        )['response']
        assert 'data' in deposit_result.keys(), \
            f"Expected that 'data' key will be in response. But response is: {deposit_result}"
        return

    def get_encryption_key(self, token, specific_case=False):
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

        return self.parse_response(r, specific_case)

    def encrypt_data(self, token, enc_key, specific_case=False):
        url = f"{self.debug_url}circle-encrypt-data"

        payload = {
            "data": "{\"number\":\"5173375000000006\",\"cvv\": \"123\"}",
            "encryptionKey": f"{enc_key}"
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

    def add_card(self, token, encryption_data, keyId, specific_case=False):
        url = f"{self.main_url}add-card"
        requestGuid = uuid4()
        payload = {
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

    def create_payment(self, token, requestGuid, encryption_data, keyId,
                       cardId, currency='USD', amount=10, specific_case=False):
        url = f"{self.main_url}create-payment"
        payload = {
            "requestGuid": requestGuid,
            "keyId": keyId,
            "cardId": cardId,
            "amount": amount,
            "currency": "USD",
            "encryptedData": encryption_data
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

    def delete_card(self, token, cardId, specific_case=False):
        url = f"{self.main_url}delete-card"
        payload = {
            "cardId": f"{cardId}"
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

    def get_card(self, token, cardId, specific_case=False):
        url = f"{self.main_url}get-card"
        payload = {
            "cardId": f"{cardId}"
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

    def get_all_cards(self, token, specific_case=False):
        url = f"{self.main_url}get-cards-all"

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

    def add_bank_account(self, token: str, bank_country: str, billing_country: str, account_number: str,
                         iban: str, routing_number: str, guid: str, specific_case=False) -> dict:
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

        return self.parse_response(r, specific_case)

    def get_bank_account_all(self, token: str, specific_case=False) -> dict:
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

        return self.parse_response(r, specific_case)

    def delete_bank_account(self, token: str, bank_account_id: str, specific_case=False) -> dict:
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

        return self.parse_response(r, specific_case)

    def get_bank_account(self, token: str, bank_account_id: str, specific_case=False) -> dict:
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

        return self.parse_response(r, specific_case)
