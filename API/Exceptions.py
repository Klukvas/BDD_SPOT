class RequestError(Exception):
    def __init__(self, url, status_code, message=None):
        self.url = url
        self.status_code = status_code
        self.message = message

    def __str__(self):
        msg = f'Negative status code from {self.url}. Status code is {self.status_code}'
        if self.message:
            msg += f'\n{self.message}'
        return msg

class SomethingWentWrong(Exception):
    def __init__(self, r):
        self.r = r

    def __str__(self):
        return f"Something went wrong. requests lib didn't return response. It returns {type(self.r)}"

class CantParseJSON(Exception):
    def __init__(self, url, response_text, status_code, *args):
        self.url = url
        self.response_text = response_text
        self.status_code = status_code
        if len(args):
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        msg = f"Can not parse json\n" \
              f"{self.url} status code is {self.status_code}\n" \
              f"Response text is:\n" \
              f"{self.response_text}"
        if self.message:
            msg += f'\nException message is:\n' \
                   f'{self.message}'
        return msg


class MessageNotFound(Exception):
    pass

class SoupGeneratingError(Exception):
    pass


class TooManyMessagesFound(Exception):
    pass


class CanNotFindTemplateData(Exception):
    pass


class CanNotFindKey(Exception):
    def __init__(self, url, message=None):
        self.url = url
        self.message = message

    def __str__(self):
        msg = f'Response from {self.url} is not contains all needed keys.'
        if self.message:
            msg += f'\nException message:\n{self.message}'
        return msg


class ParsingError(Exception):
    pass

#
#
# class ExceptionsFabric:
#
#     def __init__(self, name, add_data) -> None:
#         self.name = name
#         self.add_data = add_data
#
#     def generate_exceprion(self):
#         ex = type(self.name, (Exception,), {})
#         return ex
#
#
# raise ExceptionsFabric('TooMuchRequests').generate_exceprion()('asdasdas')
