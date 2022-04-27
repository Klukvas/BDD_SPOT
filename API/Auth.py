import json

from requests import Response
from requests_pkcs12 import post
import settings
from API.Main import MainObj
from API.Exceptions import *


class Auth(MainObj):

    def __init__(self, email, password) -> None:
        super().__init__()
        self.main_url = settings.url_auth
        self.headers = {'Content-Type': 'application/json'}
        self.email = email
        self.password = password

    def negative_cases_handler(self):
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
        return payload

    def register(self, specific_case=False) -> list[str] or int or dict:
        url = f"{self.main_url}Register"
        payload = self.negative_cases_handler()
        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=self.headers, data=payload)
        if specific_case:
            return {"response": r.text, "status": r.status_code}
        else:
            if r.status_code == 200:
                try:
                    parse_resp = json.loads(r.text)['data']
                    return {
                        "token": parse_resp['token'],
                        "refreshToken": parse_resp['refreshToken']
                    }
                except Exception as error:
                    raise CantParseJSON(r.url, r.text, r.status_code, error)
            else:
                raise RequestError(url, r.status_code)


    def authenticate(self, specific_case=False) -> dict:
        url: str = f"{self.main_url}Authenticate"
        payload: str = self.negative_cases_handler()
        r: Response = post(url,
                           pkcs12_filename=self.cert_name,
                           pkcs12_password=self.cert_pass,
                           verify=False,
                           headers=self.headers, data=payload)
        if specific_case:
            return {"response": r.text, "status": r.status_code}
        else:
            if r.status_code == 200:
                try:
                    parse_resp = json.loads(r.text)['data']
                    return {
                        "token": parse_resp['token'],
                        "refreshToken": parse_resp['refreshToken']
                    }
                except Exception as error:
                    raise CantParseJSON(r.url, r.text, r.status_code, error)
            else:
                raise RequestError(url, r.status_code)

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
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=headers, data=payload)
        if len(args):
            return {'resp': r.text, 'code': r.status_code}
        else:
            if r.status_code == 200:
                try:
                    parse_resp = json.loads(r.text)['result']
                    return {'result': parse_resp}
                except Exception as error:
                    raise CantParseJSON(r.url, r.text, r.status_code, error)
            else:
                raise RequestError(url, r.status_code)

    def forgot_password(self, email) -> list[str] or int:
        url = f"{self.main_url}ForgotPasswordCode"

        payload = json.dumps({
            "email": f"{email}",
            "deviceType": "IOS"
        })

        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=self.headers, data=payload)

        if r.status_code == 200:
            try:
                parse_resp = json.loads(r.text)
                return [parse_resp['result']]
            except Exception as error:
                raise CantParseJSON(r.url, r.text, r.status_code, error)
        else:
            raise RequestError(url, r.status_code)

    def password_recovery(self, password, code) -> list[str] or int:
        url = f"{self.main_url}PasswordRecoveryCode"
        payload = json.dumps({
            "email": self.email,
            "password": password,
            "code": code
        })

        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=self.headers, data=payload)

        if r.status_code == 200:
            try:
                parse_resp = json.loads(r.text)
                return [parse_resp['result']]
            except Exception as error:
                raise CantParseJSON(r.url, r.text, r.status_code, error)
        else:
            raise RequestError(url, r.status_code)

    def logout(self, token) -> list[str] or int or dict:
        url = f"{self.main_url}Logout"

        payload = json.dumps({
            "token": token
        })

        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=self.headers, data=payload)

        if r.status_code == 200:
            try:
                parse_resp = json.loads(r.text)
                return {"response": parse_resp}
            except Exception as error:
                raise CantParseJSON(r.url, r.text, r.status_code, error)
        else:
            raise RequestError(url, r.status_code)

    def refresh(self, refreshToken) -> list[str] or int or dict:
        url = f"{self.main_url}RefreshToken"

        payload = json.dumps({
            "refreshToken": refreshToken
        })

        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=self.headers, data=payload)

        if r.status_code == 200:
            try:
                parse_resp = json.loads(r.text)
                return {"response": parse_resp}
            except Exception as error:
                raise CantParseJSON(r.url, r.text, r.status_code, error)
        else:
            raise RequestError(url, r.status_code)
