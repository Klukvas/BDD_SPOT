from API import WalletHistory, Wallet, Blockchain, Transfer
from pytest_bdd import scenario, given, when, then, parsers
from time import sleep
import settings

@given('Some crypto on balance', target_fixture="get_balance")
def get_balance(auth):
    print(f'call get_balance ')
    token = auth(settings.email, settings.password)
    balances = Wallet(1).balances(token)
    assert type(balances) == list
    assert len(balances) > 0
    return [token, balances]

@scenario('features/transfer.feature', 'Make a transfer by phone')
def test_transfer_by_phone():
    pass

@when(parsers.parse('User send {asset} to phone number'), target_fixture="send_transfer")
def send_transfer(get_balance, asset):
    transferApi = Transfer(1)
    transferData = transferApi.create_transfer(
        get_balance[0],
        settings.transfer_to_phone,
        asset,
        settings.balance_asssets[asset] / 2
    )
    assert type(transferData) == dict, f'Expected that response will be dict, but gets: {type(transferData)}\nTransferData: {transferData}.Asset:{asset}\tAmount: {settings.balance_asssets[asset] / 2}'
    assert type(transferData['transferId']) == str
    return [transferData, asset]

@then('User has new record(by phone) in operation history')
def check_operation_history_transfer(send_transfer, get_balance):
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

@then('User`s balance is changed after transfer to phone')
def balance_change_after_transfer(get_balance, send_transfer):

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

@then('Receive user has new record in operation history', target_fixture="receive_operation_history")
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
   
    return [received_transfer[0]['newBalance'], token, send_transfer[1]]

@then('Balance of receive user are correct')
def check_balance_after_receive(receive_operation_history):
    balances = Wallet(1).balances(receive_operation_history[1])
    receive_balance = list(
        filter(
            lambda x: x['assetId'] == receive_operation_history[2],
            balances
        )
    )
    assert len(receive_balance) == 1
    assert receive_balance[0]['balance'] == receive_operation_history[0]

######################################################################################################


@scenario('features/transfer.feature', 'Make a transfer by address')
def test_transfer_by_address():
    pass

@when(parsers.parse('User send {asset} to {address}'), target_fixture="create_withdrawal")
def create_withdrawal(get_balance, asset, address):
    transferData = Blockchain(1).withdrawal(
        get_balance[0],
        asset,
        settings.balance_asssets[asset] / 2,
        address
    )
    assert type(transferData) == dict, f'Expected type dict but returned:\n{transferData}'
    assert type(transferData['operationId']) == str
    return [transferData, asset, address]

@then('User has new record in operation history')
def operation_history_withdrawal(create_withdrawal, get_balance):
    counter = 0
    while True:
        sleep(12)
        counter += 1
        op_history = WalletHistory(1).operations_history(get_balance[0])
        assert type(op_history) == list
        sended_transfer = list(
            filter(
                lambda x: str(create_withdrawal[0]['requestId']) == x['operationId'].split('|')[0],
                op_history
            )
        )
        if len(sended_transfer):
            if sended_transfer[0]['status'] == 0 and \
                sended_transfer[0]['balanceChange'] != 0:
                break
        if counter > 7:
            raise ValueError(f'Can not find operations with status 0 for 15 seconds\nSearched operationId: {create_withdrawal[0]["requestId"]}\nsended_transfer in op hi: {sended_transfer}') 
    assert len(sended_transfer) == 1, f'Expected that operationId of transfer will be unique but gets:\nrequestId: {create_withdrawal[0]["requestId"]}\n{sended_transfer}\n'
    assert sended_transfer[0]['operationType'] == 1
    assert sended_transfer[0]['assetId'] == create_withdrawal[1] == sended_transfer[0]['withdrawalInfo']['withdrawalAssetId']
    assert sended_transfer[0]['balanceChange'] == ((settings.balance_asssets[create_withdrawal[1]] / 2 )* -1) == sended_transfer[0]['withdrawalInfo']['withdrawalAmount'] * -1
    assert sended_transfer[0]['status'] == 0
    assert type(sended_transfer[0]['withdrawalInfo']) == dict
    assert sended_transfer[0]['withdrawalInfo']['toAddress'] == create_withdrawal[2]

@then('User`s balance is changed after transfer to address')
def change_balance_after_withdrawal(get_balance, create_withdrawal):

    new_balances = Wallet(1).balances(get_balance[0])
    assert type(new_balances) == list
    assert len(new_balances) > 0
    new_balances = list(
        filter(
            lambda x: x['assetId'] == create_withdrawal[1],
            new_balances
        )
    )
    
    old_balances = list(
        filter(
            lambda x: x['assetId'] == create_withdrawal[1],
            get_balance[1]
        )
    )
    assert old_balances[0]['balance'] > new_balances[0]['balance']

@then('Receive user has new record in operation history(deposit)', target_fixture="deposit_operation_history")
def deposit_operation_history(auth, create_withdrawal):
    token = auth(settings.receive_email, settings.password)
    counter = 0 
    while True:
        counter += 1
        op_history = WalletHistory(1).operations_history(token)
        received_deposit = list(
            filter(
                lambda x: str(create_withdrawal[0]['requestId']) == x['operationId'].split('|')[0],
                op_history
            )
        )
        if len(received_deposit):
            if received_deposit[0]['status'] == 0 and \
                received_deposit[0]['balanceChange']:
                break
        if counter > 6:
            raise ValueError('Can not find operations with status 0 for 15 seconds') 
        sleep(5)
    assert len(received_deposit) == 1
    assert received_deposit[0]['operationType'] == 0
    assert received_deposit[0]['assetId'] == create_withdrawal[1]
    assert received_deposit[0]['balanceChange'] == settings.balance_asssets[create_withdrawal[1]] / 2 == received_deposit[0]['depositInfo']['depositAmount']
    assert received_deposit[0]['newBalance'] > received_deposit[0]['newBalance'] - received_deposit[0]['balanceChange']

    return [received_deposit[0]['newBalance'], token, create_withdrawal[1]]

@then('Balance of deposited user are correct')
def chek_balance_after_deposit(deposit_operation_history):
    balances = Wallet(1).balances(deposit_operation_history[1])
    receive_balance = list(
        filter(
            lambda x: x['assetId'] == deposit_operation_history[2],
            balances
        )
    )
    assert len(receive_balance) == 1
    assert receive_balance[0]['balance'] == deposit_operation_history[0]
