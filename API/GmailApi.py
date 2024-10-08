from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from time import sleep
try:
    import API.Exceptions as Exceptions
except ModuleNotFoundError:
    import Exceptions as Exceptions

from bs4 import BeautifulSoup
import os


SCOPES = ['https://mail.google.com/']


class GmailApi:
    def __init__(self) -> None:
        pass

    def _deleteParsedMessage(self):
        result = self._service.users().messages().list(
            userId='me'
        ).execute()
        if result['resultSizeEstimate'] > 0:
            for item in result['messages']:
                self._service.users().messages().delete(userId='me', id=item['id']).execute()

    def generateCreds(self):

        try:
            path = os.path.join(
                os.getcwd(),
                'token.json'
            )
            self._creds = Credentials.from_authorized_user_file(path, SCOPES)
        except:
            path = os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.getcwd(), os.pardir
                    )
                ), 'token.json'
            )
            self._creds = Credentials.from_authorized_user_file(path, SCOPES)

    

    def generateService(self):
        self._service = build('gmail', 'v1', credentials=self._creds)

    def getMessageId(self, subject):
        counter = 0
        while True:
            result = self._service.users().messages().list(
                userId='me',
                q=f'from:Simple subject:({subject})',
                includeSpamTrash=False
            ).execute()
            if result['resultSizeEstimate'] <= 0 and counter > 10:
                raise Exceptions.MessageNotFound(f"Can not find message of {subject} for 2 mins")
            elif result['resultSizeEstimate'] > 1:
                raise Exceptions.TooManyMessagesFound(
                    f"Found too many messages({result['resultSizeEstimate']}) of {subject}")
            elif result['resultSizeEstimate'] == 1:
                return result['messages'][0]['id']
            counter += 1
            sleep(20)

    def getMessageById(self, id):
        messageData = self._service.users().messages().get(userId='me', id=id).execute()
        return messageData

    def decoder(self, message):
        return base64.urlsafe_b64decode(
            message + '=' * (-len(message) % 4)
        ).decode(encoding='utf-8')

    def textViewSerializer(self, messageText):
        newMessageText = messageText.replace('amp;', '')
        return newMessageText

    def parseMessage(self, messageData):
        result = {}
        for part in messageData['payload']['parts']:
            message = self.decoder(part['body']['data'])
            if part['mimeType'] == 'text/plain':
                result['textView'] = self.textViewSerializer(message)
            elif part['mimeType'] == 'text/html':
                result['htmlView'] = message
            else:
                raise KeyError(f"Unexpected mimeType: {part['mimeType']}")
        return result

    def main(self, subject):
        try:
            self.generateCreds()
        except Exception as err:
            raise Exception(f"Error of generating creds\n Error: {err}")
        try:
            self.generateService()
        except Exception as err:
            raise Exception(f"Error of generating Service\n Error: {err}")
        try:
            messageId = self.getMessageId(subject)
        except Exception as err:
            raise Exception(f"Error of getting message id.\n Error: {err}")
        msgData = self.getMessageById(messageId)
        parsedMessage = self.parseMessage(msgData)
        return parsedMessage


