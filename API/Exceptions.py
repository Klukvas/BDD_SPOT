class RequestError(Exception):
    def __init__(self, url, status_code, *args):
        self.url = url
        self.status_code = status_code
        if args:
            self.message = args[0]

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
    pass

class MessageNotFound(Exception):
    pass

class SoupGeneratingError(Exception):
    pass

class TooManyMessagesFound(Exception):
    pass

class CanNotFindTemplateData(Exception):
    pass

class CanNotFindKey(Exception):
    pass

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
