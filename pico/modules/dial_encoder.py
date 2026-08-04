import time
from machine import SPI, Pin

from hardware_defs import *
from module import SysModule


class DialEncoder(SysModule):
    def __init__(self, delta:float = 0.001):
        super().__init__(delta)
        self.sck = Pin(P_MAG_CLK, Pin.OUT)
        self.miso = Pin(P_MAG_DO, Pin.IN)
        self.ssi = SPI(ID_MAG_SSI,
                       polarity=MAG_SSI_CPOL, phase=MAG_SSI_CPHA,
                       bits=8, firstbit=SPI.MSB,
                       sck=self.sck, miso=self.miso)

        self.cs = Pin(P_MAG_CSN, Pin.OUT, value=1)

    def read(self):
        self.cs.value(0)
        # 24 bits, first 14 is angle
        raw = self.ssi.read(3, 0x0)
        self.cs.value(1)

        print(raw)

        angle_raw = int.from_bytes(raw, "big") & MSK_MAG_ANGL >> SHFT_MAG_ANGL
        print(angle_raw / 16384 * 360)

    async def update(self):
        self.read()