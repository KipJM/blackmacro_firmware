import time

from usb.device.hid import HIDInterface


class HIDModule:

    def get_interface(self) -> HIDInterface:
        pass

    # async def init_hid(self, poll_rate: int = 100): # ms, yes it's inconsistent with Sysmodule but i dont care
    #     while not self.get_interface().is_open():
    #         time.sleep_ms(poll_rate)
    #     time.sleep_ms(poll_rate) # wait a bit more
    #     return