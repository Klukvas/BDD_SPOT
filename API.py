import email
import json
from requests_pkcs12 import get, post
from datetime import datetime
import settings
from uuid import uuid4
from bs4 import BeautifulSoup

cert_name = settings.cert_name
cert_pass = settings.cert_pass

class Auth:
    
    def __init__(self, email, password) -> None:
        self.main_url = settings.url_auth
        self.headers = { 'Content-Type': 'application/json' }
        self.email = email
        self.password = password

    def register(self, *args) -> list[str] or int or dict:
        url = f"{self.main_url}Register"
        
        if self.email == "empty" and self.password == "empty":
            payload = json.dumps({
                "email": f"",
                "password": f""
            })
        
        elif self.email == "null" and self.password == "null":
            payload = json.dumps({})
        
        elif self.password == "empty" and self.email != "empty":
            payload = json.dumps({
                "email": f"{self.email}",
                "password": f""
            })
        elif self.password != "empty" and self.email == "empty":
            payload = json.dumps({
                "email": f"",
                "password": f"{self.password}"
            })
        
        elif self.password == "null" and self.email != "null":
            payload = json.dumps({
                "email": f"{self.email}"
            })
        elif self.password != "null" and self.email == "null":
            payload = json.dumps({
                "password": f"{self.password}"
            })
        
        else:
            payload = json.dumps({
                "email": f"{self.email}",
                "password": f"{self.password}"
            })
        
        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=self.headers, data=payload)
        if args:
            return {"response": r.text, "status": r.status_code}
        else:
            if r.status_code == 200:
                try:
                    parse_resp = json.loads(r.text)['data']
                    return {
                            "token": parse_resp['token'], 
                            "refreshToken": parse_resp['refreshToken']
                        }
                except:
                    return r.text,
            else:
                return r.status_code
    
    def authenticate(self, *args) -> list[str] or int:
        url = f"{self.main_url}Authenticate"

        if self.email == "empty" and self.password == "empty":
            payload = json.dumps({
                "email": f"",
                "password": f""
            })
        
        elif self.email == "null" and self.password == "null":
            payload = json.dumps({})
        
        elif self.password == "empty" and self.email != "empty":
            payload = json.dumps({
                "email": f"{self.email}",
                "password": f""
            })
        elif self.password != "empty" and self.email == "empty":
            payload = json.dumps({
                "email": f"",
                "password": f"{self.password}"
            })
        
        elif self.password == "null" and self.email != "null":
            payload = json.dumps({
                "email": f"{self.email}"
            })
        elif self.password != "null" and self.email == "null":
            payload = json.dumps({
                "password": f"{self.password}"
            })
        
        else:
            payload = json.dumps({
                "email": f"{self.email}",
                "password": f"{self.password}"
            })

        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=self.headers, data=payload)
        if args:
            return {"response": r.text, "status": r.status_code}
        else:
            if r.status_code == 200:
                parse_resp = json.loads(r.text)['data']
                return [parse_resp['token'], parse_resp['refreshToken']] 
            else:
                return (r.status_code, r.text)
    
    def change_password(self, token, oldPassword, newPassword, *args) -> list[str] or int or dict:
        url = f"{self.main_url}ChangePassword"

        payload = json.dumps({
            "oldPassword": f"{oldPassword}",
            "newPassword": f"{newPassword}",
        })
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        
        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)
        if args:
            return {'resp':r.text, 'code': r.status_code }
        else:
            if r.status_code == 200:
                try:
                    parse_resp = json.loads(r.text)['result']
                    return {'result': parse_resp}
                except:
                    return r.text,
            else:
                return r.status_code
    
    def forgot_password(self, email) -> list[str] or int:
        url = f"{self.main_url}ForgotPassword"

        payload = json.dumps({
            "email": f"{email}",
            "deviceType": "IOS"
        })
        
        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=self.headers, data=payload)

        if r.status_code == 200:
            parse_resp = json.loads(r.text)
            return [parse_resp['result']]
        else:
            return r.status_code
    
    def password_recovery(self, password, token) -> list[str] or int:
        url = f"{self.main_url}PasswordRecovery"

        payload = json.dumps({
           "password": f"{password}",
            "token": f"{token}"
        })
        
        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=self.headers, data=payload)

        if r.status_code == 200:
            parse_resp = json.loads(r.text)
            return [parse_resp['result']]
        else:
            return r.status_code
    
    def logout(self, token) -> list[str] or int or dict:
        url = f"{self.main_url}Logout"

        payload = json.dumps({
            "token": token
        })
        
        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=self.headers, data=payload)

        if r.status_code == 200:
            try:
                parse_resp = json.loads(r.text)
                return { "response": parse_resp }
            except:
                return r.text,
        else:
            return r.status_code
    
    def refresh(self, refreshToken) -> list[str] or int or dict:
        url = f"{self.main_url}RefreshToken"

        payload = json.dumps({
            "refreshToken": refreshToken
        })
        
        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=self.headers, data=payload)

        if r.status_code == 200:
            try:
                parse_resp = json.loads(r.text)
                return { "response": parse_resp }
            except:
                return r.text,
        else:
            return r.status_code
   
