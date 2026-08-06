from micropython import const
import time
import binascii

import usb.device
from blackmacro_lib.modules.jog import JogModule
from blackmacro_lib.modules.keyboard import KeyboardModule
from blackmacro_lib.modules.led import KeyLedModule, JogLedModule
from blackmacro_lib.modules.misc import InitModule, SerialNumberModule
from blackmacro_lib.modules.auth import AuthenticationModule
from blackmacro_lib.modules.battery import BatteryModule
from blackmacro_lib.settings import SpeedEditorSettings
from usb.device.hid import HIDInterface  # WARN: USING CUSTOM HID LIBRARY
from usb.device.hid import REPORT_TYPE_FEATURE, REPORT_TYPE_INPUT, REPORT_TYPE_OUTPUT
from blackmacro_lib.hid_descr import KEYPAD_REPORT_DESC



class SpeedEditorInterface(HIDInterface):
    INTERFACE_PROTOCOL_NONBOOT = const(0x00)
    i_str_manuf = const(0x1edb)  # BMD
    i_str_product = const(0xda0e)  # Speed Editor

    def __init__(self):
        super().__init__(
            KEYPAD_REPORT_DESC,
            set_report_buf=bytearray(64),  # max possible report size
            protocol=self.INTERFACE_PROTOCOL_NONBOOT,
            interface_str="DaVinci Resolve Speed Editor",
        )

        # report handlers
        # dictionary that map report ids to the respective modules. When a module is initialized, they add themselves to
        # these dictionaries.

        self.get_input_report_handlers = {}
        self.get_feature_report_handlers = {}

        self.set_output_report_handlers = {}
        self.set_feature_report_handlers = {}

        # initialize modules

        # some special modules that are commonly used have direct references
        self.auth = AuthenticationModule(self)
        self.battery = BatteryModule(self)
        self.keyboard = KeyboardModule(self)
        self.led = KeyLedModule(self)
        self.jog_led = JogLedModule(self)
        self.jog = JogModule(self)

        # others get instantiated here (+ reference to the special ones as well)
        self.modules = [InitModule(self), SerialNumberModule(self),
                        self.auth, self.battery, self.keyboard, self.led, self.jog_led, self.jog]


    @staticmethod
    def encode_report(report_id: int, data: bytes) -> bytearray:
        return bytearray([report_id]) + data

    def send_encoded_report(self, report_id: int, data: bytes):
        if self.debug:
            print(f"Sending report w/ id {report_id}")
        send_status = self.send_report(self.encode_report(report_id, data))
        if not send_status:
            print(f"Send report id {report_id} FAILED")

    # GET REPORT

    def get_report(self, report_id, report_type):
        if self.debug:
            print(f"GET_REPORT: TYPE:{report_type}, ID:{report_id}")

        if report_type == REPORT_TYPE_FEATURE:
            return self.get_feature_report(report_id)

        elif report_type == REPORT_TYPE_INPUT:
            return self.get_input_report(report_id)

        elif report_type == REPORT_TYPE_OUTPUT:
            print(f"IMPOSSIBLE GET OUTPUT REPORT: {report_type} (id {report_id}), OUTSIDE OF USB SPEC")
            return False

        else:
            print(f"UNKNOWN GET REPORT TYPE: {report_type} (id {report_id}), OUTSIDE OF USB SPEC")
            return False

    def get_feature_report(self, report_id):
        # modules
        if report_id in self.get_feature_report_handlers:
            return self.encode_report(report_id, self.get_feature_report_handlers[report_id]())

        # Unsupported
        print(f"UNKNOWN GET FEATURE REPORT ID: {report_id}")
        return False

    def get_input_report(self, report_id):
        # Delegate processing to module if possible
        if report_id in self.get_input_report_handlers:
            return self.encode_report(report_id, self.get_input_report_handlers[report_id]())

        # Unsupported
        print(f"UNKNOWN GET INPUT REPORT ID: {report_id}")
        return False

    # SET REPORT

    def on_set_report(self, report_data, report_id, report_type) -> bool:
        if self.debug:
            print(f"SET_REPORT: TYPE:{report_type}, ID:{report_id}, DAT:{binascii.hexlify(report_data)}")

        if report_type == REPORT_TYPE_FEATURE:
            return self.set_feature_report(report_id, report_data)

        elif report_type == REPORT_TYPE_INPUT:
            print(f"IMPOSSIBLE SET INPUT REPORT: {report_type} (id {report_id}), OUTSIDE OF USB SPEC")
            return False

        elif report_type == REPORT_TYPE_OUTPUT:
            return self.set_output_report(report_id, report_data)

        else:
            print(f"UNKNOWN SET REPORT TYPE: {report_type} (id {report_id}), OUTSIDE OF USB SPEC")
            return False

    def set_feature_report(self, report_id, report_data) -> bool:
        if report_id in self.set_feature_report_handlers:
            return self.set_feature_report_handlers[report_id](report_data)

        # unsupported
        print(f"UNSUPPORTED SET FEATURE REPORT ID {report_id}")
        return False

    def set_output_report(self, report_id, report_data) -> bool:
        if report_id in self.set_output_report_handlers:
            return self.set_output_report_handlers[report_id](report_data)

        # unsupported
        print(f"UNSUPPORTED SET OUTPUT REPORT ID {report_id}")
        return False



def init_speed_editor() -> SpeedEditorInterface:

    str_product = f'DaVinci Resolve Speed Editor'
    str_manuf = f'Blackmagic design'

    global k
    k = SpeedEditorInterface()
    k.debug = False

    # Class 03h: HID
    #
    usb.device.get().init(k, builtin_driver=True, manufacturer_str=str_manuf, product_str=str_product,
                          id_vendor=k.i_str_manuf, id_product=k.i_str_product, serial_str=SpeedEditorSettings.STR_SERIAL)

    print("Waiting for USB")
    while not k.is_open():
        time.sleep_ms(100)

    return k