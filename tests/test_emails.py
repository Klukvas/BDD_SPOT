from time import sleep
from requests.api import request
from API import Auth, Verify, Transfer, WalletHistory
from pytest_bdd import scenario, given, then, when
import uuid
from gmailApi import MailParser
from datetime import datetime
import settings
import requests

@scenario(f'../features/receive_email.feature', 'Email confirmation')
def test_emails():
    pass

@given('User registration', target_fixture="register")
def register():
    email = 'emailtest' + str(uuid.uuid4()) + '@mailforspam.com'
    print(f'email: {email}')
    datetime_today = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    token = Auth(email, 'testpassword1', 1).register()
    assert type(token) == list
    assert len(token) == 2
    return [token, email, datetime_today]

@given('User has new email with code', target_fixture="get_email_data")
def get_email_data(register):
    mail_parser = MailParser(0, register[1],  register[2]).parse_mail()
    assert type(mail_parser) == dict
    assert len(mail_parser.keys()) == 3
    with open('/Users/andrey.p/Desktop/BDD_SPOT/email_templates/Email_confirmation_request_mock.txt') as f:
        template = f.read()
    assert template.\
        replace('{{come_code_here}}', mail_parser['code']).\
            replace('{{link}}', mail_parser['app_link']) == \
           mail_parser['message_body'], f'Text from template: !\n{template.replace("{{come_code_here}}", mail_parser["code"])}\n!\n\nText mess: !\n{mail_parser["message_body"]}\n!'
    return {'code': mail_parser['code']}

@when('User can verify email by code from mail', target_fixture="check_op")
def verify_email(register, get_email_data):
    verify = Verify(1).verify_email(register[0][0], get_email_data['code'])
    assert verify['data'] == 'OK'

@then('User`s email is veryfied', target_fixture="check_op")
def check_email_verified(register):
    auth_data = Verify(1).client_data(register[0][0])
    assert type(auth_data) == dict, f'Expected that email ll be verifyed but:{auth_data}'
    assert auth_data['data']['emailVerified'] == True

@scenario(f'../features/receive_email.feature', 'Success login')
def test_success_login():
    pass

@given('User has new Success login email after login')
def log_in(auth):
    tokens = auth(settings.template_email, settings.password)
    datetime_today = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    mail_parser = MailParser(1, settings.template_email, datetime_today).parse_mail()
    assert type(mail_parser) == dict
    assert len(mail_parser.keys()) == 3
    with open('/Users/andrey.p/Desktop/BDD_SPOT/email_templates/Success_Login.txt') as f:
        template = f.read()
    assert template.\
        replace('{{email}}', settings.template_email).\
            replace('{{time}}', mail_parser['time']).\
                replace('{{ip}}', mail_parser['ip']) == \
           mail_parser['message_body'], f'Text from template: !\n{template.replace("{{come_code_here}}", mail_parser["code"])}\n!\n\nText mess: !\n{mail_parser["message_body"]}\n!'




@scenario(f'../features/receive_email.feature', 'Transfer')
def test_success_transfer_email():
    pass

@given('User send transfer', target_fixture='make_transfer')
def make_transfer(auth):
    token = auth(settings.template_email, settings.password )
    assert type(token) == str
    datetime_today = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    transferData = Transfer(1).create_transfer(
        token,
        settings.transfer_to_phone_with_confirm_email,
        settings.asset_to_send,
        settings.balance_asssets[settings.asset_to_send] / 2
    )
    assert type(transferData) == dict, f'Expected that response will be dict, but gets: {type(transferData)}\nTransferData: {transferData}.Asset:{"LTC"}\tAmount: {settings.balance_asssets["LTC"] / 2}'
    assert type(transferData['transferId']) == str
    return [transferData, 'LTC', datetime_today, token]

@when('User has new email with appove link', target_fixture='check_transfer_email')
def check_transfer_email(make_transfer):
    mail_parser = MailParser(2, settings.template_email, make_transfer[2]).parse_mail()
    with open('/Users/andrey.p/Desktop/BDD_SPOT/email_templates/Verify transfer.txt') as f:
        template = f.read()
    template = template.\
        replace('{{amount}}', str(settings.balance_asssets[settings.asset_to_send] / 2)).\
            replace('{{asset}}', settings.asset_to_send).\
                replace('{{ip}}', mail_parser['ip']).\
                    replace('{{phone_to}}', settings.transfer_to_phone_with_confirm_email).\
                        replace('{{link}}', mail_parser['confirm_link'])
    assert template == \
           mail_parser['message_body'], \
               f'Text from template: !\n{template}\n!\n\nText mess: !\n{mail_parser["message_body"]}\n!'
    return [mail_parser['confirm_link']]

@then('User approve transfer by link')
def approve_transfer(check_transfer_email, make_transfer):
    counter = 0
    resp = requests.get(check_transfer_email[0])
    assert resp.status_code == 200
    while True:
        balances = WalletHistory(1).operations_history(make_transfer[3], settings.asset_to_send)
        counter += 1
        for item in balances:
            if make_transfer[0]['requestId'] in item['operationId'] or \
                make_transfer[0]['requestId'] == item['operationId'] and item['status'] == 1:
                return
        if counter > 6:
            raise AttributeError(f'Can not find record operation history with status 1 and operationId like {make_transfer[0]["requestId"]}')
        sleep(5)