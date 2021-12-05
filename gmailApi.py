import requests
from bs4 import BeautifulSoup
from datetime import datetime as dateTime
from time import sleep
import re


class MailParser:

    def __init__(self, email_type, email, date_time_action, *args):
        self.counter = 0
        self.args = args
        self.date_time_action = date_time_action
        self.current_reason = email_type
        self.mail_types = {
            0: 'Email confirmation request',
            1: '[Monfex] Success Login from',
            2: 'Verify transfer',
            3: 'Verify withdrawal',
            4: 'Password recoverу'
        }
        self.email = email
        self.main_domain = 'https://www.mailforspam.com'

    def get_html(self):
        response = requests.get(
            f'{self.main_domain}/mail/{self.email}'
        )
        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                return {'soup': soup}
            except Exception as err:
                return [response, err]
        else:
            return [response, response.status_code]

    def parse_inbox(self):
        counter = 0
        while True:
            html = self.get_html()
            if type(html) != dict:
                print(f'Some error: {html}')
                return html
            emails_table = html['soup'].find('table', id='mailbox')
            emails = emails_table.findAll('tr')
            for num, email in enumerate(emails):
                _from = email.find("td")
                if _from is not None:
                    _from = _from.text.strip()
                    if _from == 'Simple <noreply@simple-spot.biz>':
                        data = email.findAll('td')
                        reason = data[1].text.strip()
                        url_to_mail = data[1].find('a')['href']
                        send_date = data[2].text.strip()
                        send_date = dateTime.strptime(
                            send_date,
                            '%d-%m-%Y %H:%M:%S'
                        )
                        if send_date >= self.date_time_action and \
                                reason == self.mail_types[self.current_reason] or \
                                self.mail_types[self.current_reason] in reason:
                            return {'from': _from, 'reason': reason, 'url': url_to_mail}
            if counter == 6:
                print('Can not find needed email for 60s')
                return None
            counter += 1
            sleep(10)

    def parse_mail(self, *args):
        if self.counter > 5:
            return 0
        else:
            email_data = self.parse_inbox()
            if not email_data:
                print('here is no email data')
                return None
            response = requests.get(
                f'{self.main_domain}{email_data["url"]}'
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            message_body = soup.find('p', id="messagebody")
            if self.current_reason == 0:
                code = re.search('\d+', message_body.text.strip()).group(0)
                app_link = re.search('Open in Application \(.+\)',message_body.text.strip()).group(0)
                return {'message_body': message_body.text.strip(), 'code': code, 'app_link': app_link}
            elif self.current_reason == 1:
                ip = re.search(r'IP address: ([0-9]|\.)*',  message_body.text.strip()).group(0)
                time = re.search(r'Time: ([0-9]|\-)*\s([0-9]|:)*\sUTC',  message_body.text.strip()).group(0)
                return {'ip': ip, 'time': time, 'message_body': message_body.text.strip()}
            elif self.current_reason == 4:
                token = re.search('jw_token.+', message_body.text.strip()).group(0).\
                    split('%3d')[1].\
                        split('%26')[0]
                return {'token': token, 'message_body': message_body.text.strip()}
            elif self.current_reason in [2,3]:
                ip = re.search(r'Your IP: ([0-9]|\.)*',  message_body.text.strip()).group(0)
                confirm_link = re.search(f'https:\/\/val([A-Z]|[a-z]|\-|[0-9]|\=|\.|\/|\?|&)*', message_body.text.strip()).group(0)
                if self.args[0] in confirm_link:
                    return {'ip': ip, 'message_body': message_body.text.strip(), 'confirm_link': confirm_link}
                else:
                    self.counter += 1
                    sleep(8)
                    return self.parse_mail()
            else:
                return {'message_body': message_body.text.strip()}

            

if __name__ == '__main__':
    datetime_today = dateTime.strptime(
        dateTime.today().strftime('%d-%m-%Y %H:%M:%S'),
        '%d-%m-%Y %H:%M:%S'
    )
    tes = MailParser(4, 'asd2323', datetime_today).parse_mail()
    print(tes)
