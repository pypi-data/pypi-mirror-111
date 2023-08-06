class APIException(Exception):
    pass


class InvalidUserCodeException(APIException):
    pass


class UnexpectedDataTypeException(APIException):
    pass
