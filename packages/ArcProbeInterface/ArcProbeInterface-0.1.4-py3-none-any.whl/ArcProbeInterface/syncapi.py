from websocket import create_connection

from .baseapi import API


class SyncAPI(API):

    def fetch_data(self):
        result = {"scores": []}
        conn = create_connection("wss://arc.estertion.win:616", timeout=self.timeout)
        conn.send(f"{self.user_code} {self.start_const} {self.end_const}")
        while True:
            _r = conn.recv()
            if self.manage_data(_r, result):
                break
        return result
