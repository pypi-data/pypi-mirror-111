class APIException(Exception):
    pass


class InvalidUserCodeException(APIException):
    pass


class UnexpectedDataTypeException(APIException):
    pass

class WebSocketIsDownException(APIException):
    pass