class ParseMessage:

    def __init__(self, searchedType) -> None:
        self.api = GmailApi()
        self.mailsEnum = {
            1: 'Password recovery',
            2: 'Success Login from IP',
            3: 'Your account already exist',
            4: 'Verify transfer',
            5: 'Verify withdrawal',
            6: 'Withdrawal declined',
            7: 'Transfer declined',
            8: 'Deposit successful',
            9: 'Withdrawal successful',
            10: 'Email confirmation request'
        }
        self.funcsEnum = {
            1: self.passwordRecoveryParser,
            2: self.successLoginParser,
            3: self.reRegistrationParser,
            4: self.transferParser,
            5: self.withdrawalPerser,
            6: self.wdDeclinedParser,

            8: self.dpSuccessfulParser,
            9: self.wdSuccssesParser,
            10: self.emailConfirmationParser
        }
        self.searchedType = searchedType

    def get_template_name(self):
        return self.mailsEnum[self.searchedType]

    def getMessage(self, templateSaver=False):
        messageData = self.api.main(
            self.mailsEnum[self.searchedType]
        )
        assert messageData, \
            f"Can not find message with theme: {self.mailsEnum[self.searchedType]}\nmessageData: {messageData}"
        if templateSaver:
            self.saveTemplate(messageData['htmlView'])
        try:
            soup = self.createSoup(messageData['htmlView'])
        except Exception as error:
            raise Exceptions.SoupGeneratingError(
                f"Can not create soup of {self.searchedType}\nError: {error}"
            )
        try:
            templateData = self.funcsEnum[
                self.searchedType
            ](soup)
        except Exception as error:
            raise Exceptions.CanNotFindTemplateData(
                f"Can not get data of template: {self.saveTemplate()} with error: {error}"
            )
        templateData['message_body'] = messageData['htmlView']
        return templateData

    def saveTemplate(self, html):

        try:
            with open(f"templates/{self.mailsEnum[self.searchedType]}.html", 'w') as f:
                f.writelines(html)
        except:
            path = os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.getcwd(), os.pardir
                    )
                ), 'templates', self.mailsEnum[self.searchedType]
            )
            with open(f"{path}.html", 'w') as f:
                f.writelines(html)

    def createSoup(self, html:str) -> BeautifulSoup:

        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def emailConfirmationParser(self, soup: BeautifulSoup) -> dict:
        confirmUrl = soup.find_all('tr')[8].find('a')['href']
        htmlConfirUrl = confirmUrl.replace('&', '&amp;')
        code = soup.find_all('tr')[12]. \
            find('div'). \
            findAll('div')[1]. \
            text.strip()
        return {
            "confirmUrl": confirmUrl,
            "htmlConfirUrl": htmlConfirUrl,
            "code": code
        }

    def dpSuccessfulParser(self, soup: BeautifulSoup) -> dict:
        tableParts = soup.find_all('tr')
        dpData = tableParts[10].find_all('div')[1].text.strip()
        return {"dpData": dpData}

    def wdDeclinedParser(self, soup: BeautifulSoup) -> dict:
        amount, asset = soup.find_all('tr')[6]. \
            find('div'). \
            text. \
            replace('Withdrawal of ', ''). \
            replace(' from your Simple account', ''). \
            strip(). \
            split(' ')
        return {
            "amount": amount,
            "asset": asset
        }

    def wdSuccssesParser(self, soup: BeautifulSoup) -> dict:
        tableParts = soup.find_all('tr')
        name = tableParts[6].text. \
            split(',')[0]. \
            strip(). \
            replace('Dear', '')
        amount, asset = tableParts[10].find_all('div')[1].text.split(' ')
        return {
            "amount": amount,
            "asset": asset,
            "name": name
        }

    def withdrawalPerser(self, soup: BeautifulSoup) -> dict:
        tableParts = soup.find_all('tr')
        amount, asset = tableParts[8].find_all('div')[1].text.split(' ')
        fee = tableParts[9].find_all('div')[1].text
        destination = tableParts[11].find_all('div')[0].text

        ip = tableParts[16].find_all('div')[1].text
        url = tableParts[18].find('a')['href']
        htmlUrl = url.replace('&', '&amp;')
        code = tableParts[22].find_all('div')[2].text.strip()
        return {
            "amount": amount,
            "asset": asset,
            "fee": fee,
            "destination": destination,
            "ip": ip,
            "url": url,
            "code": code,
            "htmlUrl": htmlUrl
        }

    def transferParser(self, soup: BeautifulSoup) -> dict:
        tableParts = soup.find_all('tr')
        amount, asset = tableParts[8].find_all('div')[1].text.split(' ')
        destination = tableParts[9].find_all('div')[1].text
        ip = tableParts[13].find_all('div')[1].text
        url = tableParts[15].find('a')['href']
        htmlUrl = url.replace('&', '&amp;')
        code = tableParts[19].find_all('div')[2].text.strip()
        return {
            "amount": amount,
            "asset": asset,
            "destination": destination,
            "ip": ip,
            "url": url,
            "code": code,
            "htmlUrl": htmlUrl
        }

    def successLoginParser(self, soup: BeautifulSoup) -> dict:
        tableParts = soup.find_all('tr')
        time = tableParts[11].find_all('div')[1].text.strip()
        ip = tableParts[12].find_all('div')[1].text.strip()
        return {"time": time, "ip": ip}

    def passwordRecoveryParser(self, soup: BeautifulSoup) -> dict or int:
        try:
            url = soup.find_all('tr')[8].find('a')['href']
            htmlUrl = url.replace('&', '&amp;')
            code = url.split('26jw_code%3d')[1].split('&apn')[0]
            return {"url": url, "htmlUrl": htmlUrl, "code": code}
        except:
            return 0

    def reRegistrationParser(self, soup: BeautifulSoup) -> dict:
        loginUrl = soup.find_all('tr')[8].find('a')['href']
        htmlLoginUrl = loginUrl.replace('&', '&amp;')
        return {
            "url": loginUrl,
            "htmlUrl": htmlLoginUrl
        }


if __name__ == "__main__":
    api = ParseMessage(2).getMessage()
    print(api)

