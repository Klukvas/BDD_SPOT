import time
from API.Swap import Swap
from API.WalletHistory import WalletHistory
from API.Invest import Invest
from pytest_bdd import scenarios, given, when, then, parsers
import settings
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
def get_given_arguments(scheduleType, isFromFixed, volume, fromAsset, toAsset, auth):
    return {'recurringBuy': dict(scheduleType=int(scheduleType)), 'isFromFixed': bool(isFromFixed),
            'volume': float(volume), 'fromAsset': fromAsset, 'toAsset': toAsset,
            'auth_token': auth(
                settings.autoinvest_email,
                settings.autoinvest_password
            )['token']}

@when('user create instruction (method 1)', target_fixture='executed_quote_response')
def create_instruction(given_args):
    swap_api = Swap()
    quote_response = swap_api.get_quote(given_args['auth_token'], given_args['fromAsset'], given_args['toAsset'],
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

    executed_quote_response = swap_api.execute_quote(given_args['auth_token'], quote_response)

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

@when('user create instruction (method 2)', target_fixture='executed_quote_response')
def create_instruction_2(given_args):
    swap_api = Swap()
    invest_api = Invest()
    quote_response = swap_api.get_quote(given_args['auth_token'], given_args['fromAsset'], given_args['toAsset'],
                                      given_args['volume'], given_args['isFromFixed'])

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
    assert isinstance(quote_response['recurringBuyInfo'], (type(None),)), '/get-quote recurringBuyInfo is not null'

    autoinvest_response = invest_api.create(given_args['auth_token'], quote_response['operationId'],
                                            given_args['recurringBuy']['scheduleType'])
    data = autoinvest_response['data']['data']
    print(data)
    assert data['scheduleType'] == given_args['recurringBuy']['scheduleType']
    assert check_is_datetime(data['nextExecutionTime'])
    assert data['fromAsset'] == given_args['fromAsset']
    assert data['toAsset'] == given_args['toAsset']
    if given_args['isFromFixed']:
        assert data['fromAmount'] == given_args['volume']
    else:
        assert data['toAmount'] == given_args['volume']

    executed_quote_response = swap_api.execute_quote(given_args['auth_token'], quote_response)

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
def is_instruction_appears(db_connection, executed_quote_response, given_args):
    db_connection['db_client'].session.commit()
    response = db_connection['db_client'].session.query(db_connection['recurringbuy.instructions']).filter_by(
        OriginalQuoteId=executed_quote_response['operationId']).first()
    assert response.ClientId == settings.autoinvest_client_id, "DB clientId != user's clientId"
    assert isinstance(response.CreationTime, datetime), "DB creationtime is not datetime"
    assert isinstance(response.ErrorText, type(None)), "DB errortext is not None"
    assert response.FromAmount == executed_quote_response['fromAssetVolume'], "DB fromAmount != /execute-quote fromAmount"
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
def change_instruction_execution_time(db_connection, executed_quote_response, given_args):
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
    db_connection['db_client'].session.commit()
    db_connection['db_client'].session.query(db_connection['recurringbuy.instructions']).filter_by(
        OriginalQuoteId=executed_quote_response['operationId']).update(
        {'CreationTime': needed_datetime, 'LastExecutionTime': needed_datetime})
    db_connection['db_client'].session.commit()

@then('wait till instruction executes (order appears at db)')
def wait_till_order_appears(db_connection, created_instruction_db_response, given_args, executed_quote_response):
    response = None
    retries = 0
    time.sleep(60)
    while response is None and retries < 10:
        time.sleep(30)
        db_connection['db_client'].session.commit()
        response = db_connection['db_client'].session.query(db_connection['recurringbuy.orders']).filter_by(
            InvestInstructionId=created_instruction_db_response.Id).first()
        retries += 1
    if retries == 10:
        assert False, f'Cant find order at DB by InvestInstructionId: {created_instruction_db_response.Id}'
    assert response.ClientId == settings.autoinvest_client_id, "DB clientId != user's clientId"
    assert response.BrokerId == 'jetwallet', "DB BrokerId is not jetwallet"
    assert response.WalletId == settings.autoinvest_wallet_id, "DB WalletId != given WalletId"
    if given_args['isFromFixed']:
        assert response.FromAmount == given_args['volume'], "DB fromAmount != given fromAmount"
        assert isinstance(response.ToAmount, (int, float)), "DB ToAmount is not int or float"
    else:
        assert response.ToAmount == given_args['volume'], "DB ToAmount != given ToAmount"
        assert isinstance(response.FromAmount, (int, float)), "DB FromAmount is not int or float"
    assert response.FromAsset == given_args['fromAsset'], "DB FromAsset != given FromAsset"
    assert response.ToAsset == given_args['toAsset'], "DB ToAsset != given ToAsset"
    assert isinstance(response.Price, (int, float)), "DB Price is not int or float"
    assert response.Status == 2, "DB Status != 2"
    assert isinstance(response.ExecutionTime, datetime), f"DB ExecutionTime is not datetime. Its {type(response.ExecutionTime)} - {response.ExecutionTime}"
    assert isinstance(response.ErrorText, type(None)), "DB errortext is not None"
    assert response.QuoteId != executed_quote_response['operationId'], "Recurring buy service did swap using OLD quote"
    assert isinstance(response.CreationTime, datetime), "DB CreationTime is not datetime"
    assert response.FeeAmount >= 0, "DB FeeAmount is not >= 0"
    assert response.FeeAsset in [given_args['fromAsset'], given_args['toAsset']], "DB FeeAsset is not in fromAsset or toAsset"
    assert response.FeeCoef >= 0, "DB FeeCoef is not >= 0"
    assert response.ScheduleType == given_args['recurringBuy']['scheduleType'], "DB ScheduleType is not given ScheduleType"

@then('new log has to be in the operation history')
def check_operation_history(given_args):
    data = WalletHistory().operations_history(given_args['auth_token'])
    history_log = data[0]
    # assert history_log['operationType'] == 13, '/operation-history. operationType is not 13'  # TODO: set 13 after fix
    assert history_log['swapInfo']['isSell'] is True, '/operation-history. isSell is not True'  # TODO: check why isSell sometimes False
    assert history_log['swapInfo']['sellAssetId'] == given_args['fromAsset'], '/operation-history. sellAssetId != given fromAsset'  # TODO: is that right ?
    assert history_log['swapInfo']['sellAmount'] == given_args['volume'], '/operation-history. sellAmount != given volume'
    assert history_log['swapInfo']['buyAssetId'] == given_args['toAsset'], '/operation-history. buyAssetId != toAsset'
    assert isinstance(history_log['swapInfo']['buyAmount'], (int, float)), '/operation-history. buyAmount is not int or float'
    assert history_log['swapInfo']['feeAsset'] in [given_args['fromAsset'], given_args['toAsset']], '/operation-history. feeAsset not eql to given fromAsset or toAsset'

@then('new log has to be in the balance history')
def check_balance_history(given_args):
    data = WalletHistory().balance(given_args['auth_token'])
    first_log, second_log = data[0], data[1]
    if first_log['assetSymbol'] == given_args['fromAsset']:
        assert first_log['amount'] == -given_args['volume'], '/balance-history. first-log amount != -given volume'
        assert first_log['type'] == "Swap", '/balance-history. first-log type != swap'
        assert isinstance(second_log['amount'], (int, float)), '/balance-history. second-log amount not int or float'
        assert second_log['type'] == "Swap", '/balance-history. second-log type != swap'
    elif first_log['assetSymbol'] == given_args['toAsset']:
        assert isinstance(first_log['amount'], (int, float)), '/balance-history. first-log amount not int or float'
        assert first_log['type'] == "Swap"
        assert second_log['amount'] == -given_args['volume'], '/balance-history. second-log amount != -given volume'
        assert second_log['type'] == "Swap", '/balance-history. second-log type != swap'

@then('switch off instruction')
def switch_off(given_args, created_instruction_db_response):
    invest_api = Invest()
    switch_response = invest_api.switch(given_args['auth_token'], created_instruction_db_response.Id, False)
    data = switch_response['data']['data']
    assert data['isSuccess'] is True, '/switch. isSuccess is not True'
    assert isinstance(data['errorMessage'], (type(None))), f'/switch. errorMessage is not null. It is - {data["errorMessage"]}'
    assert data['instruction']['id'] == created_instruction_db_response.Id, f'/switch. errorMessage is not null. It is - {data["errorMessage"]}'
    assert data['instruction']['clientId'] == settings.autoinvest_client_id, '/switch client_id != given client_id'
    assert data['instruction']['brokerId'] == 'jetwallet', '/switch brokerId != jetwallet'
    assert data['instruction']['walletId'] == settings.autoinvest_wallet_id, '/switch walletid != given walletid'
    assert data['instruction']['walletId'] == settings.autoinvest_wallet_id, '/switch walletid != given walletid'
    if given_args['isFromFixed']:
        assert data['instruction']['fromAmount'] == given_args['volume'], '/switch fromAmount != given volume'
    else:
        assert isinstance(data['instruction']['fromAmount'], (int, float)), '/switch fromAmount is not int or float'
    assert data['instruction']['fromAsset'] == given_args['fromAsset'], '/switch fromAsset != given fromAsset'
    assert data['instruction']['toAsset'] == given_args['toAsset'], '/switch toAsset != given toAsset'
    assert data['instruction']['status'] == 1, f'/switch status != 1. It is {data["instruction"]["status"]}'
    assert data['instruction']['scheduleType'] == given_args['recurringBuy']['scheduleType'], '/switch scheduleType != given scheduleType'
    assert check_is_datetime(data['instruction']['scheduledDateTime']), f'/switch scheduledDateTime is not datetime. It is {data["instruction"]["scheduledDateTime"]}'
    assert isinstance(data['instruction']['scheduledDayOfWeek'], (int,)), '/switch scheduledDayOfWeek is not int'
    assert isinstance(data['instruction']['scheduledDayOfMonth'], (int,)), '/switch scheduledDayOfMonth is not int'
    assert check_is_datetime(data['instruction']['creationTime']), f"/switch creationTime is not datetime. It is {data['instruction']['creationTime']}"
    assert check_is_datetime(data['instruction']['lastExecutionTime']), f"/switch lastExecutionTime is not datetime. It is {data['instruction']['lastExecutionTime']}"
    assert data['instruction']['shouldSendFailEmail'] is False, '/switch shouldSendFailEmail is not False'
    assert data['instruction']['originalQuoteId'] == created_instruction_db_response.OriginalQuoteId, '/switch originalQuoteId is not from creation step'
    assert isinstance(data['instruction']['errorText'], type(None),), f"/switch errorText is not None. It is {data['instruction']['errorText']}"
    assert check_is_datetime(data['instruction']['failureTime']), f"/switch failureTime is not datetime. It is {data['instruction']['failureTime']}"

@then(parsers.parse('instruction status changes at DB ({state})'))
def check_instruction_change(db_connection, executed_quote_response, given_args, state):
    # without commit - query returns old values - https://stackoverflow.com/questions/16586114/sqlalchemy-returns-stale-rows
    db_connection['db_client'].session.commit()
    response = db_connection['db_client'].session.query(db_connection['recurringbuy.instructions']).filter_by(
        OriginalQuoteId=executed_quote_response['operationId']).first()
    assert response.ClientId == settings.autoinvest_client_id, "DB clientId != user's clientId"
    assert isinstance(response.CreationTime, datetime), "DB creationtime is not datetime"
    assert isinstance(response.ErrorText, type(None)), "DB errortext is not None"
    assert response.FromAmount == executed_quote_response[
        'fromAssetVolume'], "DB fromAmount != /execute-quote fromAmount"
    assert response.FromAsset == executed_quote_response['fromAsset'], "DB FromAsset != /execute-quote FromAsset"
    assert isinstance(response.Id, str), "DB Id is not string"
    assert isinstance(response.LastExecutionTime, datetime), "DB LastExecutionTime is not datetime"
    assert response.OriginalQuoteId == executed_quote_response[
        'operationId'], "DB OriginalQuoteId != /execute-quote operationId"
    assert response.ScheduleType == given_args['recurringBuy']['scheduleType'], "DB ScheduleType != given ScheduleType"
    assert isinstance(response.ScheduledDateTime, datetime), "DB ScheduledDateTime is not datetime"
    assert isinstance(response.ScheduledDayOfWeek, int), "DB ScheduledDayOfWeek is not int"
    assert isinstance(response.ScheduledDayOfMonth, int), "DB ScheduledDayOfMonth is not int"
    assert response.ShouldSendFailEmail is False, "DB ShouldSendFailEmail is not False"
    if state == 'switch off':
        assert response.Status == 1, "DB Status is not 1"
    elif state == 'delete':
        assert response.Status == 2, "DB status is not 2"
    assert response.ToAsset == given_args['toAsset'], "DB ToAsset != given ToAsset"
    assert response.WalletId == settings.autoinvest_wallet_id, "DB WalletId != given WalletId"

@then(parsers.parse('wait {needed_time} minutes and check that instruction did not execute'))
def check_instruction_doesnt_execute(db_connection, created_instruction_db_response, needed_time):
    time.sleep(60*int(needed_time))
    db_connection['db_client'].session.commit()
    response = db_connection['db_client'].session.query(db_connection['recurringbuy.orders']).filter_by(
        InvestInstructionId=created_instruction_db_response.Id).first()
    assert isinstance(response, (type(None),)), 'oprder exists, expected otherwise'

@then('delete instruction')
def delete_instruction(given_args, created_instruction_db_response):
    invest_api = Invest()
    switch_response = invest_api.delete(given_args['auth_token'], created_instruction_db_response.Id)
    data = switch_response['data']['data']
    assert data['isSuccess'] is True, '/switch. isSuccess is not True'
    assert isinstance(data['errorMessage'],
                      (type(None))), f'/switch. errorMessage is not null. It is - {data["errorMessage"]}'
    assert data['instruction'][
               'id'] == created_instruction_db_response.Id, f'/switch. errorMessage is not null. It is - {data["errorMessage"]}'
    assert data['instruction']['clientId'] == settings.autoinvest_client_id, '/switch client_id != given client_id'
    assert data['instruction']['brokerId'] == 'jetwallet', '/switch brokerId != jetwallet'
    assert data['instruction']['walletId'] == settings.autoinvest_wallet_id, '/switch walletid != given walletid'
    assert data['instruction']['walletId'] == settings.autoinvest_wallet_id, '/switch walletid != given walletid'
    if given_args['isFromFixed']:
        assert data['instruction']['fromAmount'] == given_args['volume'], '/switch fromAmount != given volume'
    else:
        assert isinstance(data['instruction']['fromAmount'], (int, float)), '/switch fromAmount is not int or float'
    assert data['instruction']['fromAsset'] == given_args['fromAsset'], '/switch fromAsset != given fromAsset'
    assert data['instruction']['toAsset'] == given_args['toAsset'], '/switch toAsset != given toAsset'
    assert data['instruction']['status'] == 2, f'/switch status != 2. It is {data["instruction"]["status"]}'
    assert data['instruction']['scheduleType'] == given_args['recurringBuy'][
        'scheduleType'], '/switch scheduleType != given scheduleType'
    assert check_is_datetime(data['instruction'][
                                 'scheduledDateTime']), f'/switch scheduledDateTime is not datetime. It is {data["instruction"]["scheduledDateTime"]}'
    assert isinstance(data['instruction']['scheduledDayOfWeek'], (int,)), '/switch scheduledDayOfWeek is not int'
    assert isinstance(data['instruction']['scheduledDayOfMonth'], (int,)), '/switch scheduledDayOfMonth is not int'
    assert check_is_datetime(data['instruction'][
                                 'creationTime']), f"/switch creationTime is not datetime. It is {data['instruction']['creationTime']}"
    assert check_is_datetime(data['instruction'][
                                 'lastExecutionTime']), f"/switch lastExecutionTime is not datetime. It is {data['instruction']['lastExecutionTime']}"
    assert data['instruction']['shouldSendFailEmail'] is False, '/switch shouldSendFailEmail is not False'
    assert data['instruction'][
               'originalQuoteId'] == created_instruction_db_response.OriginalQuoteId, '/switch originalQuoteId is not from creation step'
    assert isinstance(data['instruction']['errorText'],
                      type(None), ), f"/switch errorText is not None. It is {data['instruction']['errorText']}"
    assert check_is_datetime(data['instruction'][
                                 'failureTime']), f"/switch failureTime is not datetime. It is {data['instruction']['failureTime']}"
