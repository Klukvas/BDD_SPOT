from API import Auth, WalletHistory, Wallet, Swap
from pytest_bdd import scenario, given, when, then
import pytest
from random import choice
from time import sleep
import settings
@scenario('spot.feature', 'Make a swap')
def test_arguments():
    pass

@given('User logIn to account', target_fixture="auth")
def auth():
    token = Auth(settings.email, settings.password, 1).authenticate()
    assert type(token) == list
    return token[0]

@given('Some crypto on balance', target_fixture="get_balance")
def get_balance(auth):
    balances = Wallet(1).balances(auth)
    assert type(balances) == list
    assert len(balances) > 0
    return balances


@when('User gets 1 step swap quote', target_fixture="get_quote")
def get_quote(auth, get_balance):
    assetList = \
        list(
            filter(
                    lambda a: a['assetId'] not in ['USD', 'EUR'], 
                    get_balance
                )
        )
    
    assert len(assetList) > 0
    asset = choice(assetList)['assetId']
    swapApi = Swap(1)
    quote = swapApi.get_quote(
        auth,
        asset,
        'USD',
        0.1
    )
    return [quote, swapApi]

@when('User execute quote', target_fixture="exec")
def exec(auth, get_quote):
    response = get_quote[1].execute_quote(auth, get_quote[0])
    assert type(response) == dict
    assert response['isExecuted'] == True
    assert response['fromAsset'] == get_quote[0]['fromAsset']
    assert response['toAsset'] == get_quote[0]['toAsset']
    assert response['fromAssetVolume'] == get_quote[0]['fromAssetVolume']
    assert response['isFromFixed'] == True 
    operationId = response['operationId']
    return [operationId, response]

@then('User has new record in operation history')
def hist(auth, exec):
    counter = 0
    while True:
        sleep(5)
        counter += 1
        op_history = WalletHistory(1).operations_history(auth)
        assert type(op_history) == list
        executed_swap = list(
            filter(
                lambda x: x['operationId'] == exec[0],
                op_history
            )
        )
        assert len(executed_swap) == 2
        if executed_swap[0]['status'] == 0 and \
            executed_swap[1]['status'] == 0 and \
            executed_swap[1]['balanceChange'] != 0 and \
            executed_swap[0]['balanceChange'] !=  0 :
            break
        elif counter > 5:
            raise ValueError('Can not find operations with status 0 for 15 seconds') 
            
    for item in executed_swap:
        if item['assetId'] == exec[1]['fromAsset']:
            assert item['operationType'] == 2
            assert item['assetId'] == exec[1]['fromAsset']
            assert item['balanceChange'] == (exec[1]['fromAssetVolume'] * -1)
            assert item['status'] == 0
            assert type(item['swapInfo']) == dict
            assert item['swapInfo']['isSell'] == True
            assert item['swapInfo']['sellAssetId'] == exec[1]['fromAsset']
            assert item['swapInfo']['sellAmount'] == exec[1]['fromAssetVolume']
            assert item['swapInfo']['buyAssetId'] == exec[1]['toAsset']
        elif item['assetId'] == exec[1]['toAsset']:
            assert item['operationType'] == 2
            assert item['assetId'] == exec[1]['toAsset']
            assert item['status'] == 0
            assert type(item['swapInfo']) == dict
            assert item['swapInfo']['isSell'] == False
            assert item['swapInfo']['sellAssetId'] == exec[1]['fromAsset']
            assert item['swapInfo']['sellAmount'] == exec[1]['fromAssetVolume']
            assert item['swapInfo']['buyAssetId'] == exec[1]['toAsset']

# @then('User has new record in balance history')
# def hist1(auth):
#     assert 2

@then('User`s balance is changed')
def hist2(auth, get_balance, exec):
    assets = [
            exec[1]['fromAsset'], 
            exec[1]['toAsset']
        ]
    new_balances = Wallet(1).balances(auth)
    assert type(new_balances) == list
    assert len(new_balances) > 0
    new_balances = list(
        filter(
            lambda x: x['assetId'] in assets,
            new_balances
        )
    )
    
    old_balances = list(
        filter(
            lambda x: x['assetId'] in assets,
            get_balance
        )
    )
    for item in range(len(new_balances)):
        new_asset = new_balances[item]['assetId']
        for jitem in range(len(old_balances)):
            old_asset = old_balances[jitem]['assetId']
            if new_asset == old_asset:
                if new_asset == assets[0]:
                    assert old_balances[jitem]['balance'] > new_balances[item]['balance']
                else:
                    assert old_balances[jitem]['balance'] < new_balances[item]['balance']
