from API import WalletHistory, Circle, Wallet
from pytest_bdd import scenario, given, when, then
from time import sleep
import settings
import pytest

@scenario(f'../features/circle.feature', 'Make a deposit by card')
def test_circle_deposit():
    pass

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
        add_card['id']
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
                lambda x: create_deposit['depositId'] == x['operationId'],
                op_history
            )
        )
        if len(deposit):
            if deposit[0]['status'] == 0 and \
                deposit[0]['balanceChange'] != 0:
                break
        elif counter > 5:
            raise ValueError(f'Can not find operations({create_deposit["depositId"]}) with status 0 for 15 seconds') 
    assert len(deposit) == 1, f'Expected that operationId of transfer will be unique but gets:\nrequestId: {create_deposit["data"]["depositId"]}\n{deposit}\n'
    assert deposit[0]['operationType'] == 0, f"Expected deposit in operation history has operationType: 0. But returned: {deposit[0]['operationType']}"
    assert deposit[0]['assetId'] == 'USD', f"Expected deposit in operation history has assetId: USD. But returned: {deposit[0]['assetId']}"
    assert deposit[0]['balanceChange'] == deposit[0]['depositInfo']['depositAmount'], f"Expected deposit.balanceChange are eql to deposit.depositInfo.depositAmount. Bur returned:\ndeposit.balanceChange:{deposit[0]['balanceChange']} deposit.depositInfo.depositAmount: {deposit[0]['depositInfo']['depositAmount']}"
    assert deposit[0]['status'] == 0, f"Expected that status of deposit are eql to 0. But returned: {deposit[0]['status']}"
    assert type(deposit[0]['depositInfo']) == dict, f"Expected that type of deposit.depositInfo are eqk ti dict. But returned: {type(deposit[0]['depositInfo'])}"
    assert deposit[0]['depositInfo']['txId'] == create_deposit['depositId'], f"Expected that deposit.depositInfo.txId are elq to Id from reponse of deposit creation. But returned:\ndeposit[0]['depositInfo']['txId']: {deposit[0]['depositInfo']['txId']} == create_deposit['depositId']: {create_deposit['depositId']}"
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
