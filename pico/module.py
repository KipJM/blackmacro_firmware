import asyncio


class LoopModule:
    def __init__(self, delta: float):
        self.delta = delta
        self.loop = asyncio.create_task(self.update_loop())

    async def update_loop(self):
        while True:
            self.update()
            await asyncio.sleep(self.delta)

    def update(self):
        pass
