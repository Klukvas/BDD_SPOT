from API.WalletHistory import WalletHistory
from API.Circle import Circle
from API.Wallet import Wallet
from API.Exceptions import RequestError, SomethingWentWrong, CantParseJSON
from pytest_bdd import scenarios, given, when, then, parsers
from time import sleep
import settings

scenarios('../features/circle.feature')

@given('User get encryption key', target_fixture="get_enc_key")
def get_enc_key(auth):
    token = auth(settings.me_tests_email, settings.me_tests_password )
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

@when('user add bank account', target_fixture="add_bank_account_response")
def add_bank_account(auth, variables_dict):
    token = auth(settings.circle_email, settings.circle_password)
    try:
        response = Circle().add_bank_account(token, variables_dict['bank_country'], variables_dict['billing_country'],
                                             variables_dict['account_number'], variables_dict['iban'],
                                             variables_dict['routing_number'], variables_dict['guid'])
        return response
    except RequestError:
        assert 1 == 0, 'Cant send add_bank_account request'
    except CantParseJSON:
        assert 1 == 0, 'Cant parse json from add_bank_account response'
    except SomethingWentWrong:
        assert 1 == 0, 'Something went wrong while sending add_bank_account request'

@then(parsers.parse('response status code has to be equals to {status_code}'))
def check_response_status_code(status_code, add_bank_account_response: dict):
    response_status_code = add_bank_account_response['status']
    assert int(status_code) == int(response_status_code), 'add_bank_accounts status code is different from expected'

@then('response must contains added bank account info')
def check_add_bank_account_response_data(variables_dict, add_bank_account_response: dict):
    response = add_bank_account_response['data']
    assert response['result'] == 'OK', f'add_bank_account response is not ok. Result is {response["result"]}, expected OK'
    response_data = response['data']
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
