from requests_pkcs12 import post, delete
import settings
from API.Main import MainObj


class Invest(MainObj):
    def __init__(self) -> None:
        super().__init__()
        self.main_url = settings.url_invest

    def create(self, token, quote_id: str, schedule_type: int, specific_case=False):
        url = f"{self.main_url}create"
        headers = {'Authorization': f'Bearer {token}'}
        payload = {'quoteId': quote_id, 'scheduleType': schedule_type}
        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                verify=False, headers=headers, json=payload)

        return self.parse_response(r, specific_case)

    def update(self):
        raise NotImplementedError

    def switch(self, token, instruction_id: str, is_enable: bool, specific_case=False):
        url = f"{self.main_url}switch"
        headers = {'Authorization': f'Bearer {token}'}
        payload = {'instructionId': instruction_id, 'isEnable': is_enable}
        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False, headers=headers, json=payload)

        return self.parse_response(r, specific_case)

    def delete(self, token, instruction_id: str, specific_case=False):
        url = f"{self.main_url}delete"
        headers = {'Authorization': f'Bearer {token}'}
        payload = {'instructionId': instruction_id}
        r = delete(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False, headers=headers, json=payload)

        return self.parse_response(r, specific_case)
