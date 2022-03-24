import json
from requests_pkcs12 import post
import settings
from API.Main import MainObj


class Simplex(MainObj):

    def __init__(self) -> None:
        super().__init__()
        self.main_url = settings.url_simplex

    def create_payment(self, token:str, _from:str, to:str, amount:int) -> dict or int:
        url = f"{self.main_url}payment"
        payload = json.dumps({
            "fromCurrency": _from,
            "fromAmount": amount,
            "toAsset": to
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
                return {"result": parse_resp['result']}
            except:
                return [parse_resp, r.status_code]
        except:
            return r.status_code
        
            #         return [parse_resp]
            # else:
            #     try:
            #         parse_resp =  json.loads(r.text)
            #         return (r.status_code, parse_resp)
            #     except:
            #         return (r.status_code, r.text)

    