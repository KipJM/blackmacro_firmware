# Manages only key LEDs.
# For Jog LEDS, see class below.
import struct

from collections import OrderedDict

from blackmacro_lib.modules.module_base import SpeedEditorModule
from blackmacro_lib.hid_keys import SpeedEditorLed, SpeedEditorJogLed


class KeyLedModule(SpeedEditorModule):
    output_id = 0x02

    def __init__(self, interface):
        super().__init__(interface)

        self.led_status: OrderedDict[str, bool] = OrderedDict()
        for name in SpeedEditorLed.name_dict.items():
            self.led_status[name] = False

    def get_active_leds(self) -> list[str]:
        output = []
        for name in self.led_status.keys():
            if self.led_status[name]:
                output.append(name)
        return output


    def set_output_report(self, report_data:bytes) -> bool:
        _, led_data = struct.unpack("<BI", report_data)

        for key in SpeedEditorLed.name_dict:
            self.led_status[SpeedEditorLed.name_dict[key]] = bool(led_data & key)

        return True


# For Shuttle, Jog, and Scroll.
# Since there are only three keys, they are managed through dedicated variables instead of a list.
class JogLedModule(SpeedEditorModule):
    output_id = 0x04

    def __init__(self, interface):
        super().__init__(interface)

        self.shuttle_lit: bool = False
        self.jog_lit: bool = False
        self.scroll_lit: bool = False

    def set_output_report(self, report_data:bytes) -> bool:
        _, led_data = struct.unpack("<BB", report_data)

        self.shuttle_lit = bool(led_data & SpeedEditorJogLed.SHTL)
        self.jog_lit     = bool(led_data & SpeedEditorJogLed.JOG)
        self.scroll_lit  = bool(led_data & SpeedEditorJogLed.SCRL)

        # Apparantly there's a short period when switching modes that multiple LEDs would be lit, :o
        # if int(self.shuttle_lit) + int(self.jog_lit) + int(self.scroll_lit) > 1:
        #     print("Received jog led state with more than one lit. This should be impossible, but I could be wrong...")

        return True