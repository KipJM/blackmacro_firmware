from blackmacro_lib.blackmacro import SpeedEditorInterface, init_speed_editor
from blackmacro_lib.hid_keys import SpeedEditorKey
from button import Button
from hardware_defs import *
from blackmacro_lib.hid_keys import SpeedEditorKey as SKey
from hid_modules.speed_editor_keys import SpeedEditorKeyTranslation
from modules.battery import BatteryMonitor, BatteryCharger
from modules.dial_encoder import DialEncoder
from modules.key import KeyMatrix, DEF_KEYS, Key
from modules.led import LEDLayer


# WARN: THIS IS VERY MUCH DIFFERENT THAN OTHER HID DEVICES.
# SPEED EDITOR MODE CAN ONLY BE USED ON ITS OWN
class SpeedEditorHID:
    def __init__(self, battery_soc: int):
        self.interface = init_speed_editor()
        self.interface.battery.battery_level = battery_soc
        self.keycode_translation = SpeedEditorKeyTranslation({
                K_LA1: SKey.IN,
                K_LA2: SKey.OUT,
                K_LB1: SKey.ESC,
                K_LB2: SKey.AUDIO_LEVEL,
                K_LB3: SKey.SNAP,
                K_LB4: SKey.CLOSE_UP,
                K_LC1: SKey.ROLL,
                K_LC2: SKey.SPLIT,
                K_LC3: SKey.RIPL_DEL,
                # K_LC4: SKey., # TODO: PURE DELETE KEY SENT BY REGULAR KEYCODE
                K_LD1: SKey.SMART_INSRT,
                K_LD2: SKey.APPND,
                K_LD3: SKey.PLACE_ON_TOP,
                K_LD4: SKey.RIPL_OWR,
                K_LE1: SKey.FULL_VIEW,
                K_LE2: SKey.STOP_PLAY,
                K_RA1: SKey.SOURCE,
                K_RA2: SKey.TIMELINE,
                K_RB1: SKey.SHTL,
                K_RB2: SKey.JOG,
                K_RB3: SKey.SCRL,
            })

    def dial_update(self, dial: DialEncoder, delta: float):
        self.interface.jog.set_angle_degrees(dial.angle_adjusted, delta)

    def battery_update(self, battery: BatteryMonitor):
        self.interface.battery.change_battery_level(battery.soc)

    def charger_update(self, charger: BatteryCharger):
        self.interface.battery.change_charge_state(charger.is_charging)

    def key_update(self, matrix: KeyMatrix, down_update: list[Button], up_update: list[Button]):
        for key in down_update:
            code = self.keycode_translation.get_skey(key)
            if code != -1:
                self.interface.keyboard.key_down_cache(code)

        for key in up_update:
            code = self.keycode_translation.get_skey(key)
            if code != -1:
                self.interface.keyboard.key_up_cache(code)

        if len(down_update) == 0: # possibility of nothing being pressed
            pressed = False
            for key in DEF_KEYS.values():
                if key.is_pressed():
                    pressed = True

            if pressed == False:
                self.interface.keyboard.clear_keys_cache() # prevent desync

        self.interface.keyboard.send_report()

    def led_lookup(self, key: Button) -> bool:
        return self.keycode_translation.get_led_stat(key, self.interface.led, self.interface.jog_led)

class SpeedEditorLEDFX(LEDLayer):
    def __init__(self, led_lookup, lit_color: tuple[int, int, int] = (125, 0, 0)):
        super().__init__()
        self.led_lookup = led_lookup
        self.lit_color = lit_color

    def process(self, data: list[tuple[int, int, int]], delta: float) -> list[tuple[int, int, int]]:
        for i in range(len(data)):
            key = self.key_lookup(i)
            if self.led_lookup(key):
                data[i] = self.lit_color

        return data
