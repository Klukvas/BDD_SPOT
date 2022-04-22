from API.WalletHistory import WalletHistory
from API.Circle import Circle
from API.Wallet import Wallet
from API.Exceptions import RequestError, SomethingWentWrong, CantParseJSON
from pytest_bdd import scenarios, given, when, then, parsers
from time import sleep
import settings
import inspect


scenarios('../features/circle.feature')

@given('User get encryption key', target_fixture="get_enc_key")
def get_enc_key(auth):
    token = auth(settings.me_tests_email, settings.me_tests_password)
    enc_key = Circle().get_encryption_key(token)
    assert type(enc_key) == dict, f"Expected: type == dict\nReturned: {type(enc_key)}"
    assert len(enc_key['data'].keys()) == 2, f"Expected that enc key object has 2 keys but returned: {len(enc_key['data'].keys())}"
    return [token, enc_key['data']]

@given('User encrypt data of his card', target_fixture="enc_data")
def enc_data(get_enc_key):
    enc_data = Circle().encrypt_data(get_enc_key[0], get_enc_key[1]['encryptionKey'])
    assert type(enc_data) == dict, f'Expected type == dict, but returned: {enc_data}'
    assert type(enc_data['data']) == str, f"Expected type == str, but returned: {type(enc_data['data'])}"
    return enc_data

@when('User add new card', target_fixture='add_card')
def add_card(enc_data, get_enc_key):
    card_data = Circle().add_card(
        get_enc_key[0],
        enc_data['data'],
        get_enc_key[1]['keyId']
    )
    assert type(card_data) == dict, f'Expected type == dict. Returned: {card_data}'
    assert all(
            key in card_data['data']
            for key in [
                        "id","cardName","last4","network",
                        "expMonth","expYear","status",
                        "errorCode","isActive","createDate",
                        "updateDate"
                    ]
        ), f"Expected that card data has all keys of ['id','cardName','last4','network','expMonth','expYear','status','errorCode','isActive','createDate','updateDate']\nBut card data == {card_data['data']}"
    assert card_data['data']['status'] == 0, f"Expected card_data['data']['status'] == {0} but returned: {card_data['data']['status']}"
    return card_data['data']

@when('user add bank account', target_fixture="add_bank_account_response")
def add_bank_account(auth, bank_country, billing_country, account_number, routing_number, iban, guid):
    token = auth(settings.circle_email, settings.circle_password)
    try:
        response = Circle().add_bank_account(token, bank_country, billing_country,
                                             account_number, iban, routing_number, guid)
        return response
    except RequestError:
        assert 1 == 0, 'Cant send add_bank_account request'
    except CantParseJSON:
        assert 1 == 0, 'Cant parse json from add_bank_account response'
    except SomethingWentWrong:
        assert 1 == 0, 'Something went wrong while sending add_bank_account request'

@then('User create deposit via card', target_fixture="create_deposit")
def create_deposit(add_card, get_enc_key, enc_data):
    sleep(5)
    deposit = Circle().create_payment(
        get_enc_key[0],
        enc_data['data'],
        get_enc_key[1]['keyId'],
        add_card['id'],
        settings.me_tests_circle_test_currency
    )
    assert type(deposit) == dict, f'Expected type dict. Retrurned: {deposit}'
    assert deposit['data']['status'] == 0, f"Expected deposit['data']['status'] == {0} but returned: {deposit['data']['status']}"
    return deposit['data']

