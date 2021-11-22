import json
from typing import List
from requests_pkcs12 import get, post
from datetime import datetime
import settings


cert_name = settings.cert_name
cert_pass = settings.cert_pass

class Auth:
    
    def __init__(self, email, password, env) -> None:
        if env == 1:
            self.main_url = 'https://wallet-api-uat.simple-spot.biz/auth/v1/Trader/'
        else:
            self.main_url = 'https://wallet-api-test.simple-spot.biz/auth/v1/trader/'
        self.headers = { 'Content-Type': 'application/json' }
        self.email = email
        self.password = password

    def register(self) -> list[str] or int:
        url = f"{self.main_url}Register"

        payload = json.dumps({
            "email": f"{self.email}",
            "password": f"{self.password}",
        })
        
        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=self.headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)
            return [parse_resp['token'], parse_resp['refreshToken']] 
        else:
            return r.status_code
    
    def authenticate(self) -> list[str] or int:
        url = f"{self.main_url}Authenticate"

        payload = json.dumps({
            "email": f"{self.email}",
            "password": f"{self.password}",
        })

        r = post(url, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=self.headers, data=payload)

        if r.status_code == 200:
            parse_resp =  json.loads(r.text)['data']
            return [parse_resp['token'], parse_resp['refreshToken']] 
        else:
            return r.status_code

class WalletHistory:

    def __init__(self, env) -> None:
        if env == 1:
            self.main_url = "https://wallet-api-uat.simple-spot.biz/api/v1/history/wallet-history/"
        else:
            self.main_url = "https://wallet-api-test.simple-spot.biz/api/v1/history/wallet-history/"

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

    def __init__(self, env) -> None:
        if env == 1:
            self.main_url = "https://wallet-api-uat.mnftx.biz/api/v1/wallet/"
            self.signalrUrl = "https://wallet-api-uat.simple-spot.biz/api/v1/signalr/wallet/wallet-balances"
        else:
            self.signalrUrl = "https://wallet-api-test.simple-spot.biz/api/v1/signalr/wallet/wallet-balances"
            self.main_url = "https://wallet-api-test.simple-spot.biz/api/v1/wallet/"

    def balances(self, token) -> list[dict] or int:
        payload={}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(self.signalrUrl, 
                pkcs12_filename=cert_name, 
                pkcs12_password=cert_pass,
                verify = False,
                headers=headers, data=payload)

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

    def __init__(self, env) -> None:
        if env == 1:
            self.main_url = "https://wallet-api-uat.simple-spot.biz/api/v1/trading/swap/"
        else:
            self.main_url = "https://wallet-api-test.simple-spot.biz/api/v1/trading/swap/"

    def get_quote(self, token, _from='EUR', to='BTC', fromToVol=300, fix=True) -> dict or int:
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
                return [parse_resp,]
        else:
            return r.status_code

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

    def __init__(self, env) -> None:
        if env == 1:
            self.main_url = "https://wallet-api-uat.mnftx.biz/api/v1/trading/"
        else:
            self.main_url = "https://wallet-api-test.simple-spot.biz/api/v1/trading/"

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

    def __init__(self, env):
        if env == 1:
            self.main_url = 'https://wallet-api-uat.simple-spot.biz/api/v1/transfer/'
        else:
            self.main_url = 'https://wallet-api-uat.simple-spot.biz/api/v1/transfer/'
    
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
                return {"transferId": parse_resp['data']['operationId'], "requestId": uniqId }
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

if __name__ == '__main__':
    tokens = Auth('basetestsusder@mailinator.com', 'testpassword1', 1 ).authenticate()
    print(tokens)
    s = WalletHistory(1).operations_history(tokens[0])
    print(s)
