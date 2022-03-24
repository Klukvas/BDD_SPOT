from time import sleep
from API import Auth, Blockchain, Verify, Transfer, WalletHistory
from pytest_bdd import scenario, given, then, when, parsers
import uuid
from gmailApi import MailParser
from datetime import datetime
import settings
import requests
import os


@scenario(f'../features/receive_email.feature', 'Email confirmation')
def test_email_confirmation():
    pass

@given('User registration', target_fixture="register")
def register():
    email = 'emailtest' + str(uuid.uuid4()) + '@mailforspam.com'
    event_date = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    token = Auth(email, 'testpassword1').register()
    assert type(token) == dict, f'Expected response type: dict\nReturned: {token}'
    assert len(token) == 2
    return {"token": token["token"], "email": email, "event_date": event_date}

@given('User has new email with code', target_fixture="get_email_data")
def get_email_data(register):
    mail_parser = MailParser(0, register['email'],  register["event_date"]).parse_mail()
    assert mail_parser
    assert type(mail_parser) == dict
    assert len(mail_parser.keys()) == 3
    path = os.path.join(
        os.getcwd(),
        'email_templates',
        'Email_confirmation_request_mock.txt'
    )
    with open(path) as f:
        template = f.read().\
            replace('{{come_code_here}}', mail_parser['code']).\
                replace('{{link}}', mail_parser['app_link'])
    assert template.strip() == mail_parser['message_body'], \
        f'Text from template: !\n{template}\n!\n\nText mess: !\n{mail_parser["message_body"]}\n!'
    return {'code': mail_parser['code']}

@when('User can verify email by code from mail', target_fixture="check_op")
def verify_email(register, get_email_data):
    verify = Verify().verify_email(register['token'], get_email_data['code'])
    assert verify['data'] == 'OK'

@then('User`s email is veryfied', target_fixture="check_op")
def check_email_verified(register):
    auth_data = Verify().client_data(register['token'])
    assert type(auth_data) == dict, f'Expected that email ll be verifyed but:{auth_data}'
    assert auth_data['data']['emailVerified'] == True


@scenario(f'../features/receive_email.feature', 'Success login')
def test_success_login():
    pass

@given('User has new Success login email after login')
def log_in(auth):
    auth(settings.template_tests_email, settings.template_tests_password)
    event_date = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    mail_parser = MailParser(1, settings.template_tests_email, event_date).parse_mail()
    assert mail_parser
    assert type(mail_parser) == dict
    assert len(mail_parser.keys()) == 3
    path = os.path.join(
        os.getcwd(),
        'email_templates',
        'Success_Login.txt'
    )
    print(f"!{mail_parser['time'].strip()}!")
    with open(path) as f:
        template = f.read().\
            replace('{{email}}', settings.template_tests_email).\
                replace('{{time}}', mail_parser['time'].strip()).\
                    replace('{{ip}}', mail_parser['ip'])
    assert template == mail_parser['message_body'],\
        f'Text from template: !\n{template}\n!\n\nText mess: !\n{mail_parser["message_body"]}\n!'


@scenario(f'../features/receive_email.feature', 'Transfer(waiting for user)')
def test_success_transfer_email():
    pass

@given(parsers.parse('User send transfer with asset: {asset}, to phone {phone}'), target_fixture='make_transfer')
def make_transfer(asset, phone, auth):
    token = auth(settings.template_tests_email, settings.template_tests_password )
    assert type(token) == str
    amount = settings.balance_asssets[asset] / 2
    event_date = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    transferData = Transfer().create_transfer(
            token, phone, asset, amount
        )
    assert type(transferData) == dict, f'Expected that response will be dict, but gets: {type(transferData)}\nTransferData: {transferData}.Asset:{asset}\tAmount: {amount}\t {type(amount)}'
    assert type(transferData['operationId']) == str
    return {
            "transferData": transferData, "asset": asset, "amount": amount, 
            "phone": phone, "event_date": event_date, "token": token
        }

