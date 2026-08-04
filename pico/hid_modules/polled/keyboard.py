from button import Button
from hardware_defs import HID_TIMEOUT
from hid_module import HIDModule
from modules.key import KeyMatrix, DEF_KEYS
from usb.device.hid import HIDInterface
from usb.device.keyboard import KeyboardInterface, KeyCode


class KeyboardHID(HIDModule):
    KEY_TRANSLATION: dict[str, int] = {
        "LA1": KeyCode.D,
        "LA2": KeyCode.F,
        "LB1": KeyCode.D,
        "LB2": KeyCode.F,
        "LB3": KeyCode.J,
        "LB4": KeyCode.H,
        "LC1": KeyCode.N5,
        "LC2": KeyCode.N6,
        "LC3": KeyCode.N7,
        "LC4": KeyCode.N8,
        "LD1": KeyCode.N9,
        "LD2": KeyCode.N0,
        "LD3": KeyCode.COMMA,
        "LD4": KeyCode.DOT,
        "LE1": KeyCode.ENTER,
        "LE2": KeyCode.SPACE,
        "RA1": KeyCode.H,
        "RA2": KeyCode.J,
        "RB1": KeyCode.H,
        "RB2": KeyCode.B,
        "RB3": KeyCode.J,
    }

    def __init__(self, matrix: KeyMatrix):
        super().__init__()
        self.interface: KeyboardInterface = KeyboardInterface()
        self.matrix = matrix

        self.matrix.register_update_callback(self.update_handler)

    def get_interface(self) -> HIDInterface:
        return self.interface

    def update_handler(self, matrix: KeyMatrix, down_keys: list[Button], up_keys: list[Button]):
        # print("ASHDSAH")
        keycode_list: list[int] = []
        for but, keycode in self.KEY_TRANSLATION.items():
            if but in DEF_KEYS:
                if DEF_KEYS[but].is_pressed():
                    keycode_list.append(keycode)

        print(keycode_list)
        self.interface.send_keys(keycode_list, HID_TIMEOUT)