import uuid

from API.Verify import Verify
from API.WalletHistory import WalletHistory
from API.Wallet import Wallet
from API.Blockchain import Blockchain
from API.Transfer import Transfer
from pytest_bdd import scenario, given, when, then, parsers
from time import sleep
import settings


@given('Some crypto on balance', target_fixture="get_balance")
def get_balance(auth):
    token = auth(
        settings.base_user_data_email, settings.base_user_data_password
    )['response']
    assert 'data' in token.keys(), \
        f"Expected that 'data' key will be in response. But returned: {token}"
    token = token['data']['token']
    balances = Wallet().balances(token)['response']
    assert 'data' in balances.keys(), \
        f"Expected that 'data' key will be in response. But returned: {token}"
    balances = balances['data']['balances']
    assert type(balances) == list
    assert len(balances) > 0
    return [token, balances]


@scenario(f'../features/transfer.feature', 'Make a transfer by phone')
def test_transfer_by_phone():
    pass


@when(parsers.parse('User send {asset} to phone number'), target_fixture="send_transfer")
def send_transfer(get_balance, asset):
    transferApi = Transfer()
    uniqId = str(uuid.uuid4())
    transferData = transferApi.create_transfer(
        token=get_balance[0],
        request_id=uniqId,
        phone=settings.base_user_data_transfer_to_phone,
        asset=asset,
        amount=settings.balance_asssets[asset] / 2,
        specific_case=False
    )['response']
    assert 'data' in transferData.keys(),\
        f"Expected that 'data' key will be in response. But returned: {transferData}"
    transferData = transferData['data']
    assert type(
        transferData) == dict, f'Expected that response will be dict, but gets: {type(transferData)}\nTransferData: {transferData}.Asset:{asset}\tAmount: {settings.balance_asssets[asset] / 2}'
    assert type(transferData['operationId']) == str
    return {"transferData": transferData, "asset": asset, "requestId": uniqId}


@when("User approve transfer by code")
def approve_transfer(send_transfer, get_balance):
    verif = Verify().verify_transfer(
        get_balance[0],
        send_transfer['transferData']['operationId']
    )['response']['result']
    assert verif == 'OK'

@then('User has new record in operation history')
def check_operation_history_transfer(send_transfer, get_balance):
    counter = 0
    while True:
        sleep(5)
        counter += 1
        op_history = WalletHistory().operations_history(
            get_balance[0]
        )['response']
        assert 'data' in op_history.keys(), \
            f"Expected that 'data' key will be in response. But returned: {op_history}"
        op_history = op_history['data']
        assert type(op_history) == list
        sended_transfer = list(
            filter(
                lambda x: send_transfer['requestId'] == x['operationId'].split('|')[0],
                op_history
            )
        )
        if len(sended_transfer):
            if sended_transfer[0]['status'] == 0 and \
                    sended_transfer[0]['balanceChange'] != 0:
                break
        elif counter > 5:
            raise ValueError('Can not find operations with status 0 for 15 seconds')
    assert len(
        sended_transfer) == 1, f'Expected that operationId of transfer will be unique but gets:\nrequestId: {send_transfer["requestId"]}\n{sended_transfer}\n'
    assert sended_transfer[0]['operationType'] == 6
    assert sended_transfer[0]['assetId'] == send_transfer['asset'] == sended_transfer[0]['transferByPhoneInfo'][
        'withdrawalAssetId']
    assert sended_transfer[0]['balanceChange'] == ((settings.balance_asssets[send_transfer['asset']] / 2) * -1) == \
           sended_transfer[0]['transferByPhoneInfo']['withdrawalAmount'] * -1
    assert sended_transfer[0]['status'] == 0
    assert type(sended_transfer[0]['transferByPhoneInfo']) == dict
    assert sended_transfer[0]['transferByPhoneInfo']['toPhoneNumber'] == settings.base_user_data_transfer_to_phone


