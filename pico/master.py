import asyncio

import key
import led

async def main():
    led_controller = led.LEDController(
        layers=[
            led.RainbowGenerator(),
            led.BrightnessControl(0.5)
        ]
    )

    key_controller = key.KeyMatrix()

    await led_controller.loop
    await key_controller.loop

asyncio.run(main())