@when('User has new email with appove link', target_fixture='check_transfer_email')
def check_transfer_email(make_transfer):
    mail_parser = MailParser(2, settings.template_tests_email, make_transfer['event_date'], make_transfer['transferData']['operationId']).parse_mail()
    assert mail_parser
    path = os.path.join(
        os.getcwd(),
        'email_templates',
        'Verify withdrawal.txt'
    )
    with open(path) as f:
        template = f.read().\
            replace('{{amount}}', str(make_transfer['amount'])).\
                replace('{{asset}}', make_transfer['asset']).\
                    replace('{{ip}}', mail_parser['ip']).\
                        replace('{{phone_to}}', make_transfer['phone']).\
                            replace('{{link}}', mail_parser['confirm_link']).\
                                replace('{{receiveAmount}}', str(make_transfer['amount'])).\
                                    replace('{{feeAmount}}', '0').\
                                        replace('{{feeAsset}}', make_transfer['asset'])

    assert template == mail_parser['message_body'], \
               f'Text from template: !\n{template}\n!\n\nText mess: !\n{mail_parser["message_body"]}\n!'
    return {"confirm_link": mail_parser['confirm_link']}

@then('User approve transfer by link')
def approve_transfer(check_transfer_email, make_transfer):
    counter = 0
    resp = requests.get(check_transfer_email['confirm_link'])
    assert resp.status_code == 200
    while True:
        balances = WalletHistory().operations_history(make_transfer['token'], make_transfer['asset'])
        counter += 1
        for item in balances:
            if make_transfer['transferData']['requestId'] in item['operationId'] \
                and item['status'] == 0 and item['balanceChange'] != 0:
                assert item['operationType'] == 6
                assert item['assetId'] == make_transfer['asset']
                assert item['balanceChange'] == make_transfer['amount']*-1, f'Expected: {make_transfer["amount"]*-1}\nReturned: {item["balanceChange"]}\nItem: {item}'
                assert item['transferByPhoneInfo'] !=  None
                assert item['transferByPhoneInfo']['toPhoneNumber'] ==  make_transfer['phone']
                assert item['transferByPhoneInfo']['withdrawalAssetId'] == make_transfer['asset']
                assert item['transferByPhoneInfo']['withdrawalAmount'] == make_transfer['amount']
                return
        if counter > 6:
            raise AttributeError(f'Can not find record operation history with status 1 and operationId like {make_transfer["transferData"]["requestId"]}')
        sleep(5)


@scenario(f'../features/receive_email.feature', 'Internal withdrawal')
def test_success_withdrawal_email():
    pass

@given(parsers.parse('User send withdrawal request wiht asset: {asset}, to address: {address}'), target_fixture='make_withdrawal')
def make_withdrawal(auth, asset, address):
    token = auth(settings.template_tests_email, settings.template_tests_password )
    assert type(token) == str
    amount = settings.balance_asssets[asset] / 2
    event_date = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    withdrawalData = Blockchain().withdrawal(
        token, asset, amount, address
    )
    assert type(withdrawalData) == dict, f'Expected that response will be dict, but gets: {type(withdrawalData)}\nTransferData: {withdrawalData}.Asset:{asset}\tAmount: {amount}'
    assert type(withdrawalData['operationId']) == str
    return {
                "withdrawalData": withdrawalData, "event_date": event_date, 
                "token": token, "asset": asset, "amount": amount, "address": address
            }

@when(parsers.parse('User has new email with appove withdwal link with {feeAmount} and {feeAsset}'), target_fixture='check_withdrawal_email')
def check_withdrawal_email(feeAmount, feeAsset, make_withdrawal):
    mail_parser = MailParser(3, settings.template_tests_email, make_withdrawal['event_date'], make_withdrawal['withdrawalData']['operationId']).parse_mail()
    assert mail_parser != None, f'Expected that email ll be finded'
    path = os.path.join(
        os.getcwd(),
        'email_templates',
        'Verify withdrawal.txt'
    )
    if feeAmount != 0:
        receiveAmount = make_withdrawal['amount'] - float(feeAmount)
    else:
        receiveAmount = 0
    with open(path) as f:
        template = f.read().\
            replace('{{amount}}', str(make_withdrawal['amount'])).\
                replace('{{asset}}', make_withdrawal['asset']).\
                    replace('{{feeAmount}}', f"{feeAmount}").\
                        replace('{{feeAsset}}', f"{feeAsset}").\
                            replace('{{ip}}', mail_parser['ip']).\
                                replace('{{link}}', mail_parser['confirm_link']).\
                                    replace('{{address}}', make_withdrawal['address']).\
                                        replace('{{receiveAmount}}', str(make_withdrawal['amount']))

    assert template == mail_parser['message_body'], \
               f'Text from template: !\n{template}\n!\n\nText mess: !\n{mail_parser["message_body"]}\n!'
    return {"link": mail_parser['confirm_link']}