@then('User has new record in operation history', target_fixture="check_op")
def check_op(get_enc_key, create_deposit):
    counter = 0
    while True:
        sleep(5)
        counter += 1
        op_history = WalletHistory().operations_history(get_enc_key[0])
        assert type(op_history) == list
        deposit = list(
            filter(
                lambda x: create_deposit['depositId'] in x['operationId'],
                op_history
            )
        )
        if len(deposit):
            if deposit[0]['status'] == 0 and \
                deposit[0]['balanceChange'] != 0:
                break
        elif counter > 5:
            raise ValueError(f'Can not find operations({create_deposit["depositId"]}) with status 0 for 15 seconds\nop_history: {deposit}') 
    assert len(deposit) == 1, f'Expected that operationId of transfer will be unique but gets:\nrequestId: {create_deposit["data"]["depositId"]}\n{deposit}\n'
    assert deposit[0]['operationType'] == 0, f"Expected deposit in operation history has operationType: 0. But returned: {deposit[0]['operationType']}"
    assert deposit[0]['assetId'] == 'USD', f"Expected deposit in operation history has assetId: USD. But returned: {deposit[0]['assetId']}"
    assert deposit[0]['balanceChange'] == deposit[0]['depositInfo']['depositAmount'], f"Expected deposit.balanceChange are eql to deposit.depositInfo.depositAmount. Bur returned:\ndeposit.balanceChange:{deposit[0]['balanceChange']} deposit.depositInfo.depositAmount: {deposit[0]['depositInfo']['depositAmount']}"
    assert deposit[0]['status'] == 0, f"Expected that status of deposit are eql to 0. But returned: {deposit[0]['status']}"
    assert type(deposit[0]['depositInfo']) == dict, f"Expected that type of deposit.depositInfo are eqk ti dict. But returned: {type(deposit[0]['depositInfo'])}"
    return deposit

@then('User`s balance is changed')
def check_balance_changed(get_enc_key, check_op):
    new_balances = Wallet().balances(get_enc_key[0])
    usd_balance = list(
        filter(
            lambda x: x['assetId'] == 'USD',
            new_balances
        )
    )
    assert len(usd_balance) == 1, f"Expected than user has USD balance"
    assert usd_balance[0]['balance'] == check_op[0]['newBalance'], f"Expected that new user`s balance: {usd_balance[0]['balance']}, but returned: {check_op[0]['newBalance']}"

@then('User delete his card')
def delete_card(get_enc_key, add_card):
    deleted_card = Circle().delete_card(get_enc_key[0], add_card['id'])
    assert deleted_card['data']['deleted'] == True, f"Expected that "
    all_cards = Circle().get_all_cards(get_enc_key[0])
    assert len(
        list(
            filter(
                lambda cards: add_card['id'] == cards['id'],
                all_cards['data']
            )
        )
    ) == 0


@given(parsers.parse('bank_country is {bank_country}; billing_country is {billing_country}; account_number is {account_number}; iban is {iban}; routing_number is {routing_number}; guid is {guid}'), target_fixture="variables_dict")
def get_variables(bank_country, billing_country, account_number, iban, routing_number, guid):
    return {'bank_country': bank_country, 'billing_country': billing_country, 'account_number': account_number,
            'iban': iban, 'routing_number': routing_number, 'guid': guid}

@when('user add bank account', target_fixture="response")
def add_bank_account(auth, variables_dict):
    token = auth(settings.circle_email, settings.circle_password)
    try:
        response = Circle().add_bank_account(token, variables_dict['bank_country'], variables_dict['billing_country'],
                                             variables_dict['account_number'], variables_dict['iban'],
                                             variables_dict['routing_number'], variables_dict['guid'])
        return response
    except RequestError:
        assert 1 == 0, f'Cant send {inspect.stack()[0][3]} request'
    except CantParseJSON:
        assert 1 == 0, f'Cant parse json from {inspect.stack()[0][3]} response'
    except SomethingWentWrong:
        assert 1 == 0, f'Something went wrong while sending {inspect.stack()[0][3]} request'

@then(parsers.parse('response status code has to be equals to {status_code}'))
def check_response_status_code(status_code, response):
    response_status_code = response['status']
    assert int(status_code) == int(response_status_code), f'status code is different from expected. Expected {status_code}'

