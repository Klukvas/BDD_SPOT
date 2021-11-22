from API import WalletHistory, Wallet, Swap, Transfer
from pytest_bdd import scenario, given, when, then, parsers
from time import sleep
import settings


@scenario('features/transfer.feature', 'Make a transfer by phone')
def test_transfer_by_phone():
    pass

@given('Some crypto on balance', target_fixture="get_balance")
def get_balance(auth):
    print(f'call get_balance ')
    token = auth(settings.email, settings.password)
    balances = Wallet(1).balances(token)
    assert type(balances) == list
    assert len(balances) > 0
    return [token, balances]

@when(parsers.parse('User send {asset} to phone number'), target_fixture="send_transfer")
def send_transfer(get_balance, asset):
    transferApi = Transfer(1)
    transferData = transferApi.create_transfer(
        get_balance[0],
        settings.transfer_to_phone,
        asset,
        settings.balance_asssets[asset] / 2
    )
    assert type(transferData['transferId']) == str
    return [transferData, asset]

@then('User has new record in operation history')
def hist(send_transfer, get_balance):
    counter = 0
    while True:
        sleep(5)
        counter += 1
        op_history = WalletHistory(1).operations_history(get_balance[0])
        assert type(op_history) == list
        sended_transfer = list(
            filter(
                lambda x: send_transfer[0]['requestId'] == x['operationId'].split('|')[0],
                op_history
            )
        )
        if len(sended_transfer):
            if sended_transfer[0]['status'] == 0 and \
                sended_transfer[0]['balanceChange'] != 0:
                break
        elif counter > 5:
            raise ValueError('Can not find operations with status 0 for 15 seconds') 
    assert len(sended_transfer) == 1, f'Expected that operationId of transfer will be unique but gets:\nrequestId: {send_transfer[0]["requestId"]}\n{sended_transfer}\n'
    assert sended_transfer[0]['operationType'] == 6
    assert sended_transfer[0]['assetId'] == send_transfer[1] == sended_transfer[0]['transferByPhoneInfo']['withdrawalAssetId']
    assert sended_transfer[0]['balanceChange'] == ((settings.balance_asssets[send_transfer[1]] / 2 )* -1) == sended_transfer[0]['transferByPhoneInfo']['withdrawalAmount'] * -1
    assert sended_transfer[0]['status'] == 0
    assert type(sended_transfer[0]['transferByPhoneInfo']) == dict
    assert sended_transfer[0]['transferByPhoneInfo']['toPhoneNumber'] == settings.transfer_to_phone

@then('User`s balance is changed')
def hist2(get_balance, send_transfer):

    new_balances = Wallet(1).balances(get_balance[0])
    assert type(new_balances) == list
    assert len(new_balances) > 0
    new_balances = list(
        filter(
            lambda x: x['assetId'] == send_transfer[1],
            new_balances
        )
    )
    
    old_balances = list(
        filter(
            lambda x: x['assetId'] == send_transfer[1],
            get_balance[1]
        )
    )
    assert old_balances[0]['balance'] > new_balances[0]['balance']

@then('Receive user has new record in operation history')
def receive_operation_history(auth, send_transfer):
    token = auth(settings.receive_email, settings.password)
    counter = 0 
    while True:
        counter += 1
        op_history = WalletHistory(1).operations_history(token)
        received_transfer = list(
            filter(
                lambda x: send_transfer[0]['requestId'] == x['operationId'].split('|')[0],
                op_history
            )
        )
        assert len(received_transfer) == 1
        if received_transfer[0]['status'] == 0 and \
            received_transfer[0]['balanceChange']:
            break
        elif counter > 6:
            raise ValueError('Can not find operations with status 0 for 15 seconds') 
        sleep(5)
    assert received_transfer[0]['operationType'] == 7
    assert received_transfer[0]['assetId'] == send_transfer[1]
    assert received_transfer[0]['balanceChange'] == settings.balance_asssets[send_transfer[1]] / 2 == received_transfer[0]['receiveByPhoneInfo']['depositAmount']
    assert received_transfer[0]['receiveByPhoneInfo']['fromPhoneNumber'] == settings.from_ph_number, f'Ar:\nEr: {received_transfer}'
    assert received_transfer[0]['newBalance'] > received_transfer[0]['newBalance'] - received_transfer[0]['balanceChange']
