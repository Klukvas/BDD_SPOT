from time import sleep
from API.Blockchain import Blockchain
from API.Auth import Auth
from API.Verify import Verify
from API.Transfer import Transfer
from API.WalletHistory import WalletHistory
from pytest_bdd import scenarios, given, then, when, parsers
import uuid
from API.GmailApi import ParseMessage
import settings
import requests
import os

scenarios(f'../features/receive_email.feature')


@given('User registration', target_fixture="register")
def register():
    email = settings.template_tests_email. \
        split('@')[0]
    email += "+" + str(uuid.uuid4().int) + "@gmail.com"
    token = Auth(email, 'testpassword1').register()['response']['data']
    assert type(token) == dict, f'Expected response type: dict\nReturned: {token}'
    assert len(token) == 2
    return {"token": token["token"], "email": email}


@given('User has new email with code', target_fixture="get_email_data")
def get_email_data(create_temporary_template):
    mail_object = ParseMessage(10)
    mail_parser = mail_object.getMessage()
    assert type(mail_parser) == dict, f"Expect type dict; Returned: {type(mail_parser)}"
    assert len(mail_parser.keys()) == 4
    path = os.path.join(
        os.getcwd(),
        'templates',
        f'{mail_object.get_template_name()}.html'
    )
    with open(path) as f:
        template = f.read(). \
            replace('{{code}}', mail_parser['code']). \
            replace('{{htmlConfirUrl}}', mail_parser['htmlConfirUrl'])
    data = create_temporary_template(mail_parser['message_body'], mail_object.get_template_name())
    os.remove(f"{mail_object.get_template_name()}.html")
    assert template.strip() == data, \
        f'Text from template: !\n{template}\n!\n\nText mess: !\n{data}\n!'
    return {'code': mail_parser['code']}


@when('User can verify email by code from mail', target_fixture="check_op")
def verify_email(register, get_email_data):
    verify = Verify().verify_email(register['token'], get_email_data['code'])
    assert verify['response']['result'] == 'OK'


@then('User`s email is veryfied', target_fixture="check_op")
def check_email_verified(register):
    auth_data = Verify().client_data(register['token'])['response']
    assert type(auth_data) == dict, f'Expected that email ll be verifyed but:{auth_data}'
    assert auth_data['data']['emailVerified'] is True


###############################################################################################################################################

@given('User has new Success login email after login')
def log_in(auth, create_temporary_template):
    auth(
        settings.template_tests_email,
        settings.template_tests_password
    )
    mail_object = ParseMessage(2)
    mail_parser = mail_object.getMessage()
    assert type(mail_parser) == dict, f"Expected type dict: returned: {type(mail_parser)}"
    assert type(mail_parser) == dict
    assert len(mail_parser.keys()) == 3
    path = os.path.join(
        os.getcwd(),
        'templates',
        f'{mail_object.get_template_name()}.html'
    )
    with open(path) as f:
        template = f.read(). \
            replace('{{time}}', mail_parser['time'].strip()). \
            replace('{{ip}}', mail_parser['ip'])
    data = create_temporary_template(mail_parser['message_body'], mail_object.get_template_name())
    os.remove(f"{mail_object.get_template_name()}.html")
    assert template == data, \
        f'Text from template: !\n{template}\n!\n\nText mess: !\n{data}\n!'


###############################################################################################################################################

@given(parsers.parse('User send transfer with asset: {asset}, to phone {phone}'), target_fixture='make_transfer')
def make_transfer(asset, phone, auth):
    token = auth(
        settings.template_tests_email,
        settings.template_tests_password
    )['response']['data']['token']

    amount = settings.balance_asssets[asset] / 2

    uniq_id = str(uuid.uuid4())

    transferData = Transfer().create_transfer(
        token, uniq_id, phone, asset, amount
    )

    assert transferData['status'] == 200
    assert transferData['response']['result'] == 'OK'
    assert type(transferData['response']['data']['operationId']) == str
    return {
        "transferData": transferData['response'], "asset": asset, "amount": amount,
        "phone": phone, "token": token, "uniq_id": uniq_id
    }


