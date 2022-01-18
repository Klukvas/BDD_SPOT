import email
import turtle
from API import WalletHistory, Circle, Wallet, Auth
from pytest_bdd import scenario, given, when, then
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
    