from hardware_defs import *
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
    K_LA1 : Key(K_LA1, (1,1), 1,  (4,0.5)),
    K_LA2 : Key(K_LA2, (1,3), 0,  (4,2.5)),
    K_LB1 : Key(K_LB1, (2,1), 5,  (3,0)),
    K_LB2 : Key(K_LB2, (2,2), 4,  (3,1)),
    K_LB3 : Key(K_LB3, (2,3), 3,  (3,2)),
    K_LB4 : Key(K_LB4, (2,4), 2,  (3,3)),
    K_LC1 : Key(K_LC1, (3,1), 9,  (2,0)),
    K_LC2 : Key(K_LC2, (3,2), 8,  (2,1)),
    K_LC3 : Key(K_LC3, (3,3), 7,  (2,2)),
    K_LC4 : Key(K_LC4, (3,4), 6,  (2,3)),
    K_LD1 : Key(K_LD1, (4,1), 13, (1,0)),
    K_LD2 : Key(K_LD2, (4,2), 12, (1,1)),
    K_LD3 : Key(K_LD3, (4,3), 11, (1,2)),
    K_LD4 : Key(K_LD4, (4,4), 10, (1,3)),
    K_LE1 : Key(K_LE1, (5,1), 15, (0,0)),
    K_LE2 : Key(K_LE2, (5,2), 14, (0,2)),
    K_RA1 : Key(K_RA1, (5,3), 20, (5,4.25)),
    K_RA2 : Key(K_RA2, (5,4), 19, (5,5.75)),
    K_RB1 : Key(K_RB1, (6,1), 18, (4,4)),
    K_RB2 : Key(K_RB2, (6,2), 17, (4,5)),
    K_RB3 : Key(K_RB3, (6,3), 16, (4,6))
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
            Pin(P_MT_CTRL1, Pin.OUT, Pin.PULL_DOWN),
            Pin(P_MT_CTRL2, Pin.OUT, Pin.PULL_DOWN),
            Pin(P_MT_CTRL3, Pin.OUT, Pin.PULL_DOWN)
        ]

        self.col_inputs = [
            Pin(P_MT_COL1, Pin.IN), # External pull-down, internal is borked :(
            Pin(P_MT_COL2, Pin.IN), # External pull-down, internal is borked :(
            Pin(P_MT_COL3, Pin.IN), # External pull-down, internal is borked :(
            Pin(P_MT_COL4, Pin.IN)  # External pull-down, internal is borked :(
        ]

        self.matrix_lookup: dict[tuple[int, int], Button] = {k.matrix: k for k in self.matrix.values()}

        self.update_callbacks = []

    def register_update_callback(self, callback):
        self.update_callbacks.append(callback)

    async def update(self):
        down_update: list[Button] = []
        up_update: list[Button] = []
        for row, signals in MT_ROW_DEMUL.items():
            # update row
            for idx, signal in enumerate(signals):
                self.row_controls[idx].value(signal)

            # read cols
            for idx, inp in enumerate(self.col_inputs):
                val = bool(inp.value())

                # prevent 6,4 mod input errors
                if (row, idx+1) in self.matrix_lookup:
                    key = self.matrix_lookup[(row, idx+1)]
                    if key.update_pressed(val):
                        if key.is_pressed():
                            down_update.append(key)
                        else:
                            up_update.append(key)

        if len(down_update) + len(up_update) > 0:
            # print("ASD")
            # notify callback
            for callback in self.update_callbacks:
                callback(self, down_update, up_update)
