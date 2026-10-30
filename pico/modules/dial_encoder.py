import time
from machine import SPI, Pin

from hardware_defs import *
from module import SysModule


class DialEncoder(SysModule):
    def __init__(self, delta: int = 1):
        super().__init__(delta)
        self.sck = Pin(P_MAG_CLK, Pin.OUT)
        self.miso = Pin(P_MAG_DO, Pin.IN)
        self.ssi = SPI(ID_MAG_SSI, baudrate=MAG_SSI_FREQ,
                       polarity=MAG_SSI_CPOL, phase=MAG_SSI_CPHA,
                       bits=8, firstbit=SPI.MSB,
                       sck=self.sck, miso=self.miso)

        self.cs = Pin(P_MAG_CSN, Pin.OUT, value=1)

        self.angle_raw: float = 0 # degrees, counterclockwise, start at magnet zero, 0-360
        self.angle_adjusted: float = 0 # degrees, start at ZEROPOINT, goes clockwise, 0-360
        self.angle_lifetime: float = 0 # degrees, start at ZEROPOINT, -inf~inf, absolute angle since poweron

        self.pressed: bool = False # unused, data supported by mag sensor but impossible to trigger bcs of mechanical design
        self.field_status: int = 0 # 1 = too strong, 2 = too weak, 0 = okay. too lazy to create an enum for this
        self.tracking_lost: bool = False # technically "too fast" in datasheet???

        # self.data_valid: bool = True # False if checksum fails for this frame
        self.update_handlers = []

    def register_update_handler(self, update_handler):
        self.update_handlers.append(update_handler)

    def read(self):
        self.cs.value(0)
        # 24 bits, first 14 is angle
        # for some reason everything is shifted right by one bit, so im reading four bytes and compensating
        extra_raw = self.ssi.read(4, 0x0)
        raw = (int.from_bytes(extra_raw, "big") >> 7) & 0xFFFFFF # first broken bit is dropped

        self.cs.value(1)

        # print()
        # print(f"{raw:024b}")
        # print("AAAAAAAAAAAAAAFFPSCCCCCC")

        # Angle

        angle_raw_data = (raw & MSK_MAG_ANGL) >> SHFT_MAG_ANGL

        self.angle_raw = angle_raw_data / 16384 * 360

        last_angle_adjusted = self.angle_adjusted
        self.angle_adjusted = 360 - (self.angle_raw - MAG_ANGLE_ZEROPOINT) % 360 # python modulo works with negatives????

        delta = self.angle_adjusted - last_angle_adjusted

        # wrapping detection, couldn't bother writing this by hand
        if delta > 180:
            delta -= 360
        elif delta < -180:
            delta += 360

        self.angle_lifetime += delta
        # print(self.angle_raw)
        # print(self.angle_adjusted)
        # print(self.angle_lifetime)
        # print() # DEBUG


        if delta != 0:
            for update_handler in self.update_handlers:
                update_handler(self, delta)

        # Mg
        self.field_status = (raw & MSK_MAG_FIELD) >> SHFT_MAG_FIELD
        self.pressed = bool((raw & MSK_MAG_PUSH) >> SHFT_MAG_PUSH)
        self.tracking_lost = bool((raw & MSK_MAG_SPEED) >> SHFT_MAG_SPEED)

        # TODO: CRC verification


    async def update(self):
        self.read()