@then('response must contains bank account info')
def check_add_bank_account_response_data(variables_dict, response):
    resp = response['data']
    assert resp['result'] == 'OK', f'add_bank_account response is not ok. Result is {resp["result"]}, expected OK'
    response_data = resp['data']
    assert isinstance(response_data['id'], str), f'add_bank_account response is not ok. Id is {response_data["id"]}, expected str'
    assert isinstance(response_data['brokerId'], str), f'add_bank_account response is not ok. BrokerId is {response_data["brokerId"]}, expected str'
    assert response_data['clientId'] == settings.circle_client_id, f'add_bank_account response is not ok. ClientId is {response_data["clientId"]}, expected {settings.circle_client_id}'
    assert isinstance(response_data['bankAccountId'], str), f'add_bank_account response is not ok. BankAccountId is {response_data["bankAccountId"]}, expected str'
    assert isinstance(response_data['bankAccountStatus'], int), f'add_bank_account response is not ok. BankAccountId is {response_data["bankAccountId"]}, expected int'
    assert isinstance(response_data['description'], str), f'add_bank_account response is not ok. Description is {response_data["description"]}, expected str'
    assert isinstance(response_data['trackingRef'], str), f'add_bank_account response is not ok. TrackingRef is {response_data["trackingRef"]}, expected str'
    assert isinstance(response_data['fingerPrint'], str), f'add_bank_account response is not ok. FingerPrint is {response_data["fingerPrint"]}, expected str'
    assert response_data['billingDetailsName'] == 'test', f'add_bank_account response is not ok. BillingDetailsName is {response_data["billingDetailsName"]}, expected "test"'
    assert response_data['billingDetailsCity'] == 'Niger', f'add_bank_account response is not ok. BillingDetailsCity is {response_data["billingDetailsCity"]}, expected "Boston"'
    assert response_data['billingDetailsCountry'] == variables_dict['billing_country'], f'add_bank_account response is not ok. BillingDetailsCountry is {response_data["billingDetailsCountry"]}, expected "{variables_dict["billing_country"]}"'
    assert response_data['billingDetailsLine1'] == 'test', f'add_bank_account response is not ok. BillingDetailsLine1 is {response_data["billingDetailsLine1"]}, expected "test"'
    assert response_data['billingDetailsLine2'] == 'test', f'add_bank_account response is not ok. BillingDetailsLine2 is {response_data["billingDetailsLine2"]}, expected "test"'
    assert response_data['billingDetailsDistrict'] == 'MA', f'add_bank_account response is not ok. BillingDetailsDistrict is {response_data["billingDetailsDistrict"]}, expected "MA"'
    assert response_data['billingDetailsPostalCode'] == '01232', f'add_bank_account response is not ok. BillingDetailsPostalCode is {response_data["billingDetailsPostalCode"]}, expected "01234"'
    assert isinstance(response_data['bankAddressBankName'], str), f'add_bank_account response is not ok. BankAddressBankName is {response_data["bankAddressBankName"]}, expected str'
    assert isinstance(response_data['bankAddressCity'], str), f'add_bank_account response is not ok. BankAddressCity is {response_data["bankAddressCity"]}, expected str'
    assert response_data['bankAddressCountry'] == variables_dict['bank_country'], f'add_bank_account response is not ok. BankAddressCountry is {response_data["bankAddressCountry"]}, expected "{variables_dict["bank_country"]}"'
    assert response_data['bankAddressLine1'] == 'test', f'add_bank_account response is not ok. BankAddressLine1 is {response_data["bankAddressLine1"]}, expected "test"'
    assert response_data['bankAddressLine2'] == 'test', f'add_bank_account response is not ok. BankAddressLine2 is {response_data["bankAddressLine2"]}, expected "test"'
    assert response_data['bankAddressDistrict'] == 'MA', f'add_bank_account response is not ok. BankAddressDistrict is {response_data["bankAddressDistrict"]}, expected "MA"'
    assert response_data['error'] is None, f'add_bank_account response is not ok. Error is {response_data["error"]}, expected "null"'
    assert response_data['isActive'] is True, f'add_bank_account response is not ok. IsActive is {response_data["isActive"]}, expected "true"'
    assert isinstance(response_data['createDate'], str), f'add_bank_account response is not ok. CreateDate is {response_data["createDate"]}, expected str'
    assert isinstance(response_data['updateDate'], str), f'add_bank_account response is not ok. UpdateDate is {response_data["updateDate"]}, expected str'

    if variables_dict['iban'] == 'null':
        assert response_data['iban'] is None, f'add_bank_account response is not ok. Iban is {response_data["iban"]}, expected "null"'
    else:
        assert response_data['iban'] == variables_dict['iban'], f'add_bank_account response is not ok. Iban is {response_data["iban"]}, expected "{variables_dict["iban"]}"'
    if variables_dict['account_number'] == 'null':
        assert response_data['accountNumber'] is None, f'add_bank_account response is not ok. AccountNumber is {response_data["accountNumber"]}, expected "null"'
    else:
        assert response_data['accountNumber'] == variables_dict['account_number'], f'add_bank_account response is not ok. AccountNumber is {response_data["accountNumber"]}, expected {variables_dict["account_number"]}'
    if variables_dict['routing_number'] == 'null':
        assert response_data['routingNumber'] is None, f'add_bank_account response is not ok. RoutingNumber is {response_data["routingNumber"]}, expected "null"'
    else:
        assert response_data['routingNumber'] == variables_dict['routing_number'], f'add_bank_account response is not ok. RoutingNumber is {response_data["routingNumber"]}, expected {variables_dict["routing_number"]}'

