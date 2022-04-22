class RequestError(Exception):
    pass

class SomethingWentWrong(Exception):
    pass

class CantParseJSON(Exception):
    pass

class MessageNotFound(Exception):
    pass

class TooManyMessagesFound(Exception):
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