@when('User has new email with appove link', target_fixture='check_transfer_email')
def check_transfer_email(make_transfer, create_temporary_template):
    mail_object = ParseMessage(4)
    mail_parser = mail_object.getMessage()
    assert type(mail_parser) == dict, f"Expected type dict; returned: {type(mail_parser)}"
    path = os.path.join(
        os.getcwd(),
        'templates',
        f'{mail_object.get_template_name()}.html'
    )
    with open(path) as f:
        template = f.read(). \
            replace('{{amount}}', str(make_transfer['amount'])). \
            replace('{{asset}}', make_transfer['asset']). \
            replace('{{ip}}', mail_parser['ip']). \
            replace('{{destination}}', make_transfer['phone']). \
            replace('{{htmlUrl}}', mail_parser['htmlUrl']). \
            replace('{{receiveAmount}}', str(make_transfer['amount'])). \
            replace('{{feeAmount}}', '0'). \
            replace('{{feeAsset}}', make_transfer['asset']). \
            replace('{{code}}', mail_parser['code'])

    data = create_temporary_template(mail_parser['message_body'], mail_object.get_template_name())
    os.remove(f"{mail_object.get_template_name()}.html")
    assert template == data, \
        f'Text from template: !\n{template}\n!\n\nText mess: !\n{data}\n!'
    return {"confirm_link": mail_parser['url']}


@then('User approve transfer by code')
def approve_transfer(check_transfer_email, make_transfer):
    counter = 0
    resp = Verify().verify_transfer(
        make_transfer['token'],
        make_transfer['transferData']['data']['operationId']
    )
    assert resp['status'] == 200
    while True:
        balances = WalletHistory().operations_history(
            make_transfer['token'],
            make_transfer['asset']
        )['response']['data']
        counter += 1
        for item in balances:
            if make_transfer['uniq_id'] in item['operationId'] \
                    and item['status'] == 0 and item['balanceChange'] != 0:
                assert item['operationType'] == 6
                assert item['assetId'] == make_transfer['asset']
                assert item['balanceChange'] == make_transfer[
                    'amount'] * -1, f'Expected: {make_transfer["amount"] * -1}\nReturned: {item["balanceChange"]}\nItem: {item}'
                assert item['transferByPhoneInfo'] is not None
                assert item['transferByPhoneInfo']['toPhoneNumber'] == make_transfer['phone']
                assert item['transferByPhoneInfo']['withdrawalAssetId'] == make_transfer['asset']
                assert item['transferByPhoneInfo']['withdrawalAmount'] == make_transfer['amount']
                return
        if counter > 6:
            raise AttributeError(
                f'Can not find record operation history with status 1 and operationId like {make_transfer["uniq_id"]}')
        sleep(5)


###############################################################################################################################################

@given(parsers.parse('User send withdrawal request wiht asset: {asset}, to address: {address}'),
       target_fixture='make_withdrawal')
def make_withdrawal(auth, asset, address):
    token = auth(
        settings.template_tests_email,
        settings.template_tests_password
    )['response']['data']['token']
    amount = settings.balance_asssets[asset] / 2
    uniq_id = str(uuid.uuid4())
    withdrawalData = Blockchain().withdrawal(
        token,
        uniq_id,
        asset,
        amount,
        address
    )['response']
    assert 'data' in withdrawalData.keys(), \
        f"Expected that 'data' key will be in response. But response is: {withdrawalData}"
    withdrawalData = withdrawalData['data']
    assert type(
        withdrawalData
    ) == dict, \
        f'''Expected that response will be dict, but gets: {type(withdrawalData)}
        TransferData: {withdrawalData}.
        Asset:{asset}
        Amount: {amount}
        '''
    assert type(withdrawalData['operationId']) == str
    return {
        "withdrawalData": withdrawalData,
        "token": token, "asset": asset, "amount": amount, "address": address, "request_id": uniq_id
    }


@when(parsers.parse('User has new email with appove withdwal link with {feeAmount} and {feeAsset}'),
      target_fixture='check_withdrawal_email')
def check_withdrawal_email(create_temporary_template, feeAmount, feeAsset, make_withdrawal):
    mail_object = ParseMessage(5)
    mail_parser = mail_object.getMessage()
    assert mail_parser is not None, f'Expected that email ll be finded'
    path = os.path.join(
        os.getcwd(),
        'templates',
        f'{mail_object.get_template_name()}.html'
    )
    if feeAmount != 0:
        receiveAmount = make_withdrawal['amount'] - float(feeAmount)
    else:
        receiveAmount = make_withdrawal['amount']
    with open(path) as f:
        template = f.read(). \
            replace('{{amount}}', str(make_withdrawal['amount'])). \
            replace('{{asset}}', make_withdrawal['asset']). \
            replace('{{fee}}', f"{feeAmount} {feeAsset}"). \
            replace('{{ip}}', mail_parser['ip']). \
            replace('{{code}}', mail_parser['code']). \
            replace('{{htmlUrl}}', mail_parser['htmlUrl']). \
            replace('{{receiveAmount}}', str(receiveAmount)). \
            replace('{{destination}}', make_withdrawal['address'])

    data = create_temporary_template(mail_parser['message_body'], mail_object.get_template_name())
    os.remove(f"{mail_object.get_template_name()}.html")
    assert template == data, \
        f'Text from template: !\n{template}\n!\n\nText mess: !\n{data}\n!'
    return {"link": mail_parser['url'], "code": mail_parser['code']}


