import settings
from API.Exceptions import *
from json.decoder import JSONDecodeError

class MainObj:

    def __init__(self) -> None:
        self.cert_name = settings.cert_name
        self.cert_pass = settings.cert_pass

    def parse_response(self, r, specific_case):
        if specific_case:
            try:
                return {"status": r.status_code, "response": r.json()}
            except JSONDecodeError:  # case when response is empty
                return {"status": r.status_code, "response": r.text}
        if r.status_code == 200:
            try:
                return {'status': r.status_code, 'response': r.json()}
            except Exception as error:
                raise CantParseJSON(r.url, r.text, r.status_code, error)
        else:
            raise RequestError(r.url, r.status_code)