@then('User approve withdrawal by link')
def approve_withdrawal(check_withdrawal_email, make_withdrawal):
    counter = 0
    resp = requests.get(check_withdrawal_email['link'])
    assert resp.status_code == 200
    while True:
        balances = WalletHistory().operations_history(make_withdrawal['token'], make_withdrawal['asset'])
        counter += 1
        for item in balances:
            if make_withdrawal['withdrawalData']['requestId'] in item['operationId'] and \
                item['status'] == 0 and \
                    item['balanceChange'] != 0:
                assert item['operationType'] == 1
                assert item['assetId'] == make_withdrawal['asset']
                assert item['balanceChange'] == make_withdrawal['amount']*-1, f'Expected: {make_withdrawal["amount"]*-1}\nReturned: {item["balanceChange"]}\nItem: {item}'
                assert item['withdrawalInfo'] !=  None
                assert item['withdrawalInfo']['toAddress'] ==  make_withdrawal['address']
                assert item['withdrawalInfo']['withdrawalAssetId'] == make_withdrawal['asset']
                assert item['withdrawalInfo']['withdrawalAmount'] == make_withdrawal['amount']
                assert item['withdrawalInfo']['isInternal'] == True
                assert str(item['withdrawalInfo']['feeAmount']) == settings.template_tests_fee_amoutn
                return
        if counter > 6:
            raise AttributeError(f'Can not find record operation history with status 1 and operationId like {make_withdrawal["withdrawalData"]["requestId"]}')
        sleep(5)



@scenario(f'../features/receive_email.feature', 'Password Recovery')
def test_password_recovery():
    pass

@given('User passed registration', target_fixture="register")
def register():
    email = 'emailtest' + str(uuid.uuid4()) + '@mailforspam.com'
    event_date = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    token = Auth(email, 'testpassword1').register()
    assert type(token) == dict, f'Expected response type: dict\nReturned: {token}'
    assert len(token) == 2
    return {"token": token, "email": email, "event_date": event_date}

@when('User send request to forgot password endpoint')
def change_password(register):
    change_res = Auth(register['email'], 'testpassword1').forgot_password(register['email'])
    assert change_res[0] == 'OK'

@then('User get new email with token', target_fixture='parse_token')
def parse_token(register):
    recovery_data = MailParser(4, register['email'], register['event_date']).parse_mail()
    assert type(recovery_data) == dict
    path = os.path.join(
        os.getcwd(),
        'email_templates',
        'Password recoverу.txt'
    )
    with open(path) as f:
        template = f.read().replace('{{token}}', recovery_data['token'])
    assert template == recovery_data['message_body'], f"Expected:!\n{template}\n!\nGets:!\n{recovery_data['message_body']}\n!"
    return {'token': recovery_data['token']}

@then('User change password using token from email')
def change_password_with_token(parse_token, register):
    recovery_resp = Auth(register['email'], 'testpassword1').\
        password_recovery('testpassword2', parse_token['token'])
    assert recovery_resp[0] == 'OK'

@then('User can not auth with old password')
def log_in_with_new_password(auth, register):
    token = auth(register['email'], 'testpassword1', False)
    assert token[0] == 401
    assert token[1] == '{"message":"InvalidUserNameOrPassword"}'

@then('User can auth with new password')
def log_in_with_new_password(register, auth):
    token = auth(register['email'], 'testpassword2')
    assert type(token) == str


@scenario(f'../features/receive_email.feature', 'ReRegistration')
def test_re_registration():
    pass
@given('ReRegistration mail on inbox after existing user pass registration')
def register_n_check_email():
    event_date = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    token = Auth(settings.template_tests_email, 'testpassword1').register()
    assert type(token) == dict, f'Expected response type: dict\nReturned: {token}'
    assert len(token) == 2
    mail_parser = MailParser(5, settings.template_tests_email, event_date).parse_mail()
    path = os.path.join(
        os.getcwd(),
        'email_templates',
        'reRegister.txt'
    )
    with open(path, encoding='utf-8') as f:
        template = f.read()
    assert template == mail_parser['message_body'], f"Expected:\n{template}\n\nReturned: {mail_parser['message_body']}"


