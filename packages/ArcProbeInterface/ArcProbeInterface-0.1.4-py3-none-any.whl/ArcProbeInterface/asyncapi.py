import websockets

from .baseapi import API


class AsyncAPI(API):

    async def fetch_data(self):
        result = {"scores": []}
        async with websockets.connect("wss://arc.estertion.win:616", timeout=self.timeout) as conn:
            await conn.send(f"{self.user_code} {self.start_const} {self.end_const}")
            while True:
                _r = await conn.recv()
                if self.manage_data(_r, result):
                    break
        return result
