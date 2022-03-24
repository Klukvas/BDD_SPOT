from API.Simplex import Simplex
from pytest_bdd import scenario, given, parsers
import settings


@scenario(f'../features/simplex.feature', 'Make a deposit by simplex')
def test_simplex_deposit():
    pass

@given(parsers.parse('User try to make a deposit from {from_asset} to {to_asset} with amount {amount}'))
def create_payment(from_asset, to_asset, amount, auth):
    token = auth(settings.me_tests_email, settings.me_tests_password )
    result = Simplex().create_payment(token, from_asset, to_asset, amount)
    assert type(result) == dict,  f"Expected: result will be dict type but returned: {result}"
    assert result['result'] == "OK", f"Expected: result will be 'OK' but returned: {result}"


@scenario(f'../features/simplex.feature', 'Make a deposit by simplex with non exists asset from')
def test_simplex_deposit_with_non_exists_asset_from():
    pass

@given(parsers.parse("User try to make a deposit by simplex with asset to {to_asset}, amount {amount},  non exists asset from"))
def create_payment_with_non_exists_asset_from(to_asset, amount, auth):
    token = auth(settings.me_tests_email, settings.me_tests_password )
    result = Simplex().create_payment(token, 'from_asset', to_asset, amount)
    assert type(result) == dict,  f"Expected: result will be dict type but returned: {result}"
    assert result['result'] == "AssetDoNotFound", f"Expected: result will be 'AssetDoNotFound' but returned: {result}"


@scenario(f'../features/simplex.feature', 'Make a deposit by simplex with non exists asset to')
def test_simplex_deposit_with_non_exists_asset_to():
    pass

@given(parsers.parse("User try to make a deposit by simplex with asset from {from_asset}, amount {amount},  non exists asset to"))
def create_payment_with_non_exists_asset_to(from_asset, amount, auth):
    token = auth(settings.me_tests_email, settings.me_tests_password )
    result = Simplex().create_payment(token, from_asset, 'to_asset', amount)
    assert type(result) == dict,  f"Expected: result will be dict type but returned: {result}"
    assert result['result'] == "AssetDoNotFound", f"Expected: result will be 'AssetDoNotFound' but returned: {result}"


@scenario(f'../features/simplex.feature', 'Make a deposit by simplex with amount more than maximum')
def test_simplex_deposit_with_amount_more_than_maximum():
    pass

@given(parsers.parse("User try to make a deposit by simplex with asset to {to_asset}, asset from {from_asset} and amount more than maximum {amount}"))
def create_payment_with_amount_more_than_maximum(to_asset, from_asset, amount, auth):
    token = auth(settings.me_tests_email, settings.me_tests_password )
    result = Simplex().create_payment(token, from_asset, to_asset, amount)
    assert type(result) == dict,  f"Expected: result will be dict type but returned: {result}"
    assert result['result'] == "AmountToLarge", f"Expected: result will be 'AmountToLarge' but returned: {result}"


@scenario(f'../features/simplex.feature', 'Make a deposit by simplex with amount less than minimum')
def test_simplex_deposit_with_amount_less_than_minimum():
    pass

@given(parsers.parse("User try to make a deposit by simplex with asset to {to_asset}, asset from {from_asset} and amount {amount}"))
def create_payment_with_amount_less_than_minimum(to_asset, from_asset, amount, auth):
    token = auth(settings.me_tests_email, settings.me_tests_password )
    result = Simplex().create_payment(token, from_asset, to_asset, amount)
    assert type(result) == dict,  f"Expected: result will be dict type but returned: {result}"
    assert result['result'] == "AmountIsSmall", f"Expected: result will be 'AmountIsSmall' but returned: {result}"
