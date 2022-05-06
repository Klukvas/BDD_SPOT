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
            payload = {
                "email": f"",
                "password": f""
            }

        elif self.email == "null" and self.password == "null":
            payload = {}

        elif self.password == "empty" and self.email != "empty":
            payload = {
                "email": f"{self.email}",
                "password": f""
            }
        elif self.password != "empty" and self.email == "empty":
            payload = {
                "email": f"",
                "password": f"{self.password}"
            }

        elif self.password == "null" and self.email != "null":
            payload = {
                "email": f"{self.email}"
            }
        elif self.password != "null" and self.email == "null":
            payload = {
                "password": f"{self.password}"
            }

        else:
            payload = {
                "email": f"{self.email}",
                "password": f"{self.password}"
            }
        return payload

    def register(self, specific_case=False) -> list[str] or int or dict:
        url = f"{self.main_url}Register"
        payload = self.negative_cases_handler()
        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=self.headers, json=payload)

        return self.parse_response(r, specific_case)

    def authenticate(self, specific_case=False) -> dict:
        url: str = f"{self.main_url}Authenticate"
        payload: dict = self.negative_cases_handler()
        r: Response = post(url,
                           pkcs12_filename=self.cert_name,
                           pkcs12_password=self.cert_pass,
                           verify=False,
                           headers=self.headers, json=payload)

        return self.parse_response(r, specific_case)

    def change_password(self, token, oldPassword, newPassword, specific_case=False) -> list[str] or int or dict:
        url = f"{self.main_url}ChangePassword"

        payload = {
            "oldPassword": f"{oldPassword}",
            "newPassword": f"{newPassword}",
        }
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=headers, json=payload)

        return self.parse_response(r, specific_case)

    def forgot_password(self, email, specific_case=False) -> list[str] or int:
        url = f"{self.main_url}ForgotPasswordCode"

        payload = {
            "email": f"{email}",
            "deviceType": "IOS"
        }

        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=self.headers, json=payload)

        return self.parse_response(r, specific_case)

    def password_recovery(self, password, code, specific_case=False) -> list[str] or int:
        url = f"{self.main_url}PasswordRecoveryCode"
        payload = {
            "email": self.email,
            "password": password,
            "code": code
        }

        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=self.headers, json=payload)

        return self.parse_response(r, specific_case)

    def logout(self, token, specific_case=False):
        url = f"{self.main_url}Logout"

        payload = {
            "token": token
        }

        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=self.headers, json=payload)

        return self.parse_response(r, specific_case)

    def refresh(self, refreshToken, specific_case=False) -> list[str] or int or dict:
        url = f"{self.main_url}RefreshToken"

        payload = {
            "refreshToken": refreshToken
        }

        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=self.headers, json=payload)

        return self.parse_response(r, specific_case)