@then('User approve withdrawal by code')
def approve_withdrawal(check_withdrawal_email, make_withdrawal):
    counter = 0
    resp = Verify().verify_withdrawal(
        make_withdrawal['token'],
        make_withdrawal['withdrawalData']['operationId'],
        False
    )
    assert resp['status'] == 200
    assert resp['response']['result'] == 'OK'
    while True:
        balances = WalletHistory().operations_history(
            make_withdrawal['token'],
            make_withdrawal['asset']
        )['response']['data']
        counter += 1
        for item in balances:
            if make_withdrawal['request_id'] in item['operationId'] and \
                    item['status'] == 0 and \
                    item['balanceChange'] != 0:
                assert item['operationType'] == 1
                assert item['assetId'] == make_withdrawal['asset']
                assert item['balanceChange'] == make_withdrawal[
                    'amount'] * -1, f'Expected: {make_withdrawal["amount"] * -1}\nReturned: {item["balanceChange"]}\nItem: {item}'
                assert item['withdrawalInfo'] is not None
                assert item['withdrawalInfo']['toAddress'] == make_withdrawal['address']
                assert item['withdrawalInfo']['withdrawalAssetId'] == make_withdrawal['asset']
                assert item['withdrawalInfo']['withdrawalAmount'] == make_withdrawal['amount']
                assert item['withdrawalInfo']['isInternal'] == True
                assert str(item['withdrawalInfo']['feeAmount']) == settings.template_tests_fee_amoutn
                return
        if counter > 6:
            raise AttributeError(
                f'Can not find record operation history with status 1 and operationId like {make_withdrawal["request_id"]}')
        sleep(5)


###############################################################################################################################################

@when('User send request to forgot password endpoint')
def change_password(register):
    change_res = Auth(
        settings.template_tests_email,
        settings.template_tests_password
    ). \
        forgot_password(register['email'])['response']['result']
    assert change_res == 'OK'


@then('User get new email with code', target_fixture='parse_code')
def parse_code(create_temporary_template):
    mail_object = ParseMessage(1)
    recovery_data = mail_object.getMessage()
    assert type(recovery_data) == dict
    path = os.path.join(
        os.getcwd(),
        'templates',
        f'{mail_object.get_template_name()}.html'
    )
    with open(path) as f:
        template = f.read(). \
            replace('{{htmlUrl}}', recovery_data['htmlUrl']). \
            replace('{{code}}', recovery_data['code'])
    data = create_temporary_template(recovery_data['message_body'], mail_object.get_template_name())
    os.remove(f"{mail_object.get_template_name()}.html")
    assert template == data, f"Expected:!\n{template}\n!\nGets:!\n{data}\n!"
    return {'code': recovery_data['code']}


@then('User change password using code from email')
def change_password_with_code(parse_code, register):
    recovery_resp = Auth(register['email'], 'testpassword1'). \
        password_recovery('testpassword2', parse_code['code'])['response']['result']
    assert recovery_resp == 'OK', \
        f"Expected that result will be 'OK' but returned: {recovery_resp[0]}; Code: {parse_code['code']}; Email: {register['email']}"


@then('User can not auth with old password')
def log_in_with_new_password(auth, register):
    token = auth(
        register['email'],
        settings.template_tests_password,
        specific_case=True
    )
    assert token['status'] == 401
    assert token['response']['message'] == "InvalidUserNameOrPassword"


@then('User can auth with new password', target_fixture='log_in_with_new_password')
def log_in_with_new_password(auth, register):
    token = auth(
        register['email'],
        'testpassword2'
    )['response']['data']['token']
    assert type(token) == str
    return {"token": token}


##############################################################################################################


@given('ReRegistration mail on inbox after existing user pass registration')
def register_n_check_email(create_temporary_template):
    token = Auth(settings.template_tests_email, 'testpassword1').\
        register()['response']['data']
    assert type(token) == dict, f'Expected response type: dict\nReturned: {token}'
    assert len(token) == 2
    mail_object = ParseMessage(3)
    mail_parser = mail_object.getMessage()
    assert type(mail_parser) == dict, f"Expected type dict; Returned: {mail_parser}"
    path = os.path.join(
        os.getcwd(),
        'templates',
        f'{mail_object.get_template_name()}.html'
    )

    with open(path) as f:
        template = f.read(). \
            replace('{{htmlUrl}}', mail_parser['htmlUrl'])
    data = create_temporary_template(mail_parser['message_body'], mail_object.get_template_name())
    os.remove(f"{mail_object.get_template_name()}.html")

    assert template == data, f"Expected:\n\n\nReturned: {2}"

