import asyncio
import struct
import time

from blackmacro_lib.modules.module_base import SpeedEditorModule
from blackmacro_lib.hid_keys import SpeedEditorKey, SpeedEditorKeyConstant


## convert dict string key to int keycode, -1 if invalid
def get_keycode_str(description: str) -> int:
    if description not in SpeedEditorKey.keycode_dict:
        return -1
    return SpeedEditorKey.keycode_dict[description]


## convert dict ID to int keycode, -1 if invalid
def get_keycode_int(index: int) -> int:
    for key, value in enumerate(SpeedEditorKey.keycode_dict.keys()):
        if key == index:
            return SpeedEditorKey.keycode_dict[value]
    return -1


def get_keyname(keycode: int) -> str:
    if keycode not in SpeedEditorKey.keyname_dict:
        return "UNKNOWN"
    return SpeedEditorKey.keyname_dict[keycode]


## Handle key presses ONLY. For key LEDs, see led.py/KeyLedModule. For Jog LEDs, see led.py/JogLedModule.
class KeyboardModule(SpeedEditorModule):
    input_id = 0x04

    def __init__(self, interface):
        super().__init__(interface)

        self.pressed_keys: list[int] = []

    # Speed editor supports 6-key rollover.
    # This takes the oldest 6 keys (the first 6) and uses it as the output
    # Why not the last? this is how the speed editor does it so...
    # The speed editor will just drop any new keys after 6 is reached
    def get_report_data(self) -> bytes:
        output_keys = []
        if len(self.pressed_keys) > 6:
            output_keys = self.pressed_keys[:6]
        else:
            output_keys = self.pressed_keys + [0x0 for _ in range(6 - len(self.pressed_keys))]

        return struct.pack('<6H', output_keys[0], output_keys[1], output_keys[2], output_keys[3], output_keys[4], output_keys[5])

    def send_report(self):
        self.k.send_encoded_report(self.input_id, self.get_report_data())

    def get_input_report(self):
        return bytearray(self.get_report_data())

    # Keypress functions do not validate keycodes!

    def clear_keys_cache(self) -> bool:
        """
        Will NOT send report automatically.
        :return:
        """
        if len(self.pressed_keys) == 0:
            return False
        self.pressed_keys = []
        return True

    def key_down(self, key: int) -> bool:
        if key not in self.pressed_keys:
            self.pressed_keys.append(key)

            self.send_report()
            return True
        else:
            return False

    def key_down_cache(self, key: int) -> bool:
        """
        Add key to pressed keys, do not send_report.
        :param key:
        :return:
        """
        if key not in self.pressed_keys:
            self.pressed_keys.append(key)
            return True
        else:
            return False

    def key_up(self, key: int) -> bool:
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)

            self.send_report()
            return True
        else:
            return False

    def key_up_cache(self, key: int) -> bool:
        """
        Remove key from pressed keys, do not send_report.
        :param key:
        :return:
        """
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
            return True
        else:
            return False

    ## returns the state the key is in now (false: key is now released)
    def toggle_key(self, key: int) -> bool:
        if key in self.pressed_keys:
            self.key_up(key)
            return False
        else:
            self.key_down(key)
            return True


    ## Emulate a key tap ("keypress") Press then release the key based on the defined duration. If the key is already down, do nothing (will not release key)
    async def tap_key(self, key: int) -> bool:
        if key in self.pressed_keys:
            return False

        self.key_down(key)

        await asyncio.sleep_ms(SpeedEditorKeyConstant.PRESS_HOLD_DURATION)

        return self.key_up(key)

    ## Emulate a key hold that will activate special functions of the key. This is really not used at all since I think all
    ## hold actions are indeterminately long and work in conjunction with the jog wheel.
    async def long_press_key(self, key: int) -> bool:
        if key in self.pressed_keys:
            return False

        self.key_down(key)

        await asyncio.sleep_ms(SpeedEditorKeyConstant.LONG_PRESS_DURATION)

        return self.key_up(key)


    ## Emulate a double-tap to activate secondary function of the key.
    async def double_press_key(self, key: int) -> bool:
        if not await self.tap_key(key):
            return False

        await asyncio.sleep_ms(SpeedEditorKeyConstant.DOUBLE_PRESS_RELEASE_DURATION)

        return await self.tap_key(key)

    ## Emulate a double-tap but don't release, for some secondary functions of the key
    async def double_hold_key(self, key:int) -> bool:
        if not await self.tap_key(key):
            return False

        time.sleep_ms(SpeedEditorKeyConstant.DOUBLE_PRESS_RELEASE_DURATION)

        return self.key_down(key)
