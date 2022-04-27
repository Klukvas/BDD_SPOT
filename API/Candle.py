import json
from requests_pkcs12 import get
import settings
from API.Main import MainObj
from API.Exceptions import *

class Candle(MainObj):

    def __init__(self):
        super().__init__()
        self.main_url = settings.url_candles

    def get_candels(self, token, type, instrument, fromDate, toDate, mergeCount):
        url = f"{self.main_url}/{type}?Instruction={instrument}&BidOrAsk=0&FromDate={fromDate}&ToDate={toDate}&MergeCandlesCount={mergeCount}"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        r = get(url, 
                pkcs12_filename=self.cert_name, 
                pkcs12_password=self.cert_pass,
                verify = False,
                headers=headers)

        try:
            parse_resp = json.loads(r.text)
            return {"data": parse_resp, "url": url}
        except Exception as error:
            raise CantParseJSON(r.url, r.text, r.status_code, error)
