from API import WalletHistory, Wallet, Swap
from pytest_bdd import scenario, given, when, then, parsers
from time import sleep
import settings
from random import choice
from GRPC.AssetsInfo import assetsInfo
from GRPC.Helper import helper


@scenario(f'../features/swap.feature', 'Make a swap')
def test_make_swap():
    pass

@given('Some crypto on balance', target_fixture="get_balance")
def get_balance(auth):
    token = auth(settings.me_tests_email, settings.me_tests_password)
    balances = Wallet().balances(token)
    assert type(balances) == list
    assert len(balances) > 0
    return [token, balances] #{"token": token }

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



@scenario(f'../features/swap.feature', 'Swap with amount more than balance')
def test_make_swap_more_than_balance():
    pass

@given('User try to get quote with amount more than has on balance. User get an lowBalance error')
def quote_more_than_balance(auth):
    token = auth(settings.me_tests_email, settings.me_tests_password)
    from_asset = choice(list(settings.balance_asssets.keys()))
    quote = Swap().get_quote(
            token, 
            from_asset,
            'USD',
            settings.balance_asssets[from_asset] * 2,
            True
        )
    assert quote[0] == {"result": "LowBalance"}, f"Expected that response from get quote is: 'result': 'LowBalance' but returned: {quote}"




@scenario(f'../features/swap.feature', 'Swap with nonexisting asset from')
def test_make_swap_nonexisting_asset_from():
    pass

@given('User try to get quote with nonexisting asset from. User get an Asset do not found error')
def quote_nonexisting_asset_from(auth):
    token = auth(settings.me_tests_email, settings.me_tests_password)
    quote = Swap().get_quote(
            token, 
            'asd',
            'USD',
            2,
            True
        )
    assert quote[1] == {"message": "FromAsset or ToAsset do not found"}, f"Expected that response from get quote is: message: FromAsset or ToAsset do not found but returned: {quote}"
    assert quote[0] == 400, f"Expected that response from get quote is 400 but returned: {quote}"

@scenario(f'../features/swap.feature', 'Swap with nonexisting asset to')
def test_make_swap_nonexisting_asset_to():
    pass

@given('User try to get quote with nonexisting asset to. User get an Asset do not found error')
def quote_nonexisting_asset_from(auth):
    token = auth(settings.me_tests_email, settings.me_tests_password)
    quote = Swap().get_quote(
            token, 
            'LTC',
            'asdasd',
            0.00002,
            True
        )
    assert quote[1] == {"message": "FromAsset or ToAsset do not found"}, f"Expected that response from get quote is: message: FromAsset or ToAsset do not found but returned: {quote}"
    assert quote[0] == 400, f"Expected that response from get quote is 400 but returned: {quote}"




# Scenario: Swap with min && max amount
#         Given User try to get assets with setted min and max amount
#         Given User try to get quote with min and max amout

@scenario(f'../features/swap.feature', 'Swap with min && max amount')
def test_swap_min_max_amount():
    pass

@given(parsers.parse("User set to {asset} min and max amount"), target_fixture="get_assets_with_min_max_volume")
def get_assets_with_min_max_volume(asset):

    response = assetsInfo.get_asset_by_id(asset)
    assert response != None, f"Error of getting asset"
    
    min_vol = helper.string_to_decimal(
        str(settings.balance_asssets[asset]* 0.2) #20%
    )
    assert min_vol != None, f"Error of getting min volume as dict"
    
    max_vol = helper.string_to_decimal(
        str(settings.balance_asssets[asset]*0.5) #50%
    )
    assert max_vol != None, f"Error of getting max volume as dict"

    min_max = {
        "MaxTradeValue": max_vol,
        "MinTradeValue": min_vol
    }

    update_response = assetsInfo.update_asset(response.Value, min_max)
    assert update_response != None, f"Error with updating asset"

    return { 
            "response": response, 
            "min_dict": min_vol, 
            "max_dict": max_vol,
            "min_float": settings.balance_asssets[asset]* 0.2,
            "max_float": settings.balance_asssets[asset]* 0.5,
            "asset": asset
        }

@given(parsers.parse("User try to get quote with {min_max} amout and fixed {fixed}"))
def get_quote_with_min_max_volume(min_max, fixed, auth, get_assets_with_min_max_volume):
    try:
        token = auth(settings.me_tests_email, settings.me_tests_password)
        swapApi = Swap()
        if min_max == 'min':
            volume = get_assets_with_min_max_volume['min_float'] - ( get_assets_with_min_max_volume['min_float'] * 0.1 )
        else:
            volume = get_assets_with_min_max_volume['max_float'] + ( get_assets_with_min_max_volume['max_float'] * 0.1 )
        if fixed == True:
            quote = swapApi.get_quote(
                token,
                get_assets_with_min_max_volume['asset'],
                choice(list(settings.balance_asssets.keys())),
                volume,
                True,
                'MIN_MAX_TESTS'
            )
        else:
            quote = swapApi.get_quote(
                token, 
                choice(list(settings.balance_asssets.keys())),
                get_assets_with_min_max_volume['asset'],
                volume,
                False,
                'MIN_MAX_TESTS'
            )
        expected_response = 'AmountIsSmall' if min_max == 'min' else 'AmountToLarge'
        print(f"quote: {quote}")
        assert quote == expected_response, f"Exp: {expected_response}  Returned: {quote}"
    except Exception as err:
        raise Exception(err)
    finally:
        min_vol = get_assets_with_min_max_volume["response"].Value.MinTradeValue if get_assets_with_min_max_volume["response"].Value.MinTradeValue else None
        max_vol = get_assets_with_min_max_volume["response"].Value.MaxTradeValue if get_assets_with_min_max_volume["response"].Value.MaxTradeValue else None
        min_max_object = {
            "MinTradeValue": min_vol,
            "MaxTradeValue": max_vol
        }
        min_max_object['MinTradeValue']
        min_max_object['MaxTradeValue']
        assetsInfo.update_asset(get_assets_with_min_max_volume["response"].Value, min_max_object)
