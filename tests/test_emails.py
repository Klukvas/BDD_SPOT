from API import Auth
from pytest_bdd import scenario, given, then
import os
import uuid
from gmailApi import MailParser
from datetime import datetime

@scenario(f'{os.path.join(os.path.abspath(".."),"BDD_SPOT","features","receive_email.feature")}', 'Email confirmation')
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


@then('User has new email with code', target_fixture="get_email_data")
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

@then('User can verify email by code from mail', target_fixture="check_op")
def verify_email(get_email_data):
    pass
