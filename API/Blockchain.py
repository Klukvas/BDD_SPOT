import json
from requests_pkcs12 import post
import settings
from uuid import uuid4
from API.Main import MainObj


class Blockchain(MainObj):
   
    def __init__(self):
        super().__init__()
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
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_name,
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