@then('User`s balance is changed')
def balance_change_after_transfer(get_balance, send_transfer):
    new_balances = Wallet().balances(
        get_balance[0]
    )['response']
    assert 'data' in new_balances.keys(), \
        f"Expected that key 'data' will be in response. But response is: {new_balances}"
    new_balances = new_balances['data']['balances']
    assert type(new_balances) == list
    assert len(new_balances) > 0
    new_balances = list(
        filter(
            lambda x: x['assetId'] == send_transfer['asset'],
            new_balances
        )
    )

    old_balances = list(
        filter(
            lambda x: x['assetId'] == send_transfer['asset'],
            get_balance[1]
        )
    )
    assert old_balances[0]['balance'] > new_balances[0]['balance']


@then('Receive user has new record in operation history', target_fixture="receive_operation_history")
def receive_operation_history(auth, send_transfer):
    token = auth(
        settings.base_user_data_receive_email,
        settings.base_user_data_password
    )['response']
    assert 'data' in token.keys(), \
        f"Expected that key 'data' will be in response. But response is: {token}"
    token = token['data']['token']
    counter = 0
    while True:
        counter += 1
        op_history = WalletHistory().operations_history(token)
        assert op_history['status'] == 200
        assert 'data' in op_history['response'].keys(), \
            f"Expected that key 'data' will be in response. But response is: {op_history}"
        op_history = op_history['response']['data']
        received_transfer = list(
            filter(
                lambda x: send_transfer['requestId'] == x['operationId'].split('|')[0],
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
    assert received_transfer[0]['assetId'] == send_transfer['asset']
    assert received_transfer[0]['balanceChange'] == settings.balance_asssets[send_transfer['asset']] / 2 == \
           received_transfer[0]['receiveByPhoneInfo']['depositAmount']
    assert received_transfer[0]['receiveByPhoneInfo']['fromPhoneNumber'] == settings.base_user_data_from_phone_number, \
        f'Ar:{settings.base_user_data_from_phone_number}\nEr: {received_transfer}'
    assert received_transfer[0]['newBalance'] > received_transfer[0]['newBalance'] - received_transfer[0][
        'balanceChange']

    return [received_transfer[0]['newBalance'], token, send_transfer['asset']]


@then('Balance of receive user are correct')
def check_balance_after_receive(receive_operation_history):
    balances = Wallet().balances(
        receive_operation_history[1]
    )['response']
    assert  'data' in balances.keys(), \
        f"Expected that 'data' key will be in response. But returned: {balances}"
    balances = balances['data']['balances']
    receive_balance = list(
        filter(
            lambda x: x['assetId'] == receive_operation_history[2],
            balances
        )
    )
    assert len(receive_balance) == 1
    assert receive_balance[0]['balance'] == receive_operation_history[0]


######################################################################################################


@scenario('../features/transfer.feature', 'Make a internalWithdrawal')
def test_transfer_by_address():
    pass


@when(parsers.parse('User send {asset} to {address}'), target_fixture="create_withdrawal")
def create_withdrawal(get_balance, asset, address):
    uniqId = str(uuid.uuid4())
    transferData = Blockchain().withdrawal(
        token=get_balance[0],
        uniqId=uniqId,
        asset=asset,
        amount=settings.balance_asssets[asset] / 2,
        address=address
    )['response']
    assert 'data' in transferData.keys(), \
        f"Expected that key 'data' will be in response. But response is: {transferData}"
    transferData = transferData['data']
    assert type(transferData) == dict, f'Expected type dict but returned:\n{transferData}'
    assert type(transferData['operationId']) == str
    return {
        "transferData": transferData,
        "asset": asset,
        "address": address,
        "requestId": uniqId
    }


@then('User has new record(withdrawal) in operation history')
def operation_history_withdrawal(create_withdrawal, get_balance):
    appoved = False
    counter = 0
    while True:
        sleep(20)
        counter += 1
        op_history = WalletHistory().operations_history(
            get_balance[0]
        )['response']
        assert 'data' in op_history.keys(), \
            f"Expected that 'data' key will be in response. But returned: {op_history}"
        op_history = op_history['data']
        sended_transfer = list(
            filter(
                lambda x: str(create_withdrawal['requestId']) in x['operationId'].split('|')[0],
                op_history
            )
        )
        if len(sended_transfer):
            if sended_transfer[0]['status'] == 0 and \
                    sended_transfer[0]['balanceChange'] != 0:
                break
            elif sended_transfer[0]['status'] == 1 and \
                    not appoved:
                appoved = True
                counter -= 1
                approve_opetarion = Verify().verify_withdrawal(
                    get_balance[0], create_withdrawal['transferData']['operationId']
                )['response']['result']
                assert approve_opetarion == 'OK', f"Expected that response ll be string, but returned: {approve_opetarion}"
        if counter > 7:
            raise ValueError(
                f'Can not find operations with status 0 for 15 seconds\nSearched operationId: {create_withdrawal["transferData"]["requestId"]}\nsended_transfer in op hi: {sended_transfer}')
    assert len(
        sended_transfer) == 1, \
        f'Expected that operationId of transfer will be unique but gets:\nrequestId: {create_withdrawal["transferData"]["requestId"]}\n{sended_transfer}\n'
    assert sended_transfer[0]['operationType'] == 1
    assert sended_transfer[0]['assetId'] == create_withdrawal['asset'] == sended_transfer[0]['withdrawalInfo'][
        'withdrawalAssetId']
    assert sended_transfer[0]['balanceChange'] == ((settings.balance_asssets[create_withdrawal['asset']] / 2) * -1) == \
           sended_transfer[0]['withdrawalInfo']['withdrawalAmount'] * -1
    assert sended_transfer[0]['status'] == 0
    assert type(sended_transfer[0]['withdrawalInfo']) == dict
    assert sended_transfer[0]['withdrawalInfo']['toAddress'] == create_withdrawal['address']


@then('User`s balance is changed after withdrawal')
def change_balance_after_withdrawal(get_balance, create_withdrawal):
    new_balances = Wallet().balances(
        get_balance[0]
    )['response']
    assert 'data' in new_balances.keys(), \
        f"Expected that 'data' key will be in response. But returned: {new_balances}"
    new_balances = new_balances['data']['balances']
    assert len(new_balances) > 0
    new_balances = list(
        filter(
            lambda x: x['assetId'] == create_withdrawal['asset'],
            new_balances
        )
    )

    old_balances = list(
        filter(
            lambda x: x['assetId'] == create_withdrawal['asset'],
            get_balance[1]
        )
    )
    assert old_balances[0]['balance'] > new_balances[0]['balance']


@then('Receive user has new record(deposit) in operation history', target_fixture="deposit_operation_history")
def deposit_operation_history(auth, create_withdrawal):
    token = auth(
        settings.base_user_data_receive_email,
        settings.base_user_data_password
    )['response']
    assert 'data' in token.keys(), \
        f"Expected that 'data' key will be in response. But returned: {token}"
    token = token['data']['token']
    counter = 0
    while True:
        counter += 1
        op_history = WalletHistory().operations_history(
            token
        )['response']
        assert 'data' in op_history.keys(), \
            f"Expected that 'data' key will be in response. But returned: {op_history}"
        op_history = op_history['data']
        received_deposit = list(
            filter(
                lambda x: str(create_withdrawal['requestId']) == x['operationId'].split('|')[0],
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
    assert received_deposit[0]['assetId'] == create_withdrawal['asset']
    assert received_deposit[0]['balanceChange'] == settings.balance_asssets[create_withdrawal['asset']] / 2 == \
           received_deposit[0]['depositInfo']['depositAmount']
    assert received_deposit[0]['newBalance'] > received_deposit[0]['newBalance'] - received_deposit[0]['balanceChange']

    return [received_deposit[0]['newBalance'], token, create_withdrawal['asset']]


@then('Balance of deposited user are correct')
def chek_balance_after_deposit(deposit_operation_history):
    balances = Wallet().balances(
        deposit_operation_history[1]
    )['response']
    assert 'data' in balances.keys(), \
        f"Expected that key 'data' will be in response. But response is: {balances}"
    balances = balances['data']['balances']
    receive_balance = list(
        filter(
            lambda x: x['assetId'] == deposit_operation_history[2],
            balances
        )
    )
    assert len(receive_balance) == 1
    assert receive_balance[0]['balance'] == deposit_operation_history[0]
