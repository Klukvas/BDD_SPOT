import json
from API.WalletHistory import WalletHistory
from API.Invest import Invest
from API.Swap import Swap
from API.Auth import Auth
from API.Wallet import Wallet
from API.Exceptions import RequestError, SomethingWentWrong, CantParseJSON
from pytest_bdd import scenarios, given, when, then, parsers
from time import sleep
import settings
import inspect
from dateutil import parser
from datetime import datetime

scenarios('../features/autoinvest.feature')

def check_is_datetime(date_string):
    try:
        date = parser.parse(date_string)
        return isinstance(date, datetime)
    except:
        return False

@given('scheduleType is {scheduleType}; isFromFixed is {isFromFixed}; volume is {volume}; fromAsset is {fromAsset}; toAsset is {toAsset}', target_fixture='given_args')
def get_given_arguments(scheduleType, isFromFixed, volume, fromAsset, toAsset):
    return {'recurringBuy': dict(scheduleType=int(scheduleType)), 'isFromFixed': bool(isFromFixed),
            'volume': float(volume), 'fromAsset': fromAsset, 'toAsset': toAsset}

@when('user create instruction (method 1)', target_fixture='operation_id')
def create_instruction(auth, given_args):
    token = auth(settings.autoinvest_email, settings.autoinvest_password)
    swap_api = Swap()
    quote_response = swap_api.get_quote(token, given_args['fromAsset'], given_args['toAsset'],
                                      given_args['volume'], given_args['isFromFixed'],
                                      given_args['recurringBuy'])

    assert type(quote_response['operationId']) == str, '/get-quote. operationId is not string'
    assert quote_response['fromAsset'] == given_args['fromAsset'], '/get-quote. response fromAsset != given fromAsset'
    assert quote_response['toAsset'] == given_args['toAsset'], '/get-quote. response toAsset != given toAsset'
    assert isinstance(quote_response['price'], (float, int)), '/get-quote. price is not float or int'
    assert quote_response['isFromFixed'] == given_args['isFromFixed'], '/get-quote. response isFromFixed != given isFromFixed'
    assert quote_response['actualTimeInSecond'] >= 0, '/get-quote. response actualTimeInSecond != >=0'
    assert quote_response['feePercentage'] >= 0, '/get-quote. response feePercentage != >=0'
    assert quote_response['feeAmount'] >= 0, '/get-quote. response feeAmount != >=0'
    assert quote_response['feeAsset'] in [given_args['fromAsset'], given_args['toAsset']], '/get-quote. response feeAsset not in given fromAsset or toAsset'
    if given_args['isFromFixed']:
        assert quote_response['fromAssetVolume'] == given_args['volume'], '/get-quote. response fromAssetVolume != given fromAssetVolume'
        assert isinstance(quote_response['toAssetVolume'], (float, int)), '/get-quote. response fromAssetVolume != given fromAssetVolume'
    else:
        assert isinstance(quote_response['fromAssetVolume'], (float, int)), '/get-quote. response fromAssetVolume != given fromAssetVolume'
        assert quote_response['toAssetVolume'] == given_args['volume'], '/get-quote. response fromAssetVolume != given fromAssetVolume'

    assert quote_response['recurringBuyInfo']['scheduleType'] == given_args['recurringBuy']['scheduleType'], '/get-quote. scheduleType from response != scheduleType from request'
    assert check_is_datetime(quote_response['recurringBuyInfo']['nextExecutionTime']), f'/get-quote. nextExecutionTime from response is not datetime. Its - {quote_response["recurringBuyInfo"]["nextExecutionTime"]}'

    executed_quote_response = swap_api.execute_quote(token, quote_response)

    assert executed_quote_response['isExecuted'] is True, '/execute-quote. isExecuted is not True'
    assert executed_quote_response['operationId'] == quote_response['operationId'], '/execute-quote. operationId is not /get-quote operationId'
    assert executed_quote_response['fromAsset'] == given_args['fromAsset'], '/execute-quote. response fromAsset != given fromAsset'
    assert executed_quote_response['toAsset'] == given_args['toAsset'], '/execute-quote. response toAsset != given toAsset'
    assert executed_quote_response['price'] == quote_response['price'], '/execute-quote. price from response != /get-quote price'
    assert executed_quote_response['isFromFixed'] == given_args['isFromFixed'], '/execute-quote. response isFromFixed != given isFromFixed'
    if given_args['isFromFixed']:
        assert executed_quote_response['fromAssetVolume'] == given_args['volume'], '/execute-quote. response fromAssetVolume != given fromAssetVolume'
        assert isinstance(executed_quote_response['toAssetVolume'], (float, int)), '/execute-quote. response fromAssetVolume != given fromAssetVolume'
    else:
        assert isinstance(executed_quote_response['fromAssetVolume'], (float, int)), '/execute-quote. response fromAssetVolume != given fromAssetVolume'
        assert executed_quote_response['toAssetVolume'] == given_args['volume'], '/execute-quote. response fromAssetVolume != given fromAssetVolume'

    return executed_quote_response['operationId']

@when('instruction appears in DB')
def is_instruction_appears(db_connection, recurringbuy_instructions, operation_id):
    response = db_connection.session.query(recurringbuy_instructions).filter_by(OriginalQuoteId=operation_id).first()
    assert response.