@scenario(f'../features/receive_email.feature', 'Success withdrawal or transfer && deposit')
def test_success_deposit_withdrawal():
    pass

@given(parsers.parse("User send withdrawal/transfer with asset: {asset}, to address/phone {address_phone}"), target_fixture="create_operation")
def create_operation(auth, asset, address_phone):
    token = auth(settings.template_tests_email, settings.template_tests_password )
    amount = settings.balance_asssets[asset] / 2
    if address_phone.startswith('+'):
        operation = Transfer().create_transfer(token, address_phone, asset, amount)
        operation_type = 'transfer'
    else:
        operation = Blockchain().withdrawal(token, asset, amount, address_phone)
        operation_type = 'withdrawal'

    assert type(operation) == dict, f"Expected that operation will be dict, but returned: {operation}"

    return {
                "type": operation_type,
                "operationId": operation['operationId'], 
                "token": token, 
                "requestId": operation['requestId'], 
                "asset": asset, 
                "amount": amount
            }

@when("User approve withdrawal/transfer by restApi", target_fixture="approve_opetarion")
def approve_opetarion(create_operation):
    #Ожидание когда вывод станет в статус ApprovalPending
    counter = 0
    while True:
        sleep(5)
        counter += 1
        op_history = WalletHistory().operations_history(create_operation['token'], create_operation['asset'])
        assert type(op_history) == list
        pending_operation = list(
            filter(
                lambda x: create_operation["requestId"] in x['operationId'],
                op_history
            )
        )
        if  len(pending_operation) == 1 and \
            pending_operation[0]['status'] == 1:
            break
        elif counter > 5:
            raise ValueError('Can not find operations with status 0 for 15 seconds')
    event_date = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    if create_operation['type'] == 'withdrawal':
        approve_resp = Verify().verify_withdrawal(create_operation['token'], create_operation['operationId'])
    else:
        approve_resp = Verify().verify_transfer(create_operation['token'], create_operation['operationId'])
    assert approve_resp == 'Simple | Buy, sell and manage cryptocurrency portfolios'
    return {"event_date": event_date}

@then("User has new success withdrawal email")
def check_success_withdrawal_email(create_operation, approve_opetarion):
    counter = 0
    while True:
        sleep(5)
        counter += 1
        op_history = WalletHistory().operations_history(create_operation['token'], create_operation['asset'])
        assert type(op_history) == list
        approved_withdrawal = list(
            filter(
                lambda x: create_operation["requestId"] in x['operationId'],
                op_history
            )
        )
        if  len(approved_withdrawal) == 1 and \
            approved_withdrawal[0]['status'] == 0:
            break
        elif counter > 5:
            raise ValueError('Can not find operations with status 0 for 15 seconds') 
    success_withdrawal = MailParser(6, settings.template_tests_email, approve_opetarion['event_date'], withdrawal_asset = create_operation['asset'] ).parse_mail()
    assert type(success_withdrawal) == dict
    path = os.path.join(
        os.getcwd(),
        'email_templates',
        'Withdrawal_successful.txt'
    )
    with open(path) as f:
        template = f.read().\
             replace('{{amount}}', str(create_operation['amount'])).\
                replace('{{asset}}', str(create_operation['asset']))
    assert template == success_withdrawal['message_body'], f"Exception with Withdrawal_successful template\nExpected:!\n{template}\n!\nGets:!\n{success_withdrawal['message_body']}\n!"

@then(parsers.parse("Receive user with email {email} has new success deposit email"))
def check_success_deposit_email(email, create_operation, approve_opetarion):
    success_withdrawal = MailParser(7, email, approve_opetarion['event_date']).parse_mail()
    assert type(success_withdrawal) == dict
    path = os.path.join(
        os.getcwd(),
        'email_templates',
        'Deposit_successful.txt'
    )
    with open(path) as f:
        template = f.read().\
            replace('{{amount}}', str(create_operation['amount'])).\
                replace('{{asset}}', str(create_operation['asset']))
    assert template == success_withdrawal['message_body'], f"Exception with Deposit_successful template\nExpected:!\n{template}\n!\nGets:!\n{success_withdrawal['message_body']}\n!"







