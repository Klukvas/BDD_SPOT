from API import WalletHistory, Wallet, Swap
from pytest_bdd import scenario, given, when, then, parsers
from time import sleep
import settings


@scenario(f'../features/swap.feature', 'Make a swap')
def test_make_swap():
    pass

@given('Some crypto on balance', target_fixture="get_balance")
def get_balance(auth):
    token = auth(settings.me_tests_email, settings.me_tests_password)
    balances = Wallet().balances(token)
    assert type(balances) == list
    assert len(balances) > 0
    return [token, balances]

@when(parsers.parse('User gets swap quote with from fixed {isFromFixed} from asset {fromAsset} to  asset {toAsset}'), target_fixture="get_quote")
def get_quote(get_balance,isFromFixed, fromAsset, toAsset):
    swapApi = Swap()
    # isFromFixed = True if isFromFixed == 'True' else False
    if isFromFixed == 'True':
        isFromFixed = True
        volume = settings.balance_asssets[fromAsset]/2
    else:
        isFromFixed = False
        volume = settings.to_balance[toAsset]/2

    quote = swapApi.get_quote(
        get_balance[0],
        fromAsset,
        toAsset,
        volume,
        isFromFixed
    )
    assert type(quote) == dict, f'Expected that quote will be dict, but returned:\n{quote}.\nFrom asset: {fromAsset}; Toasset: {toAsset}; isFromFixed: {isFromFixed}'
    assert quote['fromAsset'] == fromAsset
    assert quote['toAsset'] == toAsset
    if isFromFixed:
        assert quote['fromAssetVolume'] == volume
    else:
        assert quote['toAssetVolume'] == volume
    assert quote['isFromFixed'] == isFromFixed
   
    
    return {"quote": quote, "SwapApiObject": swapApi, "isFromFixed": isFromFixed}

@when('User execute quote', target_fixture="exec")
def exec(get_balance, get_quote):
    response = get_quote["SwapApiObject"].execute_quote(get_balance[0], get_quote["quote"])
    assert type(response) == dict, f'Expected: type dict\nReturned: {type(response)}\nResponse: {response}'
    assert response['isExecuted'] == True
    assert response['fromAsset'] == get_quote["quote"]['fromAsset']
    assert response['toAsset'] == get_quote["quote"]['toAsset']
    assert response['fromAssetVolume'] == get_quote["quote"]['fromAssetVolume']
    assert response['isFromFixed'] == get_quote["isFromFixed"]
    operationId = response['operationId']
    return [operationId, response]

@then('User has new record in operation history')
def hist(get_balance, exec):
    counter = 0
    while True:
        sleep(5)
        counter += 1
        op_history = WalletHistory().operations_history(get_balance[0])
        assert type(op_history) == list
        executed_swap = list(
            filter(
                lambda x: x['operationId'] == exec[0],
                op_history
            )
        )
        if  len(executed_swap) == 2 and \
            executed_swap[0]['status'] == 0 and \
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

@then('User`s balance is changed')
def hist2(get_balance, exec):
    assets = [
            exec[1]['fromAsset'], 
            exec[1]['toAsset']
        ]
    new_balances = Wallet().balances(get_balance[0])
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
            get_balance[1]
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