class WalletHistory:

    def __init__(self) -> None:
        self.main_url = settings.url_wallet_history

    def balance(self, token) -> list[dict] or int:
        url = f"{self.main_url}balance-history"
        payload={}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            return parse_resp['data']
        else:
            return r.status_code

    def swap(self, token) -> list[dict] or int:
        url = f"{self.main_url}swap-history"
        payload={}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            hist =  parse_resp['data']
            if hist == None:
                return []
            else:
                return hist
        else:
            return r.status_code

    def trade(self, token) -> list[dict] or int:
        url = f"{self.main_url}trade-history"
        payload={}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            try:
                return parse_resp['data']
            except:
                return {'response': parse_resp}
        else:
            return r.status_code

    def operations_history(self, token, asset=None) -> dict or list[dict] or int:
        if asset:
            url = f"{self.main_url}operation-history?assetId={asset}"
        else:
            url = f"{self.main_url}operation-history"
        payload={}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            try:
                return parse_resp['data']
            except:
                return {'response': parse_resp}
        else:
            return r.status_code

class Wallet:

    def __init__(self) -> None:
        self.main_url = settings.url_wallet
        self.signalrUrl = settings.url_signalR

    def balances(self, token) -> list[dict] or int:
        url = self.signalrUrl + 'wallet/wallet-balances'
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            return parse_resp['data']['balances']
        else:
            return r.status_code
    
    def converter_map(self, asset,  token) -> list[dict] or int:
        url = f"{self.main_url}base-currency-converter-map/{asset}"
        payload={}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            return parse_resp['data']['maps']
        else:
            return r.status_code

class Swap:

    def __init__(self) -> None:
        self.main_url = settings.url_swap

    def get_quote(self, token, _from, to, fromToVol, fix) -> dict or int:
        url = f"{self.main_url}get-quote"
        if fix:
            payload = json.dumps({
                "fromAsset": f"{_from}",
                "toAsset": f"{to}",
                "fromAssetVolume": fromToVol,
                "isFromFixed": fix
            })
        else:
            payload = json.dumps({
                "fromAsset": f"{_from}",
                "toAsset": f"{to}",
                "toAssetVolume": fromToVol,
                "isFromFixed": fix
            })
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            try:
                return parse_resp['data']
            except:
                return [parse_resp]
        else:
            try:
                parse_resp =  json.loads(r.text)
                return (r.status_code, parse_resp)
            except:
                return (r.status_code, r.text)

    def execute_quote(self, token, body) -> dict or int or list:
        url = f"{self.main_url}execute-quote"
        payload = json.dumps( body )
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            try:
                return parse_resp['data']
            except:
                return [parse_resp,]
        else:
            return r.status_code

