import asyncio
import sys


class SysModule:
    def __init__(self, delta: float):
        self.delta = delta
        self.loop = asyncio.create_task(self.update_loop())

    async def update_loop(self):
        while True:
            try:
                await self.update()
            except Exception as e:
                print()
                print("========== SYSMODULE CRASH =========")
                print(f"=== MODULE: {self.__class__.__name__} ===")
                print(e)
                sys.print_exception(e)
                print("====================================")
                print()
                return
            await asyncio.sleep(self.delta)

    async def update(self):
        pass