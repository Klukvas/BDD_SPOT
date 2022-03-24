import json
from requests_pkcs12 import post
import settings
from API.Main import MainObj


class Auth(MainObj):
    
    def __init__(self, email, password) -> None:
        super().__init__()
        self.main_url = settings.url_auth
        self.headers = { 'Content-Type': 'application/json' }
        self.email = email
        self.password = password

    def register(self, *args) -> list[str] or int or dict:
        url = f"{self.main_url}Register"
        
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
        
        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=self.headers, data=payload)
        if args:
            return {"response": r.text, "status": r.status_code}
        else:
            if r.status_code == 200:
                try:
                    parse_resp = json.loads(r.text)['data']
                    return {
                            "token": parse_resp['token'], 
                            "refreshToken": parse_resp['refreshToken']
                        }
                except:
                    return r.text,
            else:
                return r.status_code
    
    def authenticate(self, *args) -> list[str] or int:
        url = f"{self.main_url}Authenticate"

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

        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=self.headers, data=payload)
        if args:
            return {"response": r.text, "status": r.status_code}
        else:
            if r.status_code == 200:
                parse_resp = json.loads(r.text)['data']
                return [parse_resp['token'], parse_resp['refreshToken']] 
            else:
                return (r.status_code, r.text)
    
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
                verify = False,
                headers=headers, data=payload)
        if args:
            return {'resp':r.text, 'code': r.status_code }
        else:
            if r.status_code == 200:
                try:
                    parse_resp = json.loads(r.text)['result']
                    return {'result': parse_resp}
                except:
                    return r.text,
            else:
                return r.status_code
    
    def forgot_password(self, email) -> list[str] or int:
        url = f"{self.main_url}ForgotPassword"

        payload = json.dumps({
            "email": f"{email}",
            "deviceType": "IOS"
        })
        
        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=self.headers, data=payload)

        if r.status_code == 200:
            parse_resp = json.loads(r.text)
            return [parse_resp['result']]
        else:
            return r.status_code
    
    def password_recovery(self, password, token) -> list[str] or int:
        url = f"{self.main_url}PasswordRecovery"

        payload = json.dumps({
           "password": f"{password}",
            "token": f"{token}"
        })
        
        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=self.headers, data=payload)

        if r.status_code == 200:
            parse_resp = json.loads(r.text)
            return [parse_resp['result']]
        else:
            return r.status_code
    
    def logout(self, token) -> list[str] or int or dict:
        url = f"{self.main_url}Logout"

        payload = json.dumps({
            "token": token
        })
        
        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=self.headers, data=payload)

        if r.status_code == 200:
            try:
                parse_resp = json.loads(r.text)
                return { "response": parse_resp }
            except:
                return r.text,
        else:
            return r.status_code
    
    def refresh(self, refreshToken) -> list[str] or int or dict:
        url = f"{self.main_url}RefreshToken"

        payload = json.dumps({
            "refreshToken": refreshToken
        })
        
        r = post(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=self.headers, data=payload)

        if r.status_code == 200:
            try:
                parse_resp = json.loads(r.text)
                return { "response": parse_resp }
            except:
                return r.text,
        else:
            return r.status_code
 