class Trading:

    def __init__(self) -> None:
        self.main_url = settings.url_trading

    def limit_order(self, token, instrumentSymbol, side, price, volume) -> dict or int:
        url = f"{self.main_url}order/create-limit-order"

        payload = json.dumps({
            "instrumentSymbol": f"{instrumentSymbol}",
            "side": f"{side}",
            "price": price,
            "volume": volume
        })

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            try:
                return parse_resp['data']
            except:
                return [parse_resp,]
        else:
            return r.status_code  
    
    def market_order(self, token, instrumentSymbol, side, volume) -> dict or list:
        url = f"{self.main_url}order/create-market-order"

        payload = json.dumps({
            "instrumentSymbol": f"{instrumentSymbol}",
            "side": f"{side}",
            "volume": volume
        })

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        parse_resp =  json.loads(r.text)
        try:
            return parse_resp['data']
        except:
            return [parse_resp, r.status_code]
    
    def cancel_order(self, token, orderId) -> dict or int:
        url = f"{self.main_url}order/cancel-order"

        payload = json.dumps({
            "orderId": f"{orderId}"
        })

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            return parse_resp
        else:
            return r.status_code  
    
    def list_order(self, token) -> list or int:
        url = f"https://wallet-api-spot.mnftx.biz/api/v1/signalr/wallet/order-list"

        payload = {}

        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            try:
                return parse_resp['data']
            except:
                return {'Response': parse_resp}
        else:
            return r.status_code  

class Transfer:

    def __init__(self):
        self.main_url = settings.url_transfer
    
    def create_transfer(self, token, phone, asset, amount) -> dict or list:
        url = f"{self.main_url}by-phone"

        uniqId = str(datetime.strftime(datetime.today(), '%m%d%H%s%f'))

        payload = json.dumps({
            "requestId": uniqId,
            "assetSymbol": asset,
            "amount": amount,
            "toPhoneNumber": phone,
            "lang": "En"
        })

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
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
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
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
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        parse_resp =  json.loads(r.text)
        try:
            return parse_resp['data']
        except:
            return [parse_resp, r.status_code]

class Blockchain:
    def __init__(self):
        self.main_url = settings.url_blockchain
    
    def withdrawal(self, token, asset, amount, address):
        url = f"{self.main_url}withdrawal"

        uniqId = uuid4()

        payload = json.dumps({
                "requestId": f"{uniqId}",
                "assetSymbol": f"{asset}",
                "amount": amount,
                "toAddress": f"{address}",
                "lang": "En"
            })

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        try:
            parse_resp =  json.loads(r.text)
            try:
                return {"operationId": parse_resp['data']['operationId'], "requestId": str(uniqId) }
            except:
                return [parse_resp, r.status_code]
        except:
            return r.status_code

class Circle:

    def __init__(self):
        self.main_url = settings.url_circle
        self.debug_url = settings.url_debug

    def get_encryption_key(self, token):
        url = f"{self.main_url}get-encryption-key"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = get(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
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
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
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
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
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

    def create_payment(self, token, encryption_data, keyId, cardId, amount=10):
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
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
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
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
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
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
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
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
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

class Verify:

    def __init__(self):
        self.main_url = settings.url_verify

    def verify_email(self,token, code):
        url = f"{self.main_url}email-verification/verify"

        payload = json.dumps({
                "code": f"{code}"
            })
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

        try:
            parse_resp =  json.loads(r.text)
            try:
                return {"data": parse_resp['result'] }
            except:
                return [parse_resp, r.status_code]
        except:
            return r.status_code   
    
    def client_data(self,token):
        url = f"https://wallet-api-uat.simple-spot.biz/api/v1/info/session-info"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = get(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers)

        try:
            parse_resp =  json.loads(r.text)
            try:
                return {"data": parse_resp['data'] }
            except:
                return [parse_resp, r.status_code]
        except:
            return r.status_code   

    def verify_withdrawal(self,token, code):
        url = f"{self.main_url}withdrawal-verification/verify?brand=simple&withdrawalProcessId={code}&code=000000"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        try:
            r = get(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.find('title').text
            return title
        except Exception as err:
            return err,
    
    def verify_transfer(self, token, code):
        url = f"{self.main_url}transfer-verification/verify?transferProcessId={code}&code=000000&brand=simple"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = get(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers)

        try:
            r = get(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.find('title').text
            return title
        except Exception as err:
            return err,


if __name__ == '__main__':
    tokens = Auth('basetestsusder@mailinator.com', 'testpassword1').authenticate()
    s = Auth('basetestsusder@mailinator.com', 'testpassword1').change_password(tokens[0], 'testpassword1','testpassword1')
    print(s)