########################################################################################################################
@given(parsers.parse('user send request to parse existed bank_account_id ({count})'), target_fixture='resp')
def get_all_bank_accounts(auth, count):
    if count == '>=1':
        token = auth(settings.circle_email, settings.circle_password)
    elif count == '0':
        token = auth(settings.circle_empty_bank_accounts_email, settings.circle_empty_bank_accounts_password)
    try:
        response = Circle().get_bank_account_all(token)
        response['token'] = token
        response['accounts_count'] = len(response['data']['data'])
        try:
            response['bankaccountid_to_delete'] = response['data']['data'][-1]['bankAccountId']
        except IndexError:
            pass
        return response
    except RequestError:
        assert 1 == 0, f'Cant send {inspect.stack()[0][3]} request'
    except CantParseJSON:
        assert 1 == 0, f'Cant parse json from {inspect.stack()[0][3]} response'
    except SomethingWentWrong:
        assert 1 == 0, f'Something went wrong while sending {inspect.stack()[0][3]} request'

@when(parsers.parse("user send request to get all bank accounts ({count})"), target_fixture='response')
def get_all_bank_accounts_1(auth, count):
    if count == '>=1':
        token = auth(settings.circle_email, settings.circle_password)
    elif count == '0':
        token = auth(settings.circle_empty_bank_accounts_email, settings.circle_empty_bank_accounts_password)
    try:
        response = Circle().get_bank_account_all(token)
        response['token'] = token
        response['accounts_count'] = len(response['data']['data'])
        try:
            response['bankaccountid_to_delete'] = response['data']['data'][-1]['bankAccountId']
        except IndexError:
            pass
        return response
    except RequestError:
        assert 1 == 0, f'Cant send {inspect.stack()[0][3]} request'
    except CantParseJSON:
        assert 1 == 0, f'Cant parse json from {inspect.stack()[0][3]} response'
    except SomethingWentWrong:
        assert 1 == 0, f'Something went wrong while sending {inspect.stack()[0][3]} request'

