from time import sleep
from requests.api import request
from API import Auth, Blockchain, Verify, Transfer, WalletHistory
from pytest_bdd import scenario, given, then, when, parsers
import uuid
from gmailApi import MailParser
from datetime import datetime
import settings
import requests

@scenario(f'../features/receive_email.feature', 'Email confirmation')
def test_email_confirmation():
    pass

@given('User registration', target_fixture="register")
def register():
    email = 'emailtest' + str(uuid.uuid4()) + '@mailforspam.com'
    datetime_today = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    token = Auth(email, 'testpassword1', 1).register()
    assert type(token) == list
    assert len(token) == 2
    return {"token": token, "email": email, "datetime_today": datetime_today}

@given('User has new email with code', target_fixture="get_email_data")
def get_email_data(register):
    mail_parser = MailParser(0, register['email'],  register["datetime_today"]).parse_mail()
    assert mail_parser
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
    verify = Verify(1).verify_email(register['token'][0], get_email_data['code'])
    assert verify['data'] == 'OK'

@then('User`s email is veryfied', target_fixture="check_op")
def check_email_verified(register):
    auth_data = Verify(1).client_data(register['token'][0])
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
    assert mail_parser
    assert type(mail_parser) == dict
    assert len(mail_parser.keys()) == 3
    with open('/Users/andrey.p/Desktop/BDD_SPOT/email_templates/Success_Login.txt') as f:
        template = f.read()
    assert template.\
        replace('{{email}}', settings.template_email).\
            replace('{{time}}', mail_parser['time']).\
                replace('{{ip}}', mail_parser['ip']) == \
           mail_parser['message_body'], f'Text from template: !\n{template.replace("{{come_code_here}}", mail_parser["code"])}\n!\n\nText mess: !\n{mail_parser["message_body"]}\n!'




@scenario(f'../features/receive_email.feature', 'Transfer(waiting for user)')
def test_success_transfer_email():
    pass

@given(parsers.parse('User send transfer with asset: {asset}, amount: {amount}, to phone {phone}'), target_fixture='make_transfer')
def make_transfer(asset, amount, phone, auth):
    token = auth(settings.template_email, settings.password )
    assert type(token) == str
    datetime_today = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    transferData = Transfer(1).create_transfer(
            token, phone, asset, amount
        )
    assert type(transferData) == dict, f'Expected that response will be dict, but gets: {type(transferData)}\nTransferData: {transferData}.Asset:{asset}\tAmount: {amount}\t {type(amount)}'
    assert type(transferData['transferId']) == str
    return {"transferData": transferData, "asset": asset, "amount": amount, "phone": phone, "datetime_today": datetime_today, "token": token}

@when('User has new email with appove link', target_fixture='check_transfer_email')
def check_transfer_email(make_transfer):
    mail_parser = MailParser(2, settings.template_email, make_transfer['datetime_today']).parse_mail()
    assert mail_parser
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
    return {"confirm_link": mail_parser['confirm_link']}

@then('User approve transfer by link')
def approve_transfer(check_transfer_email, make_transfer):
    counter = 0
    resp = requests.get(check_transfer_email['confirm_link'])
    assert resp.status_code == 200
    while True:
        balances = WalletHistory(1).operations_history(make_transfer['token'], settings.asset_to_send)
        counter += 1
        for item in balances:
            if make_transfer['transferData']['requestId'] in item['operationId'] or \
                make_transfer['transferData']['requestId'] == item['operationId'] and item['status'] == 1:
                return
        if counter > 6:
            raise AttributeError(f'Can not find record operation history with status 1 and operationId like {make_transfer["transferData"]["requestId"]}')
        sleep(5)




@scenario(f'../features/receive_email.feature', 'Internal withdrawal')
def test_success_withdrawal_email():
    pass

@given(parsers.parse('User send withdrawal request wiht asset: {asset}, amount: {amount} to address: {address}'), target_fixture='make_withdrawal')
def make_withdrawal(auth, asset, amount, address):
    token = auth(settings.template_email, settings.password )
    assert type(token) == str
    datetime_today = datetime.strptime(
        datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    withdrawalData = Blockchain(1).withdrawal(
        token, asset, amount, address
    )
    assert type(withdrawalData) == dict, f'Expected that response will be dict, but gets: {type(withdrawalData)}\nTransferData: {withdrawalData}.Asset:{settings.asset_to_send}\tAmount: {settings.balance_asssets[settings.asset_to_send] / 2}'
    assert type(withdrawalData['operationId']) == str
    return {
                "withdrawalData": withdrawalData, "datetime_today": datetime_today, 
                "token": token, "asset": asset, "amount": amount, "address": address
            }

@when('User has new email with appove withdwal link', target_fixture='check_withdrawal_email')
def check_withdrawal_email(make_withdrawal):
    mail_parser = MailParser(3, settings.template_email, make_withdrawal['datetime_today'], make_withdrawal['withdrawalData']['operationId']).parse_mail()
    assert mail_parser != None, f'Expected that email ll be finded'
    with open('/Users/andrey.p/Desktop/BDD_SPOT/email_templates/Verify withdrawal.txt') as f:
        template = f.read()
    template = template.\
        replace('{{amount}}', make_withdrawal['amount']).\
            replace('{{asset}}', make_withdrawal['asset']).\
                replace('{{feeAmount}}', 0).\
                    replace('{{feeAsset}}', make_withdrawal['asset']).\
                        replace('{{ip}}', mail_parser['ip']).\
                            replace('{{link}}', mail_parser['confirm_link']).\
                                replace('{{address}}', make_withdrawal['address'])
    assert template == \
           mail_parser['message_body'], \
               f'Text from template: !\n{template}\n!\n\nText mess: !\n{mail_parser["message_body"]}\n!'
    return [mail_parser['confirm_link']]

@then('User approve withdrawal by link')
def approve_withdrawal(check_withdrawal_email, make_withdrawal):
    counter = 0
    resp = requests.get(check_withdrawal_email[0])
    assert resp.status_code == 200
    while True:
        balances = WalletHistory(1).operations_history(make_withdrawal['token'], settings.asset_to_send)
        counter += 1
        for item in balances:
            if ( make_withdrawal['withdrawalData']['requestId'] in item['operationId'] or \
                make_withdrawal['withdrawalData']['requestId'] == item['operationId'] ) and \
                item['status'] == 0 and \
                    item['balanceChange'] != 0:
                assert item['operationType'] == 1
                assert item['assetId'] == settings.asset_to_send
                assert item['balanceChange'] == (settings.balance_asssets[settings.asset_to_send] / 2)*-1, f'Expected: {(settings.balance_asssets[settings.asset_to_send] / 2)*-1}\nReturned: {item["balanceChange"]}\nItem: {item}'
                assert item['withdrawalInfo'] !=  None
                assert item['withdrawalInfo']['toAddress'] ==  settings.asset_blockchain_address
                assert item['withdrawalInfo']['withdrawalAssetId'] == settings.asset_to_send
                assert item['withdrawalInfo']['withdrawalAmount'] == settings.balance_asssets[settings.asset_to_send] / 2
                assert item['withdrawalInfo']['isInternal'] == True
                assert str(item['withdrawalInfo']['feeAmount']) == settings.fee_amount
                return
        if counter > 6:
            raise AttributeError(f'Can not find record operation history with status 1 and operationId like {make_withdrawal["withdrawalData"]["requestId"]}')
        sleep(5)
