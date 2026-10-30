import struct

import math
from micropython import const

from button import Button
from hardware_defs import HID_TIMEOUT
from hid_module import HIDModule
from hid_modules.regular.hid_descriptors import gamepad_descr
from modules.dial_encoder import DialEncoder
from modules.key import KeyMatrix
from usb.device.hid import HIDInterface

INTERFACE_PROTOCOL_NONBOOT = const(0x00)

# Haptics not implemented.
class GamepadInterface(HIDInterface):
    def __init__(self, timeout):
        super().__init__(
            gamepad_descr.GAMEPAD_REPORT_DESC,
            protocol=INTERFACE_PROTOCOL_NONBOOT,
            interface_str="MicroPython Gamepad"
        )

        self.timeout = timeout
        self.button_state = 0 # bitmask
        self.x: int = 0
        self.y: int = 0
        self.z: int = 0
        self.rz: int = 0
        self.reports = [
            bytearray(6),
            bytearray(6),
        ]

    def press_buttons(self, buttons: list[int]):
        if len(buttons) == 0:
            return
        self.update_buttons(buttons, [])


    def release_buttons(self, buttons: list[int]):
        if len(buttons) == 0:
            return
        self.update_buttons([], buttons)


    def update_buttons(self, down_buttons: list[int], up_buttons: list[int]):
        if len(up_buttons) == 0 and len(down_buttons) == 0:
            return

        for button in down_buttons:
            self.button_state |= 1 << button

        for button in up_buttons:
            self.button_state &= ~(1 << button)

        # print(bin(self.button_state))
        self.send_update()

    def set_left_stick(self, x: int, y: int, z:int = 0, rz: int = 0):
        self.x = x
        self.y = y
        self.z = z
        self.rz = rz
        self.send_update()

    def send_update(self):
        r, s = self.reports
        # [0]: Button[0-7]
        # [1]: Button[8-15]
        # [2]: Button[16-20], #, #, #
        # [3]: #
        # [4]: X
        # [5]: Y
        # [6]: Rx
        # [7]: Ry
        struct.pack_into("<Hbbbb", r, 0,
                         self.button_state,
                         self.x, self.y,
                         self.z, self.rz)
        # print(r)

        if self.send_report(r, self.timeout):
            self.reports[0] = s
            self.reports[1] = r
            return True
        return False


class GamepadHID(HIDModule):
    KEY_TRANSLATION: dict[str, int] = {
        "LA1": 0,
        "LA2": 1,
        "LB1": 2,
        "LB2": 3,
        "LB3": 4,
        "LB4": 5,
        "LC1": 6,
        "LC2": 7,
        "LC3": 8,
        "LC4": 9,
        "LD1": 10,
        "LD2": 11,
        "LD3": 12,
        "LD4": 13,
        "LE1": 14,
        "LE2": 15
    }

    def __init__(self, matrix: KeyMatrix, dial: DialEncoder):
        super().__init__()
        self.interface: GamepadInterface = GamepadInterface(HID_TIMEOUT)
        self.matrix = matrix
        self.dial = dial

        self.matrix.register_update_callback(self.key_update_handler)
        self.dial.register_update_handler(self.dial_update_handler)

    def get_interface(self) -> HIDInterface:
        return self.interface

    def key_update_handler(self, matrix: KeyMatrix, down_keys: list[Button], up_keys: list[Button]):
        down_buttons: list[int] = []
        up_buttons: list[int] = []

        for key in down_keys:
            if key.name in self.KEY_TRANSLATION:
                down_buttons.append(self.KEY_TRANSLATION[key.name])

        for key in up_keys:
            if key.name in self.KEY_TRANSLATION:
                up_buttons.append(self.KEY_TRANSLATION[key.name])

        # print(down_buttons, up_buttons)

        self.interface.update_buttons(down_buttons, up_buttons)

    def angle_to_axis(self, angle) -> tuple[int, int]:
        ang: float = math.radians(angle - 90.0)

        x = int(gamepad_descr.GAMEPAD_AXIS_MAX * math.cos(ang))
        y = int(gamepad_descr.GAMEPAD_AXIS_MAX * math.sin(ang))

        x = max(-gamepad_descr.GAMEPAD_AXIS_MAX, min(x, gamepad_descr.GAMEPAD_AXIS_MAX))
        y = max(-gamepad_descr.GAMEPAD_AXIS_MAX, min(y, gamepad_descr.GAMEPAD_AXIS_MAX))

        return x,y


    def dial_update_handler(self, dial: DialEncoder, delta: float):
        if delta != 0:
            self.interface.set_left_stick(*self.angle_to_axis(dial.angle_adjusted))
