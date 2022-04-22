import json
from requests_pkcs12 import post
import settings
from API.Main import MainObj
from API.Exceptions import *

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
            parse_resp = json.loads(r.text)
            try:
                return {"result": parse_resp['result']}
            except Exception as err:
                raise CanNotFindKey(
                    f"Response from api/get-encryption-key is not contains all needen keys. Error: {err}"
                )
        except Exception as err:
            raise CantParseJSON(
                f"Can not parse response from api/get-encryption-key. Error: {err}"
            )

    