@then('response must contains info about all bank accounts')
def check_all_bank_accounts(response):
    resp = response['data']
    assert resp['result'] == 'OK', f'get-bank-account-all response is not ok. Result is {resp["result"]}, expected OK'
    response_data = resp['data']
    assert len(response_data) > 0, f'get-bank-account-all response is not ok. Response contains {len(response_data)} bank accounts expected >0'
    for account in response_data:
        assert isinstance(account['id'], str), f'get-bank-account-all response is not ok. Id is {account["id"]}, expected str'
        assert isinstance(account['brokerId'], str), f'get-bank-account-all response is not ok. BrokerId is {account["brokerId"]}, expected str'
        assert account['clientId'] == settings.circle_client_id, f'get-bank-account-all response is not ok. ClientId is {account["clientId"]}, expected {settings.circle_client_id}'
        assert isinstance(account['bankAccountId'], str), f'get-bank-account-all response is not ok. BankAccountId is {account["bankAccountId"]}, expected str'
        assert isinstance(account['bankAccountStatus'], int), f'get-bank-account-all response is not ok. BankAccountId is {account["bankAccountId"]}, expected int'
        assert isinstance(account['description'], str), f'get-bank-account-all response is not ok. Description is {account["description"]}, expected str'
        assert isinstance(account['trackingRef'], str), f'get-bank-account-all response is not ok. TrackingRef is {account["trackingRef"]}, expected str'
        assert isinstance(account['fingerPrint'], str), f'get-bank-account-all response is not ok. FingerPrint is {account["fingerPrint"]}, expected str'
        assert isinstance(account['billingDetailsName'], str), f'get-bank-account-all response is not ok. BillingDetailsName is {account["billingDetailsName"]}, expected str'
        assert isinstance(account['billingDetailsCity'], str), f'get-bank-account-all response is not ok. BillingDetailsCity is {account["billingDetailsCity"]}, expected str'
        assert isinstance(account['billingDetailsCountry'], str), f'get-bank-account-all response is not ok. BillingDetailsCountry is {account["billingDetailsCountry"]}, expected str'
        assert isinstance(account['billingDetailsLine1'], (type(None), str)), f'get-bank-account-all response is not ok. BillingDetailsLine1 is {account["billingDetailsLine1"]}, expected str'
        assert isinstance(account['billingDetailsLine2'], (type(None), str)), f'get-bank-account-all response is not ok. BillingDetailsLine2 is {account["billingDetailsLine2"]}, expected str'
        assert isinstance(account['billingDetailsDistrict'], str), f'get-bank-account-all response is not ok. BillingDetailsDistrict is {account["billingDetailsDistrict"]}, expected str'
        assert isinstance(account['billingDetailsPostalCode'], str), f'get-bank-account-all response is not ok. BillingDetailsPostalCode is {account["billingDetailsPostalCode"]}, expected str'
        assert isinstance(account['bankAddressBankName'], str), f'get-bank-account-all response is not ok. BankAddressBankName is {account["bankAddressBankName"]}, expected str'
        assert isinstance(account['bankAddressCity'], str), f'get-bank-account-all response is not ok. BankAddressCity is {account["bankAddressCity"]}, expected str'
        assert isinstance(account['bankAddressCountry'], str), f'get-bank-account-all response is not ok. BankAddressCountry is {account["bankAddressCountry"]}, expected str'
        assert isinstance(account['bankAddressLine1'], (type(None), str)), f'get-bank-account-all response is not ok. BankAddressLine1 is {account["bankAddressLine1"]}, expected str'
        assert isinstance(account['bankAddressLine2'], (type(None), str)), f'get-bank-account-all response is not ok. BankAddressLine2 is {account["bankAddressLine2"]}, expected str'
        assert isinstance(account['bankAddressDistrict'], str), f'get-bank-account-all response is not ok. BankAddressDistrict is {account["bankAddressDistrict"]}, expected str'
        assert account['error'] is None, f'get-bank-account-all response is not ok. Error is {account["error"]}, expected "null"'
        assert account['isActive'] is True, f'get-bank-account-all response is not ok. IsActive is {account["isActive"]}, expected "true"'
        assert isinstance(account['createDate'], str), f'get-bank-account-all response is not ok. CreateDate is {account["createDate"]}, expected str'
        assert isinstance(account['updateDate'], str), f'get-bank-account-all response is not ok. UpdateDate is {account["updateDate"]}, expected str'
        assert account['iban'] is None or isinstance(account['iban'], str), f'get-bank-account-all response is not ok. Iban is {account["iban"]}, expected "null"'
        assert account['accountNumber'] is None or isinstance(account['accountNumber'], str), f'get-bank-account-all response is not ok. AccountNumber is {account["accountNumber"]}, expected "null" or "str"'
        assert account['routingNumber'] is None or isinstance(account['routingNumber'], str), f'get-bank-account-all response is not ok. RoutingNumber is {account["routingNumber"]}, expected "null" or "str"'

@then('response must return empty list')
def check_all_bank_accounts_empty(response):
    resp = response['data']
    assert resp['result'] == 'OK', f'get-bank-account-all response is not ok. Result is {resp["result"]}, expected OK'
    response_data = resp['data']
    assert len(response_data) == 0, f'get-bank-account-all response is not ok. Response contains {len(response_data)} bank accounts expected == 0'

########################################################################################################################

@when(parsers.parse('user send request to get bank account {state}'), target_fixture='response')
def get_bank_account(auth, state):
    if state != 'with no auth token':
        token = auth(settings.circle_email, settings.circle_password)
    try:
        if state == 'if it exist':
            response = Circle().get_bank_account(token, settings.circle_my_bank_account_id)
        elif state == "if bank_account_id is not my":
            response = Circle().get_bank_account(token, settings.circle_not_my_bank_account_id)
        elif state == 'with no auth token':
            response = Circle().get_bank_account('', settings.circle_my_bank_account_id)
        elif state == 'if bank_account_id was deleted':
            response = Circle().get_bank_account(token, settings.circle_deleted_bank_account_id)
        elif state == 'if bank_account_id is invalid':
            response = Circle().get_bank_account(token, settings.circle_invalid_bank_account_id)
        return response
    except RequestError:
        assert 1 == 0, f'Cant send {inspect.stack()[0][3]} request'
    except CantParseJSON:
        assert 1 == 0, f'Cant parse json from {inspect.stack()[0][3]} response'
    except SomethingWentWrong:
        assert 1 == 0, f'Something went wrong while sending {inspect.stack()[0][3]} request'

