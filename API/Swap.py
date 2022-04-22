import json
from requests_pkcs12 import post
import settings
from API.Main import MainObj



class Swap(MainObj):

    def __init__(self) -> None:
        super().__init__()
        self.main_url = settings.url_swap

    def get_quote(self, token, _from, to, fromToVol, fix, recurringBuy: None or dict = None, *args) -> dict or int:
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
        if args:
            if args[0] == 'MIN_MAX_TESTS':
                parse_resp = json.loads(r.text)
                try:
                    return parse_resp['result']
                except:
                    return [parse_resp]
        else:
            if r.status_code == 200:
                parse_resp = json.loads(r.text)
                try:
                    return parse_resp['data']
                except:
                    return [parse_resp]
            else:
                try:
                    parse_resp = json.loads(r.text)
                    return (r.status_code, parse_resp)
                except:
                    return (r.status_code, r.text)

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
            parse_resp = json.loads(r.text)
            try:
                return parse_resp['data']
            except:
                return [parse_resp,]
        else:
            return r.status_code
