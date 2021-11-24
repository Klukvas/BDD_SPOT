from API import WalletHistory, Circle, Wallet
from pytest_bdd import scenario, given, when, then
from time import sleep
import settings


@scenario('features/circle.feature', 'Make a deposit by card')
def test_transfer_by_phone():
    pass

@given('Some crypto on balance', target_fixture="get_enc_key")
def get_enc_key(auth):
    print(f'call get_balance ')
    token = auth(settings.email, settings.password)
    enc_key = Circle(1).get_encryption_key(token)
    assert type(enc_key) == dict
    assert len(enc_key['data'].keys()) == 2
    return [token, enc_key['data']]

@given('User encrypt data of his card', target_fixture="enc_data")
def enc_data(get_enc_key):
    enc_data = Circle(1).encrypt_data(get_enc_key[0], get_enc_key[1]['data']['encryptionKey'])
    assert type(enc_data['data']) == dict
    assert len(enc_data.keys()) == 2
    return enc_data

@when('User add new card', target_fixture='add_card')
def add_card(enc_data, get_enc_key):
    card_data = Circle(1).add_card(
        get_enc_key[0],
        enc_data['data']['data'],
        get_enc_key[1]['data']['keyId']
    )
    assert all(
            key in card_data['data']['data'] 
            for key in [
                        "id","cardName","last4","network",
                        "expMonth","expYear","status",
                        "errorCode","isActive","createDate",
                        "updateDate"
                    ]
        )
    return card_data['data']

@then('User create deposit via card')
def create_deposit(add_card, get_enc_key, enc_data):
    deposit = Circle(1).create_payment(
        get_enc_key[0],
        enc_data['data']['data'],
        get_enc_key['data']['keyId'],
        add_card['data']['data']['id']
    )
    assert type(deposit) == dict
    assert deposit['data']['data']['status'] == 0
    return deposit['data']

@then('User has new record in operation history')
def check_op(get_enc_key, create_deposit):
    counter = 0
    while True:
        sleep(5)
        counter += 1
        op_history = WalletHistory(1).operations_history(get_enc_key[0])
        assert type(op_history) == list
        deposit = list(
            filter(
                lambda x: create_deposit['data']['depositId'] == x['operationId'],
                op_history
            )
        )
        if len(deposit):
            if deposit[0]['status'] == 0 and \
                deposit[0]['balanceChange'] != 0:
                break
        elif counter > 5:
            raise ValueError('Can not find operations with status 0 for 15 seconds') 
    assert len(deposit) == 1, f'Expected that operationId of transfer will be unique but gets:\nrequestId: {create_deposit["data"]["depositId"]}\n{deposit}\n'
    assert deposit[0]['operationType'] == 0
    assert deposit[0]['assetId'] == 'USD'
    assert deposit[0]['balanceChange'] == 11 == deposit[0]['depositInfo']['depositAmount']
    assert deposit[0]['status'] == 0
    assert type(deposit[0]['depositInfo']) == dict
    assert deposit[0]['depositInfo']['txId'] == create_deposit['data']['depositId']
    return deposit

@then('User`s balance is changed')
def check_balance_changed(get_enc_key, check_op):
    new_balances = Wallet(1).balances(get_enc_key[0])
    usd_balance = list(
        filter(
            lambda x: x['assetId'] == 'USD',
            new_balances
        )
    )
    assert len(usd_balance) == 1
    assert usd_balance['balance'] == check_op['newBalance']

@then('User delete his card')
def delete_card(get_enc_key, add_card):
    deleted_card = Circle(1).delete_card(get_enc_key[0], add_card['data']['id'])
    assert deleted_card['data']['data']['deleted'] == True
    all_cards = Circle(1).get_all_cards(get_enc_key[0])
    assert len(all_cards['data']['data']) == 0
