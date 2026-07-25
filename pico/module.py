import asyncio


class SysModule:
    def __init__(self, delta: float):
        self.delta = delta
        self.loop = asyncio.create_task(self.update_loop())

    async def update_loop(self):
        while True:
            await self.update()
            await asyncio.sleep(self.delta)

    async def update(self):
        pass
