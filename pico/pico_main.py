import asyncio

from machine import I2C, USBDevice
import usb.device

import modules.battery as battery
import modules.key as key
import modules.led as led
import modules.dial_encoder as dial_encoder

import reg_encoder
from hardware_defs import *
from hid_modules import speed_editor
from module import SysModule


### ADD AN FAILSAFE RESET OR I WILL KILL YOU!! - past me

async def main():
    modules: list[SysModule] = []

    # === MODULE INIT ===

    key_controller = key.KeyMatrix()
    modules.append(key_controller)

    brightness_control = led.BrightnessControlFX(0.1)

    led_controller = led.LEDController(
        layers=[
            led.RainbowGenerator(),
        ],
        sys_layers=[
            # led.KeyImmediateVisualizationFX((99999, 99999, 99999)), # yes you can have hdr lol its python datatypes are a myth
            led.KeyFadeVisualizationFX((255, 255, 255), 1),
            brightness_control
        ]
    )
    modules.append(led_controller)

    bat_charger = battery.BatteryCharger()
    modules.append(bat_charger)

    i2c = I2C(ID_I2C, scl=P_I2C_SCL, sda=P_I2C_SDA, freq=I2C_FREQ, timeout=I2C_TIMEOUT)
    bat_monitor = battery.BatteryMonitor(i2c)
    modules.append(bat_monitor)

    mag_enc = dial_encoder.DialEncoder()
    modules.append(mag_enc)

    # ===

    def change_brightness(value: int):
        print(":O")
        brightness_control.change_brightness_gamma(max(0.0, min(3.0, float(value) / 200.0)))

    reg_encoder.DEF_ENCODERS["RENC1"].register_rot_callback(change_brightness)

    # ==============================================================

    # -- USB Failsafe Init --
    def usb_failsafe(_, _2):
        usb.device.get().init(builtin_driver=USBDevice.BUILTIN_CDC)
        raise KeyboardInterrupt

    reg_encoder.DEF_ENCODERS["RENC2"].register_update_callback(usb_failsafe)

    # Second boot-up failsafe incase the program crashes
    await key_controller.update()
    if reg_encoder.DEF_ENCODERS["RENC2"].is_pressed():
        usb_failsafe(None, None)
        print(":O")
        return

    # # # === HID EMULATION INIT (Non-davinci) ===
    # hid_modules: list[HIDModule] = [
    #     KeyboardHID(key_controller),
    # ]
    # # Init usb, btw i hate python syntax so much what is this * shit man
    # usb.device.get().init(*[mod.get_interface() for mod in hid_modules], builtin_driver=True)

    # # for hid_mod in hid_modules: # this hangs pico, removed
    # #     await hid_mod.init_hid()

    # === HID EMULATION INIT (DAVINCI) ===
    editor = speed_editor.SpeedEditorHID()

    mag_enc.register_update_handler(editor.dial_update)
    bat_monitor.register_update_handler(editor.battery_update)
    bat_charger.register_update_handler(editor.charger_update)
    key_controller.register_update_callback(editor.key_update)

    led_controller.layers.append(speed_editor.SpeedEditorLEDFX(editor.led_lookup, (125, 0, 0)))

    # ==============================================================

    # Prevent main loop from exiting
    for module in modules:
        await module.loop


asyncio.run(main())