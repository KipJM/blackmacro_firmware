from blackmacro_lib.modules.keyboard import get_keyname
from blackmacro_lib.modules.led import KeyLedModule, JogLedModule
from button import Button
from hardware_defs import *
from blackmacro_lib.hid_keys import SpeedEditorKey as SKey

class SpeedEditorKeyTranslation:
    def __init__(self, key_translation_dict: dict[str, int] = None):
        # MODIFY THIS
        if key_translation_dict is None:
            key_translation_dict: dict[str, int] = {
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
            }
        self.key_translation = key_translation_dict


    def get_key_translation(self) -> dict[str, int]:
        return self.key_translation

    def get_skey(self, button: Button) -> int:
        """
        :return: -1 if not found
        """
        if button.name in self.get_key_translation():
            return self.get_key_translation()[button.name]
        else:
            return -1

    def get_skey_name(self, button: Button) -> str:
        """
        :param button:
        :return: \"\" if not found
        """
        if self.get_skey(button) != -1:
            return get_keyname(self.get_skey(button))
        else:
            return ""

    def get_led_stat(self, key: Button, key_led: KeyLedModule, jog_led: JogLedModule) -> bool:
        keycode = self.get_skey(key)

        if keycode == -1:
            return False

        if keycode == SKey.JOG:
            return jog_led.jog_lit
        elif keycode == SKey.SHTL:
            return jog_led.shuttle_lit
        elif keycode == SKey.SCRL:
            return jog_led.scroll_lit
        else:
            return self.get_skey_name(key) in key_led.get_active_leds()
