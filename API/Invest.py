from requests_pkcs12 import post, delete
import settings
from API.Main import MainObj
from requests import Response
from API.Exceptions import *

def parse_response(r):
    if isinstance(r, Response):
        if r.status_code == 200:
            try:
                resp = r.json()
                return {'status': r.status_code, 'data': resp}
            except:
                raise CantParseJSON(str({'status': r.status_code, 'data': r.text}))
        else:
            return {'status': r.status_code, 'data': None}
            # raise RequestError(r.url, r.status_code)
    else:
        raise SomethingWentWrong

class Invest(MainObj):
    def __init__(self) -> None:
        super().__init__()
        self.main_url = settings.url_invest

    def create(self, token, quote_id: str, schedule_type: int):
        url = f"{self.main_url}create"
        headers = {'Authorization': f'Bearer {token}'}
        payload = {'quoteId': quote_id, 'scheduleType': schedule_type}
        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                verify=False, headers=headers, json=payload)

        return parse_response(r)

    def update(self):
        raise NotImplementedError

    def switch(self, token, instruction_id: str, is_enable: bool):
        url = f"{self.main_url}switch"
        headers = {'Authorization': f'Bearer {token}'}
        payload = {'instructionId': instruction_id, 'isEnable': is_enable}
        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False, headers=headers, json=payload)

        return parse_response(r)

    def delete(self, token, instruction_id: str):
        url = f"{self.main_url}delete"
        headers = {'Authorization': f'Bearer {token}'}
        payload = {'instructionId': instruction_id}
        r = delete(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False, headers=headers, json=payload)

        return parse_response(r)
