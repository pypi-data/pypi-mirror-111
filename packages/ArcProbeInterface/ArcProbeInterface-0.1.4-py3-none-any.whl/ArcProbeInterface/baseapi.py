import json
import re
from abc import ABC, abstractmethod
from typing import Optional

import brotli

from .exceptions import InvalidUserCodeException, UnexpectedDataTypeException


class API(ABC):
    user_code: str
    start_const: int
    end_const: int
    timeout: Optional[int]

    def __init__(self, user_code, start=8, end=12, timeout=None):
        if not re.fullmatch(r'\d{9}', user_code):
            raise InvalidUserCodeException(f"\"{user_code}\" is not a valid user code.")
        self.user_code = user_code
        self.start_const = start
        self.end_const = end
        self.timeout = timeout

    @abstractmethod
    def fetch_data(self):
        pass

    def manage_data(self, raw_data, container):
        if isinstance(raw_data, str):
            print(raw_data)
            if raw_data == 'error,invalid user code':
                raise InvalidUserCodeException(f"User code \"{self.user_code}\" was refused by the WebSocket.")
            if raw_data == 'error,add':
                raise WebSocketIsDownException("The Redive Websocket is down :c")
            if raw_data == 'bye':
                return True
        elif isinstance(raw_data, bytes):
            byte_data = brotli.decompress(raw_data)
            dict_data = json.loads(byte_data.decode('utf-8'))
            if isinstance(dict_data['data'], list):
                for elm in dict_data['data']:
                    container[dict_data['cmd']].append(elm)
            else:
                container[dict_data['cmd']] = dict_data['data']
        else:
            raise UnexpectedDataTypeException(
                f"Expected str or bytes to be received, actually received {type(raw_data)}.")
        return False
