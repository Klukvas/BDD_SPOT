import json
from requests_pkcs12 import post
import settings
from API.Main import MainObj
from API.Exceptions import *


class Swap(MainObj):

    def __init__(self) -> None:
        super().__init__()
        self.main_url = settings.url_swap

    def get_quote(self, token, _from, to, fromToVol, fix, recurringBuy=False, specific_case=False) -> dict or int:
        url = f"{self.main_url}get-quote"
        payload = {"fromAsset": _from, "toAsset": to}
        if fix:
            payload['isFromFixed'] = True
            payload["fromAssetVolume"] = fromToVol
        else:
            payload['isFromFixed'] = False
            payload['toAssetVolume'] = fromToVol
        if recurringBuy:
            payload['recurringBuy'] = recurringBuy
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers, json=payload)

        if r.status_code == 200:
            try:
                parse_resp = json.loads(r.text)
            except Exception as err:
                raise CantParseJSON(
                    f"Can not parse json from api/get-quote. Error: {err}"
                )
            try:
                if specific_case:
                    return parse_resp['result']
                return parse_resp['data']
            except Exception as err:
                raise CanNotFindKey(
                    f"Can not find all keys from api/get-quote. Error: {err}"
                )
        elif r.status_code == 400 and specific_case:
            try:
                parse_resp = json.loads(r.text)
            except Exception as err:
                raise CantParseJSON(
                    f"Can not parse json from api/get-quote. Error: {err}"
                )
            try:
                return {"response": parse_resp, "code": 400}
            except Exception as err:
                raise CanNotFindKey(
                    f"Can not find all keys from api/get-quote. Error: {err}"
                )
        else:
            raise RequestError(
                f"Negative status code of response from api/get-quote. Status code: {r.status_code}"
            )

    def execute_quote(self, token, body) -> dict or int or list:
        url = f"{self.main_url}execute-quote"
        payload = json.dumps(body)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers, data=payload)

        if r.status_code == 200:
            try:
                parse_resp = json.loads(r.text)
            except Exception as err:
                raise CantParseJSON(
                    f"Can not parse json from api/execute-quote. Error: {err}"
                )
            try:
                return parse_resp['data']
            except Exception as err:
                raise CanNotFindKey(
                    f"Can not find all keys from api/execute-quote. Error: {err}"
                )
        else:
            raise RequestError(
                f"Negative status code from {url}: code {r.status_code}"
            )
