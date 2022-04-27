import json
from requests_pkcs12 import get
import settings
from API.Main import MainObj
from API.Exceptions import *


class WalletHistory(MainObj):

    def __init__(self) -> None:
        super().__init__()
        self.main_url = settings.url_wallet_history

    def balance(self, token) -> list[dict] or int:
        url = f"{self.main_url}balance-history"
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url,
                pkcs12_filename=self.cert_name,
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers)

        if r.status_code == 200:
            try:
                parse_resp = json.loads(r.text)
                return parse_resp['data']
            except Exception as err:
                raise CantParseJSON(
                    f"Can not parse response from: balance-history with Error: {err}"
                )
        else:
            raise RequestError(
                f"Negative status code from {url}: code {r.status_code}"
            )
    def swap(self, token) -> list[dict] or int:
        url = f"{self.main_url}swap-history"
        payload={}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url,
                pkcs12_filename=self.cert_name,
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=headers, data=payload)

        if r.status_code == 200:
            try:
                parse_resp = json.loads(r.text)
                hist = parse_resp['data']
            except Exception as err:
                raise CantParseJSON(
                    f"Can not parse response from: balance-history with Error: {err}"
                )
            if hist is None:
                return []
            else:
                return hist
        else:
            raise RequestError(
                f"Negative status code from {url}: code {r.status_code}"
            )
    def trade(self, token) -> list[dict] or int:
        url = f"{self.main_url}trade-history"
        payload={}
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url,
                pkcs12_filename=self.cert_name,
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers, data=payload)

        if r.status_code == 200:
            parse_resp = json.loads(r.text)
            try:
                return parse_resp['data']
            except Exception as err:
                raise CantParseJSON(
                    f"Can not parse response from: balance-history with Error: {err}"
                )
        else:
            raise RequestError(
                f"Negative status code from {url}: code {r.status_code}"
            )

    def operations_history(self, token, asset=None, specific_case=False) -> dict or list[dict] or int:
        if asset:
            url = f"{self.main_url}operation-history?assetId={asset}"
        else:
            url = f"{self.main_url}operation-history"
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = get(url,
                pkcs12_filename=self.cert_name,
                pkcs12_password=self.cert_pass,
                verify=False,
                headers=headers)
        if specific_case:
            return {"response": r.text, "code": r.status_code}
        if r.status_code == 200:
            parse_resp = json.loads(r.text)
            try:
                return parse_resp['data']
            except Exception as err:
                raise CantParseJSON(
                    f"Can not parse response from: operation-history with Error: {err}"
                )
        else:
            raise RequestError(
                f"Negative status code from {url}: code {r.status_code}"
            )