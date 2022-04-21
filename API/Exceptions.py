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