@then('response must contains info about bank account')
def check_get_bank_account(response):
    resp = response['data']
    assert resp['result'] == 'OK', f'get-bank-account response is not ok. Result is {resp["result"]}, expected OK'
    account = resp['data']
    assert isinstance(account['id'], str), f'get-bank-account response is not ok. Id is {account["id"]}, expected str'
    assert isinstance(account['brokerId'], str), f'get-bank-account response is not ok. BrokerId is {account["brokerId"]}, expected str'
    assert account['clientId'] == settings.circle_client_id, f'get-bank-account response is not ok. ClientId is {account["clientId"]}, expected {settings.circle_client_id}'
    assert isinstance(account['bankAccountId'], str), f'get-bank-account response is not ok. BankAccountId is {account["bankAccountId"]}, expected str'
    assert isinstance(account['bankAccountStatus'], int), f'get-bank-account response is not ok. BankAccountId is {account["bankAccountId"]}, expected int'
    assert isinstance(account['description'], str), f'get-bank-account response is not ok. Description is {account["description"]}, expected str'
    assert isinstance(account['trackingRef'], str), f'get-bank-account response is not ok. TrackingRef is {account["trackingRef"]}, expected str'
    assert isinstance(account['fingerPrint'], str), f'get-bank-account response is not ok. FingerPrint is {account["fingerPrint"]}, expected str'
    assert isinstance(account['billingDetailsName'], str), f'get-bank-account response is not ok. BillingDetailsName is {account["billingDetailsName"]}, expected str'
    assert isinstance(account['billingDetailsCity'], str), f'get-bank-account response is not ok. BillingDetailsCity is {account["billingDetailsCity"]}, expected str'
    assert isinstance(account['billingDetailsCountry'], str), f'get-bank-account response is not ok. BillingDetailsCountry is {account["billingDetailsCountry"]}, expected str'
    assert isinstance(account['billingDetailsLine1'], (type(None), str)), f'get-bank-account response is not ok. BillingDetailsLine1 is {account["billingDetailsLine1"]}, expected str'
    assert isinstance(account['billingDetailsLine2'], (type(None), str)), f'get-bank-account response is not ok. BillingDetailsLine2 is {account["billingDetailsLine2"]}, expected str'
    assert isinstance(account['billingDetailsDistrict'], str), f'get-bank-account response is not ok. BillingDetailsDistrict is {account["billingDetailsDistrict"]}, expected str'
    assert isinstance(account['billingDetailsPostalCode'], str), f'get-bank-account response is not ok. BillingDetailsPostalCode is {account["billingDetailsPostalCode"]}, expected str'
    assert isinstance(account['bankAddressBankName'], str), f'get-bank-account response is not ok. BankAddressBankName is {account["bankAddressBankName"]}, expected str'
    assert isinstance(account['bankAddressCity'], str), f'get-bank-account response is not ok. BankAddressCity is {account["bankAddressCity"]}, expected str'
    assert isinstance(account['bankAddressCountry'], str), f'get-bank-account response is not ok. BankAddressCountry is {account["bankAddressCountry"]}, expected str'
    assert isinstance(account['bankAddressLine1'], (type(None), str)), f'get-bank-account response is not ok. BankAddressLine1 is {account["bankAddressLine1"]}, expected str'
    assert isinstance(account['bankAddressLine2'], (type(None), str)), f'get-bank-account response is not ok. BankAddressLine2 is {account["bankAddressLine2"]}, expected str'
    assert isinstance(account['bankAddressDistrict'], str), f'get-bank-account response is not ok. BankAddressDistrict is {account["bankAddressDistrict"]}, expected str'
    assert account['error'] is None, f'get-bank-account response is not ok. Error is {account["error"]}, expected "null"'
    assert account['isActive'] is True, f'get-bank-account response is not ok. IsActive is {account["isActive"]}, expected "true"'
    assert isinstance(account['createDate'], str), f'get-bank-account response is not ok. CreateDate is {account["createDate"]}, expected str'
    assert isinstance(account['updateDate'], str), f'get-bank-account response is not ok. UpdateDate is {account["updateDate"]}, expected str'
    assert account['iban'] is None or isinstance(account['iban'], str), f'get-bank-account response is not ok. Iban is {account["iban"]}, expected "null"'
    assert account['accountNumber'] is None or isinstance(account['accountNumber'], str), f'get-bank-account response is not ok. AccountNumber is {account["accountNumber"]}, expected "null" or "str"'
    assert account['routingNumber'] is None or isinstance(account['routingNumber'], str), f'get-bank-account response is not ok. RoutingNumber is {account["routingNumber"]}, expected "null" or "str"'

