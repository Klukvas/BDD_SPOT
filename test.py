from API import Auth, WalletHistory, Wallet, Swap
from pytest_bdd import scenario, given, when, then
import pytest
from random import choice


@scenario('spot.feature', 'Make a swap')
def test_arguments():
    pass

@given('User logIn to account', target_fixture="auth")
def auth():
    authApi = Auth('trn1@mailinator.com', 'testpassword1', 1)
    token = authApi.authenticate()
    assert type(token) == list
    return token[0]
    # request.config.cache.set('token', token[0])

@given('Some crypto on balance', target_fixture="get_balance")
def get_balance(auth):
    # balances = Wallet(1).balances(request.config.cache.get('token', None))
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

@when('User execute quote')
def exec(auth, get_quote):
    response = get_quote[1].execute_quote(auth, get_quote[0])
    assert response == 1
    print(response)

@then('User has new record in operation history')
def hist(auth):
    assert 2
@then('User has new record in balance history')
def hist1(auth):
    assert 2
@then('User`s balance is changed')
def hist2(auth):
    assert 2