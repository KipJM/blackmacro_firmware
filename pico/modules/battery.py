import asyncio
import math
from datetime import timedelta

from machine import Pin, I2C

from BQ27427 import BQ27427
from BQ27427h import *

from module import SysModule
from hardware_defs import *

# TP4056 charge pin monitor
class BatteryCharger(SysModule):
    def __init__(self, delta: float = 1.0):
        super().__init__(delta)
        self.charge_signal = Pin(P_CHRG, Pin.IN, Pin.PULL_UP)
        self.vbus_detect = Pin(P_VBUS, Pin.IN)

        self.debug_led = Pin("LED", Pin.OUT) # TODO: remove later

        self.is_usb_connected: bool = False
        self.is_charging: bool = False

    async def update(self):
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
    def __init__(self, i2c: I2C, delta: float = 5.0):
        super().__init__(delta)
        self.battery = BQ27427(i2c, seal_flag=True)

        self.soc: int = 0 # out of 100
        self.soh: int = 0 # out of 100
        self.current: int = 0 # mA
        self.power: int = 0 # mW

        self.estimated_ttl: timedelta = timedelta(hours=0); " Estimated time to empty based on avg. current, in hours"

        asyncio.run(self.battery_init())


    async def battery_init(self):
        if not self.battery.begin():
            raise IOError("Error: Unable to communicate with BQ27427")
        # Gauge config. This would probably be stored in its ROM? If the monitor is sealed,
        # we assume the data has already been written to prevent wearing out the rom
        if not self.battery.is_sealed():
            await self.battery.enter_config(True)
            await self.battery.set_capacity(BATTERY_CAPACITY)
            await self.battery.set_design_energy(BATTERY_ENERGY)
            if await self.battery.get_current_polarity():  # reverse polarity
                await self.battery.change_current_polarity()
            await self.battery.set_chem_id(ChemistryProfile.CHEM_B)  # change to your setup
            await self.battery.set_terminate_voltage(BATTERY_TERMINATE_VOLTAGE)  # soc is considered 0% at 3000mV
            # Taper Rate (Unit: 0.1h, basically 10*C) = Design Capacity / (0.1 * Taper Current)
            await self.battery.set_taper_rate(
                int(10 * BATTERY_CAPACITY / BATTERY_TAPER_CURRENT))  # soc is considered 100% at this point
            await self.battery.exit_config(True)


    async def update(self):
        self.soc = self.battery.get_soc(SocMeasure.FILTERED)
        self.soh = self.battery.get_soh(SohMeasure.PERCENT)
        self.current = self.battery.get_current(CurrentMeasure.AVG)
        self.power = self.battery.get_avg_power()

        if self.current <= 0:
            self.estimated_ttl = timedelta(hours = float(await self.battery.get_capacity(CapacityMeasure.REMAIN)) / -self.current)
        else:
            # When charging, change to very rough estimate on time to full
            self.estimated_ttl = timedelta(hours = float(await self.battery.get_capacity(CapacityMeasure.FULL) -
                                                         await self.battery.get_capacity(CapacityMeasure.REMAIN)) / self.current)

        print(f"BAT: SOC: {self.soc}%, Current: {self.current/1000}A, Power: {self.power/1000}W, Estimated TTL: {self.estimated_ttl}")