# @scenario(f'../features/receive_email.feature', 'Success withdrawal or transfer && deposit')
# def test_success_deposit_withdrawal():
#     pass

# @given(parsers.parse("User send withdrawal/transfer with asset: {asset}, to address/phone {address_phone}"), target_fixture="create_operation")
# def create_operation(auth, asset, address_phone):
#     token = auth(settings.template_tests_email, settings.template_tests_password )
#     amount = settings.balance_asssets[asset] / 2
#     if address_phone.startswith('+'):
#         operation = Transfer().create_transfer(token, address_phone, asset, amount)
#         operation_type = 'transfer'
#     else:
#         operation = Blockchain().withdrawal(token, asset, amount, address_phone)
#         operation_type = 'withdrawal'

#     assert type(operation) == dict, f"Expected that operation will be dict, but returned: {operation}"

#     return {
#                 "type": operation_type,
#                 "operationId": operation['operationId'], 
#                 "token": token, 
#                 "requestId": operation['requestId'], 
#                 "asset": asset, 
#                 "amount": amount
#             }

# @when("User approve withdrawal/transfer by restApi", target_fixture="approve_opetarion")
# def approve_opetarion(create_operation):
#     #Ожидание когда вывод станет в статус ApprovalPending
#     counter = 0
#     while True:
#         sleep(5)
#         counter += 1
#         op_history = WalletHistory().operations_history(create_operation['token'], create_operation['asset'])
#         assert type(op_history) == list
#         pending_operation = list(
#             filter(
#                 lambda x: create_operation["requestId"] in x['operationId'],
#                 op_history
#             )
#         )
#         if  len(pending_operation) == 1 and \
#             pending_operation[0]['status'] == 1:
#             break
#         elif counter > 5:
#             raise ValueError('Can not find operations with status 0 for 15 seconds')
#     event_date = datetime.strptime(
#         datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
#         '%d-%m-%Y %H:%M:%S'
#     )
#     if create_operation['type'] == 'withdrawal':
#         approve_resp = Verify().verify_withdrawal(create_operation['token'], create_operation['operationId'])
#     else:
#         approve_resp = Verify().verify_transfer(create_operation['token'], create_operation['operationId'])
#     assert approve_resp == 'Simple | Buy, sell and manage cryptocurrency portfolios'
#     return {"event_date": event_date}

# @then("User has new success withdrawal email")
# def check_success_withdrawal_email(create_operation, approve_opetarion):
#     counter = 0
#     while True:
#         sleep(5)
#         counter += 1
#         op_history = WalletHistory().operations_history(create_operation['token'], create_operation['asset'])
#         assert type(op_history) == list
#         approved_withdrawal = list(
#             filter(
#                 lambda x: create_operation["requestId"] in x['operationId'],
#                 op_history
#             )
#         )
#         if  len(approved_withdrawal) == 1 and \
#             approved_withdrawal[0]['status'] == 0:
#             break
#         elif counter > 5:
#             raise ValueError('Can not find operations with status 0 for 15 seconds') 
#     success_withdrawal = MailParser(6, settings.template_tests_email, approve_opetarion['event_date'], withdrawal_asset = create_operation['asset'] ).parse_mail()
#     assert type(success_withdrawal) == dict
#     path = os.path.join(
#         os.getcwd(),
#         'email_templates',
#         'Withdrawal_successful.txt'
#     )
#     with open(path) as f:
#         template = f.read().\
#              replace('{{amount}}', str(create_operation['amount'])).\
#                 replace('{{asset}}', str(create_operation['asset']))
#     assert template == success_withdrawal['message_body'], f"Exception with Withdrawal_successful template\nExpected:!\n{template}\n!\nGets:!\n{success_withdrawal['message_body']}\n!"

# @then(parsers.parse("Receive user with email {email} has new success deposit email"))
# def check_success_deposit_email(email, create_operation, approve_opetarion):
#     success_withdrawal = MailParser(7, email, approve_opetarion['event_date']).parse_mail()
#     assert type(success_withdrawal) == dict
#     path = os.path.join(
#         os.getcwd(),
#         'email_templates',
#         'Deposit_successful.txt'
#     )
#     with open(path) as f:
#         template = f.read().\
#             replace('{{amount}}', str(create_operation['amount'])).\
#                 replace('{{asset}}', str(create_operation['asset']))
#     assert template == success_withdrawal['message_body'], f"Exception with Deposit_successful template\nExpected:!\n{template}\n!\nGets:!\n{success_withdrawal['message_body']}\n!"
