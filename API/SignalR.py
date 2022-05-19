import logging
import pprint
import time
from signalrcore.protocol.json_hub_protocol import JsonHubProtocol
from signalrcore.hub_connection_builder import HubConnectionBuilder
import settings

# Uncomment this to enable debug logging
# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)

# Add this to self.hub_connection to enable debug logging
# .configure_logging(logging.DEBUG, socket_trace=True, handler=handler) \

# Add this to hub_connection to automate reconnecting at close
# .with_automatic_reconnect({
#             "type": "interval",
#             "keep_alive_interval": 10,
#             "reconnect_interval": 5,
#             "max_attempts": 5})

# En example to add new hub parser to SignalR class:
# 1: add to init
# self.hub_connection.on("prices-base-currency", lambda response: self.get_prices_base_currency(response))
# self.prices_base_currency = []
# 2: create a function
#  def get_prices_base_currency(self, response):
#    self.prices_base_currency.append(*response)
# 3:
# Add hub to get_response_from_handled_hubs function

class SignalR:
    def __init__(self, token):
        self.token = token
        self.exit = False
        self.hub_connection = HubConnectionBuilder() \
            .with_url(settings.url_signalr, options={"verify_ssl": False, "skip_negotiation": True}) \
            .with_hub_protocol(JsonHubProtocol()).build()

        self.hub_connection.on_open(self.send_init)
        self.hub_connection.on_close(lambda: print("SignalR connection is closed"))
        self.hub_connection.on_reconnect(lambda: print("SignalR reconnection is in progress"))
        self.hub_connection.on_error(lambda msg: self.raise_on_error(msg.error))

        self.hub_connection.on("prices-base-currency", lambda response: self.get_prices_base_currency(response))
        self.prices_base_currency = []

        self.hub_connection.on("client-detail", lambda response: self.get_client_detail(response))
        self.client_detail = []

        self.hub_connection.on("market-reference", lambda response: self.get_market_reference(response))
        self.market_reference = []

        self.hub_connection.on("spot-wallet-balances", lambda response: self.get_spot_wallet_balances(response))
        self.spot_wallet_balances = []

        self.hub_connection.on("referrer-stats", lambda response: self.get_referrer_stats(response))
        self.referrer_stats = []

        self.hub_connection.on("index-details", lambda response: self.get_index_details(response))
        self.index_details = []

        self.hub_connection.on("kyc-countries", lambda response: self.get_kyc_countries(response))
        self.kyc_countries = []

        self.hub_connection.on("market-info", lambda response: self.get_market_info(response))
        self.market_info = []

        self.hub_connection.on("convert-price-settings", lambda response: self.get_convert_price_settings(response))
        self.convert_price_settings = []

        self.hub_connection.on("cards", lambda response: self.get_cards(response))
        self.cards = []

        self.hub_connection.on("recurring-buys", lambda response: self.get_recurring_buys(response))
        self.recurring_buys = []

        self.hub_connection.on("campaigns-banners", lambda response: self.get_campaigns_banners(response))
        self.campaigns_banners = []

        self.hub_connection.start()

    def send_init(self):
        self.hub_connection.send('Init', [self.token, 'er', None, None])

    def raise_on_error(self, message):
        raise Exception(f'SignalR returned an error: {message}')

    def get_prices_base_currency(self, response):
        self.prices_base_currency.append(*response)

    def get_client_detail(self, response):
        self.client_detail.append(*response)

    def get_market_reference(self, response):
        self.market_reference.append(*response)

    def get_spot_wallet_balances(self, response):
        self.spot_wallet_balances.append(*response)

    def get_referrer_stats(self, response):
        self.referrer_stats.append(*response)

    def get_index_details(self, response):
        self.index_details.append(*response)

    def get_kyc_countries(self, response):
        self.kyc_countries.append(*response)

    def get_market_info(self, response):
        self.market_info.append(*response)

    def get_convert_price_settings(self, response):
        self.convert_price_settings.append(*response)

    def get_cards(self, response):
        self.cards.append(*response)

    def get_recurring_buys(self, response):
        self.recurring_buys.append(*response)

    def get_campaigns_banners(self, response):
        self.campaigns_banners.append(*response)

    def get_response_from_handled_hubs(self):
        return {'prices-base-currency': self.prices_base_currency,
                'client-detail': self.client_detail,
                'market-reference': self.market_info,
                'spot-wallet-balances': self.spot_wallet_balances,
                'referrer-stats': self.referrer_stats,
                'index-details': self.index_details,
                'kyc-countries': self.kyc_countries,
                'market-info': self.market_info,
                'convert-price-settings': self.convert_price_settings,
                'cards': self.cards,
                'recurring-buys': self.recurring_buys,
                'campaigns.py-banners': self.campaigns_banners}

    def close(self):
        self.exit = True
        self.hub_connection.stop()


if __name__ == '__main__':
    sleep = 10
    t = 'c4dlD1tnAUizWZ2dNZcpVSIp71/i0fRF1eRx1Rd2TRcHHawviQP8WYB2kzO4T9xLfqy4n5/i2phLPghwsx2APjp6FUczfCw4XXhaNXDwzg8GR6P8SgtLW23VZ4yYfBR6+h3fGabqxwDJEtwN1Pxv/kTIR2eCm3DTMf22k6Zz0mo='
    k = SignalR(t)
    print('SignalR initialized')
    print(f'waiting {sleep}s to parse hub responses')
    time.sleep(sleep)
    pprint.pprint(k.get_response_from_handled_hubs())
