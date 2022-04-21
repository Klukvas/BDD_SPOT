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
from dateutil.relativedelta import relativedelta
from dateutil import parser
from datetime import datetime, timezone

scenarios('../features/autoinvest.feature')

def get_utc_time():
    return datetime.now(timezone.utc)

def get_needed_datetime(days_delta=None, month_delta=None, weeks_delta=None):
    if days_delta:
        return get_utc_time() - relativedelta(days=days_delta)
    elif month_delta:
        return get_utc_time() - relativedelta(months=month_delta)
    elif weeks_delta:
        return get_utc_time() - relativedelta(weeks=weeks_delta)

def check_is_datetime(date_string):
    try:
        date = parser.parse(date_string)
        return isinstance(date, datetime)
    except:
        return False

@given(parsers.parse('scheduleType is {scheduleType}; isFromFixed is {isFromFixed}; volume is {volume}; fromAsset is {fromAsset}; toAsset is {toAsset}'), target_fixture='given_args')
def get_given_arguments(scheduleType, isFromFixed, volume, fromAsset, toAsset):
    return {'recurringBuy': dict(scheduleType=int(scheduleType)), 'isFromFixed': bool(isFromFixed),
            'volume': float(volume), 'fromAsset': fromAsset, 'toAsset': toAsset}

@when('user create instruction (method 1)', target_fixture='executed_quote_response')
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

    return executed_quote_response

@when('instruction appears in DB', target_fixture='created_instruction_db_response')
def is_instruction_appears(db_connection, recurringbuy_instructions, executed_quote_response, given_args):
    response = db_connection.session.query(recurringbuy_instructions).filter_by(OriginalQuoteId=executed_quote_response['operationId']).first()
    assert response.ClientId == settings.autoinvest_client_id, "DB clientId != user's clientId"
    assert isinstance(response.CreationTime, datetime), "DB creationtime is not datetime"
    assert isinstance(response.ErrorText, type(None)), "DB errortext is not None"
    assert response.FromAmount == given_args['volume'], "DB fromAmount != given fromAmount"
    assert response.FromAsset == executed_quote_response['fromAsset'], "DB FromAsset != /execute-quote FromAsset"
    assert isinstance(response.Id, str), "DB Id is not string"
    assert isinstance(response.LastExecutionTime, datetime), "DB LastExecutionTime is not datetime"
    assert response.OriginalQuoteId == executed_quote_response['operationId'], "DB OriginalQuoteId != /execute-quote operationId"
    assert response.ScheduleType == given_args['recurringBuy']['scheduleType'], "DB ScheduleType != given ScheduleType"
    assert isinstance(response.ScheduledDateTime, datetime), "DB ScheduledDateTime is not datetime"
    assert isinstance(response.ScheduledDayOfWeek, int), "DB ScheduledDayOfWeek is not int"
    assert isinstance(response.ScheduledDayOfMonth, int), "DB ScheduledDayOfMonth is not int"
    assert response.ShouldSendFailEmail is False, "DB ShouldSendFailEmail is not False"
    assert response.Status == 0, "DB Status is not 0"
    assert response.ToAsset == given_args['toAsset'], "DB ToAsset != given ToAsset"
    assert response.WalletId == settings.autoinvest_wallet_id, "DB WalletId != given WalletId"
    return response

@then('change execution time at DB')
def change_instruction_execution_time(db_connection, recurringbuy_instructions, executed_quote_response, given_args):
    if given_args['recurringBuy']['scheduleType'] == 1:
        needed_datetime = get_needed_datetime(days_delta=1)
    elif given_args['recurringBuy']['scheduleType'] == 2:
        needed_datetime = get_needed_datetime(weeks_delta=1)
    elif given_args['recurringBuy']['scheduleType'] == 3:
        needed_datetime = get_needed_datetime(weeks_delta=2)
    elif given_args['recurringBuy']['scheduleType'] == 4:
        needed_datetime = get_needed_datetime(month_delta=1)
    else:
        assert False, 'needed_period is not accepted'
    db_connection.session.query(recurringbuy_instructions).filter_by(
        OriginalQuoteId=executed_quote_response['operationId']).update({'CreationTime': needed_datetime})
    db_connection.session.commit()

@then('wait till instruction executes')
def wait_till_order_appears(db_connection, recurringbuy_orders, created_instruction_db_response):
    db_connection.session.query(recurringbuy_orders).filter_by()