from API.Simplex import Simplex
from pytest_bdd import scenario, given, when, then
import settings


@scenario(f'../features/circle.feature', 'Make a deposit by card')
def test_simplex_deposit():
    pass

@given('User try to make a deposit from {from_asset} to {to_asset} with amount {amount}')
def create_payment(from_asset, to_asset, amount, auth):
    token = auth(settings.me_tests_email, settings.me_tests_password )
    result = Simplex().create_payment(token, from_asset, to_asset, amount)
    assert result['result'] == "OK", f"Expected: result will be 'OK' but returned: {result}"