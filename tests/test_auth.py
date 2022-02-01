from API import WalletHistory, Auth
from pytest_bdd import scenario, given, when, then, parsers
from time import sleep
import settings
from uuid import uuid4

@scenario(f'../features/auth.feature', 'Change password')
def test_cahnge_password():
    pass

@given('User pass the registration', target_fixture="register")
def register():
    password = settings.template_tests_password
    email = str(uuid4()).replace('-', '') + '@mailinator.com'
    auth_object = Auth(email, password)
    reg_data = auth_object.register()
    assert type(reg_data) == dict, f"Expected: type == dict\nReturned: {type(reg_data)}\treg_data:{reg_data}"
    assert all (k in reg_data for k in ("token","refreshToken")), f"Expected that reg_data object has 2 keys but returned: {reg_data}"
    return { "token": reg_data['token'], "auth_object": auth_object, "email":  email}

@when('User change his password')
def change_password(register):
    ch_pass_data = register['auth_object'].change_password(
        register['token'],
        settings.template_tests_password,
        'newpassword1'
    )
    assert type(ch_pass_data) == dict, f"Expected: type == dict\nReturned: {type(ch_pass_data)}\tch_pass_data: {ch_pass_data}"

@then('User can not logIn by old password')
def log_in_by_old_password(auth, register):
    auth_data = auth(register['email'], settings.template_tests_password, 'incorrect password')
    assert type(auth_data) == tuple, f"Expected that response will be tirple vut returned: {type(auth_data)}\tauth_data:{auth_data}"
    assert auth_data[0] == 401, f"Expected that status code will be 401 but returned: {auth_data[0]}"
    assert auth_data[1] == '{"message":"InvalidUserNameOrPassword"}', f"Expecte thatn auth resp will be: 'message': 'InvalidUserNameOrPassword' but returned: {auth_data[1]}"

@then('User can logIn by new password')
def log_in_by_new_password(auth, register):
    auth_data = auth(register['email'], 'newpassword1')
    assert type(auth_data) == str, f"Expected that response will be str vut returned: {type(auth_data)}\tauth_data:{auth_data}"


@scenario(f'../features/auth.feature', 'LogOut')
def test_logout():
    pass

@given('User logIn to account', target_fixture="get_token")
def get_token(auth):
    token = auth(settings.template_tests_email, settings.template_tests_password)
    assert type(token) == str, f"Expected: type == str\nReturned: {type(token)}\treg_data:{token}"
    return { "token": token}

@given('User can interact with endpoints')
def check_token(get_token):
    op_history = WalletHistory().operations_history(get_token['tokens'][0])
    assert type(op_history) == list, f"Expected that resp type will be list but returned: {op_history}"

@when('User make LogOut')
def log_out(get_token):
    
    logout_data = Auth(None, None).logout(get_token['tokens'][0])
    assert type(logout_data) == dict, f"Expected that response will be dict but returned: {logout_data}"
    assert logout_data['response']['result'] == 'OK', f"Expected that result of response will be eql to OK but returned: {logout_data}"

@then('User can not interact with endpoint with old token')
def check_logouted_token(get_token):
    op_history = WalletHistory().operations_history(get_token['tokens'][0])
    assert type(op_history) == int, f"Expected that resp type will be int but returned: {op_history}"
    assert op_history == 401, f"Expected that resp will be eql to 401 but returned: {op_history}"


@scenario(f'../features/auth.feature', 'Refresh token')
def test_refreshtoken():
    pass

@given('User logIn to account', target_fixture="get_token")
def get_token(auth):
    tokens = auth(settings.template_tests_email, settings.template_tests_password, 'need refresh token')
    assert type(tokens) == list, f"Expected: type == str\nReturned: {type(tokens)}\t tokens: {tokens}"
    return { "tokens": tokens}

@given('User can interact with endpoints')
def check_token(get_token):
    op_history = WalletHistory().operations_history(get_token['tokens'][0])
    assert type(op_history) == list, f"Expected that resp type will be list but returned: {op_history}"

@when('User make Refresh of token', target_fixture="refresh")
def refresh(get_token):
    new_token = Auth(None, None).refresh(get_token['tokens'][1])
    assert type(new_token) == dict, f"Expected that response will be dict but returned: {new_token}"
    assert all([k in ['refreshToken', 'token'] for k in list( new_token['response']['data'].keys() )]), f"Expected that response contains next keys: refreshToken, token< but response is: {new_token['response'].keys()}\tnew_token{new_token}"
    return { "new_tokens": new_token }

@then('User can interact with endpoint with new token')
def check_logouted_token(refresh):
    # op_history = WalletHistory().operations_history(get_token['tokens'][0])
    # assert type(op_history) == int, f"Expected that resp type will be int but returned: {op_history}"
    # assert op_history == 401, f"Expected that resp will be eql to 401 but returned: {op_history}"
    op_history = WalletHistory().operations_history(refresh['new_tokens']['response']['data']['token'])
    assert type(op_history) == list, f"Expected that resp type will be int but returned: {op_history}"

@scenario(f'../features/auth.feature', 'Negative registration')
def test_negative_registration():
    pass

@given(parsers.parse("User try to registration with {email} and {password}. User get {response} with {status_code}"))
def test_registration(email, password, response, status_code):
    negative_response = Auth(email, password).register('negative cases')
    assert type(negative_response) == dict, f"Expected: type == str\nReturned: {type(negative_response)}\t tokens: {negative_response}"
    assert negative_response['response'] == response, f"Expected: {response}\nReturned: {negative_response['response']}"
    assert negative_response['status'] == int(status_code),f"Expected: {status_code}\nReturned: {negative_response['status']}"

@scenario(f'../features/auth.feature', 'Negative authentification')
def test_negative_authentification():
    pass

@given(parsers.parse("User try to authentification with {email} and {password}. User get {response} with {status_code}"))
def test_authentification(email, password, response, status_code):
    negative_response = Auth(email, password).authenticate('negative cases')
    assert type(negative_response) == dict, f"Expected: type == str\nReturned: {type(negative_response)}\t tokens: {negative_response}"
    assert negative_response['response'] == response, f"Expected: {response}\nReturned: {negative_response['response']}"
    assert negative_response['status'] == int(status_code),f"Expected: {status_code}\nReturned: {negative_response['status']}"

@scenario(f'../features/auth.feature', 'Negative change password')
def test_negative_change_password():
    pass

@given(parsers.parse("User try to change password from {password_old} to {password_new}. User get {response} with {status_code}"))
def test_change_password_negative(auth, password_old, password_new, response, status_code):
    token = auth(settings.auth_tests_email_for_change_password, settings.auth_tests_password_for_change_password)
    if password_old == 'default':
        password_old = settings.auth_tests_password_for_change_password
    change_password_resp = Auth(
        settings.auth_tests_email_for_change_password, 
        settings.auth_tests_password_for_change_password
    ).change_password(token, password_old, password_new, "negative cases")
    assert str(change_password_resp['code']) == status_code, f"Expected status code eql to {status_code} but returned: {change_password_resp}"
    assert change_password_resp['resp'] == response, f"Expected status code eql to {status_code} but returned: {change_password_resp}"