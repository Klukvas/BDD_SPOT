from ast import arg
import json
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

    def negative_cases_handler(func):
        def inner(self, *args):
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
            return func(self, args, reg_data=payload)

        return inner

    @negative_cases_handler
    def register(self, *args, **kwargs) -> list[str] or int or dict:
        url = f"{self.main_url}Register"
        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=self.headers, data=kwargs['reg_data'])
        if len(args[0]):
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
                    raise CantParseJSON(
                        f'''
                             Can not parse json.
                             Response from api/Register: {r.text} with status code: {r.status_code}
                             Error message: {error}
                         '''
                    )
            else:
                raise RequestError(
                    f"Negative status code from {url}: code {r.status_code}"
                )

    @negative_cases_handler
    def authenticate(self, *args, **kwargs) -> list[str] or int:
        url = f"{self.main_url}Authenticate"

        r = post(url,
                 pkcs12_filename=self.cert_name,
                 pkcs12_password=self.cert_pass,
                 verify=False,
                 headers=self.headers, data=kwargs['reg_data'])
        if len(args[0]):
            return {"response": r.text, "status": r.status_code}
        else:
            if r.status_code == 200:
                try:
                    parse_resp = json.loads(r.text)['data']
                    return [parse_resp['token'], parse_resp['refreshToken']]
                except Exception as error:
                    raise CantParseJSON(
                        f'''
                            Can not parse json.
                            Response from api/Authenticate: {r.text} with status code: {r.status_code}
                            Error message: {error}
                        '''
                    )

            else:
                raise RequestError(
                    f"Negative status code from {url}: code {r.status_code}"
                )

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
                    raise CantParseJSON(
                        f'''
                            Can not parse json.
                            Response from api/ChangePassword: {r.text} with status code: {r.status_code}
                            Error message: {error}
                        '''
                    )

            else:
                raise RequestError(
                    f"Negative status code from {url}: code {r.status_code}"
                )

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
                raise CantParseJSON(
                    f'''
                        Can not parse json.
                        Response from api/ForgotPasswordCode: {r.text} with status code: {r.status_code}
                        Error message: {error}
                    '''
                )

        else:
            raise RequestError(
                f"Negative status code from {url}: code {r.status_code}"
            )

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
                raise CantParseJSON(
                    f'''
                        Can not parse json.
                        Response from api/PasswordRecoveryCode: {r.text} with status code: {r.status_code}
                        Error message: {error}
                    '''
                )

        else:
            raise RequestError(
                f"Negative status code from {url}: code {r.status_code}"
            )

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
                raise CantParseJSON(
                    f'''
                        Can not parse json.
                        Response from api/Logout: {r.text} with status code: {r.status_code}
                        Error message: {error}
                    '''
                )

        else:
            raise RequestError(
                f"Negative status code from {url}: code {r.status_code}"
            )

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
                raise CantParseJSON(
                    f'''
                        Can not parse json.
                        Response from api/RefreshToken: {r.text} with status code: {r.status_code}
                        Error message: {error}
                    '''
                )

        else:
            raise RequestError(
                f"Negative status code from {url}: code {r.status_code}"
            )