@then(parsers.parse('response must returns {result}'))
def check_get_bank_account_result(response, result):
    resp = response['data']
    assert resp['result'] == result, f'get-bank-account response is not ok. Result is {resp["result"]}, expected {result}'

########################################################################################################################

@given('user get deleted bank_account_id', target_fixture='resp')
def get_resp(resp):
    resp['bankaccountid_to_delete'] = settings.circle_deleted_bank_account_id
    return resp

@when('user send request to delete bank account', target_fixture='response')
def delete_bank_account(resp):
    bankaccountid_to_delete = resp['bankaccountid_to_delete']
    try:
        response = Circle().delete_bank_account(resp['token'], bankaccountid_to_delete)
        response['deleted_bankaccountid'] = bankaccountid_to_delete
        return response
    except RequestError:
        assert 1 == 0, f'Cant send {inspect.stack()[0][3]} request'
    except CantParseJSON:
        assert 1 == 0, f'Cant parse json from {inspect.stack()[0][3]} response'
    except SomethingWentWrong:
        assert 1 == 0, f'Something went wrong while sending {inspect.stack()[0][3]} request'

@then('response must contains deleted true')
def check_delete_bank_account_response(response):
    resp = response['data']
    assert resp['result'] == 'OK', f'delete_bank_account response is not ok. Result is {resp["result"]}, expected OK'
    response_data = resp['data']
    assert response_data['deleted'] is True, f'delete_bank_account response is not ok. Deleted is {response_data["deleted"]} expected "true"'

@then("get-bank-accounts-all haven't to return deleted bank account")
def check_delete_bank_account(resp, response):
    r = Circle().get_bank_account_all(resp['token'])
    assert len(r['data']['data']) == resp['accounts_count'] - 1, f'get-bank-accounts-all response is not ok. {len(response["data"]["data"])} accounts at response, expected {resp["accounts_count"] - 1}'
    for account in r['data']['data']:
        assert account['bankAccountId'] != response['deleted_bankaccountid'], f'get-bank-accounts-all response is not ok. Deleted bankaccountid - {resp["deleted_bankaccountid"]} is in response'

@then("count of bank accounts at get-bank-accounts-all hasn't change")
def check_delete_deleted_bank_account(resp):
    r = Circle().get_bank_account_all(resp['token'])
    assert len(r['data']['data']) == resp['accounts_count'], f'get-bank-accounts-all response is not ok. {len(r["data"]["data"])} accounts at response, expected {resp["accounts_count"]}'

@when('user2 send request to delete bank account', target_fixture='response')
def delete_bank_account_2(auth, resp):
    token = auth(settings.circle_empty_bank_accounts_email, settings.circle_empty_bank_accounts_password)
    try:
        response = Circle().delete_bank_account(token, resp['bankaccountid_to_delete'])
        return response
    except RequestError:
        assert 1 == 0, f'Cant send {inspect.stack()[0][3]} request'
    except CantParseJSON:
        assert 1 == 0, f'Cant parse json from {inspect.stack()[0][3]} response'
    except SomethingWentWrong:
        assert 1 == 0, f'Something went wrong while sending {inspect.stack()[0][3]} request'

@when('user send request to delete bank account without token', target_fixture='response')
def delete_bank_account_3(resp):
    try:
        response = Circle().delete_bank_account('', resp['bankaccountid_to_delete'])
        return response
    except RequestError:
        assert 1 == 0, f'Cant send {inspect.stack()[0][3]} request'
    except CantParseJSON:
        assert 1 == 0, f'Cant parse json from {inspect.stack()[0][3]} response'
    except SomethingWentWrong:
        assert 1 == 0, f'Something went wrong while sending {inspect.stack()[0][3]} request'

