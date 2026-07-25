import hardware_defs
from button import Button
from module import SysModule
from machine import Pin

from reg_encoder import DEF_ENCODERS

class Key(Button):
    def __init__(self, name: str, matrix: tuple[int, int], led: int, position: tuple[float, float]):
        super().__init__(name, matrix)
        self.led: int = led
        self.position: tuple[float, float] = position


### KEY DEFS
# Keyname: matrix(row 1-index, column 1-index), led 0-index, physical position(y,x, float, origin at bottom left, gaps considered)

# MOD key is not included. if you wanna deal with that write your own firmware
DEF_KEYS: dict[str, Key] = {
    "LA1" : Key("LA1", (1,1), 1,  (4,0.5)),
    "LA2" : Key("LA2", (1,3), 0,  (4,2.5)),
    "LB1" : Key("LB1", (2,1), 5,  (3,0)),
    "LB2" : Key("LB2", (2,2), 4,  (3,1)),
    "LB3" : Key("LB3", (2,3), 3,  (3,2)),
    "LB4" : Key("LB4", (2,4), 2,  (3,3)),
    "LC1" : Key("LC1", (3,1), 9,  (2,0)),
    "LC2" : Key("LC2", (3,2), 8,  (2,1)),
    "LC3" : Key("LC3", (3,3), 7,  (2,2)),
    "LC4" : Key("LC4", (3,4), 6,  (2,3)),
    "LD1" : Key("LD1", (4,1), 13, (1,0)),
    "LD2" : Key("LD2", (4,2), 12, (1,1)),
    "LD3" : Key("LD3", (4,3), 11, (1,2)),
    "LD4" : Key("LD4", (4,4), 10, (1,3)),
    "LE1" : Key("LE1", (5,1), 15, (0,0)),
    "LE2" : Key("LE2", (5,2), 14, (0,2)),
    "RA1" : Key("RA1", (5,3), 20, (5,4.25)),
    "RA2" : Key("RA2", (5,4), 19, (5,5.75)),
    "RB1" : Key("RB1", (6,1), 18, (4,4)),
    "RB2" : Key("RB2", (6,2), 17, (4,5)),
    "RB3" : Key("RB3", (6,3), 16, (4,6))
}

# implement mod 1 and 2 yourself
# row (not demul output): demul input
MT_ROW_DEMUL: dict[int, tuple[bool, bool, bool]] = {
    1 : ( True  , False , True  ),
    2 : ( False , False , True  ),
    3 : ( True  , True  , False ),
    4 : ( False , True  , False ),
    5 : ( True  , False , False ),
    6 : ( False , False , False )
}


class KeyMatrix(SysModule):
    def __init__(self, delta: float = 0.001):
        super().__init__(delta)
        self.matrix: dict[str, Button] = DEF_KEYS.copy()
        self.matrix.update(DEF_ENCODERS) # add encoders, this is bad but should work

        self.row_controls = [
            Pin(hardware_defs.P_MT_CTRL1, Pin.OUT, Pin.PULL_DOWN),
            Pin(hardware_defs.P_MT_CTRL2, Pin.OUT, Pin.PULL_DOWN),
            Pin(hardware_defs.P_MT_CTRL3, Pin.OUT, Pin.PULL_DOWN)
        ]

        self.col_inputs = [
            Pin(hardware_defs.P_MT_COL1, Pin.IN), # External pull-down, internal is borked :(
            Pin(hardware_defs.P_MT_COL2, Pin.IN), # External pull-down, internal is borked :(
            Pin(hardware_defs.P_MT_COL3, Pin.IN), # External pull-down, internal is borked :(
            Pin(hardware_defs.P_MT_COL4, Pin.IN)  # External pull-down, internal is borked :(
        ]

        self.matrix_lookup: dict[tuple[int, int], Button] = {k.matrix: k for k in self.matrix.values()}


    async def update(self):
        for row, signals in MT_ROW_DEMUL.items():
            # update row
            for idx, signal in enumerate(signals):
                self.row_controls[idx].value(signal)

            # read cols
            for idx, inp in enumerate(self.col_inputs):
                val = bool(inp.value())

                # prevent 6,4 mod input errors
                if (row, idx+1) in self.matrix_lookup:
                    self.matrix_lookup[(row, idx+1)].update_pressed(val)

