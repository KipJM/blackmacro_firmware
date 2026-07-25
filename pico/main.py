import asyncio

import battery
import key
import led
import reg_encoder
from module import SysModule


### THIS IS NOW NAMED MAIN!!!!!
### DO NOT ADD USB CONTROL CODE HERE OR I WILL KILL YOU!!

async def main():
    modules: list[SysModule] = []

    # === MODULE INIT ===

    key_controller = key.KeyMatrix()
    modules.append(key_controller)

    brightness_control = led.BrightnessControlFX(0.1)

    led_controller = led.LEDController(
        layers=[
            led.RainbowGenerator(),
            led.KeyImmediateVisualizationFX((99999,99999,99999)), # yes you can have hdr lol its python datatypes are a myth
            brightness_control
        ]
    )
    modules.append(led_controller)

    charger = battery.BatteryCharger()
    modules.append(charger)

    # ===

    def change_brightness(value: int):
        print(":O")
        brightness_control.brightness = max(0.0, min(1.0, float(value) / 200.0))

    reg_encoder.DEF_ENCODERS["RENC1"].add_change_callback(change_brightness)


    for module in modules:
        await module.loop

asyncio.run(main())