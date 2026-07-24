from machine import Pin

from module import SysModule
import hardware_defs

# TP4056 charge pin monitor
class BatteryCharger(SysModule):
    def __init__(self, delta: float = 1.0):
        super().__init__(delta)
        self.charge_signal = Pin(hardware_defs.P_CHRG, Pin.IN, Pin.PULL_UP)
        self.vbus_detect = Pin(hardware_defs.P_VBUS, Pin.IN)

        self.debug_led = Pin("LED", Pin.OUT) # TODO: remove later

        self.is_usb_connected: bool = False
        self.is_charging: bool = False

    def update(self):
        self.is_usb_connected = bool(self.vbus_detect.value())
        self.is_charging = not bool(self.charge_signal.value())
        # print(self.is_usb_connected, self.is_charging)

        self.debug_led.value(self.is_charging) # TODO: remove later

    def get_is_usb_connected(self):
        return self.is_usb_connected

    def get_is_charging(self):
        return self.is_charging

# TI battery fuel gauge controller
class BatteryMonitor(SysModule):
    def __init__(self, delta: float = 5):
        super().__init__(delta)

    def update(self):
        # TODO
        pass