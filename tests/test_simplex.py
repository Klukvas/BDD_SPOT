from API.Simplex import Simplex
from pytest_bdd import scenario, given, parsers
import settings


@scenario(f'../features/simplex.feature', 'Make a deposit by simplex')
def test_simplex_deposit():
    pass

@given(parsers.parse('User try to make a deposit from {from_asset} to {to_asset} with amount {amount}'))
def create_payment(from_asset, to_asset, amount, auth):
    token = auth(settings.me_tests_email, settings.me_tests_password )
    print(token)
    result = Simplex().create_payment(token, from_asset, to_asset, amount)
    assert type(result) == dict,  f"Expected: result will be dict type but returned: {result}"
    assert result['result'] == "OK", f"Expected: result will be 'OK' but returned: {result}"