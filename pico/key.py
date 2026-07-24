import hardware_defs
from module import LoopModule
from machine import Pin

class Key:
    def __init__(self, matrix: tuple[int, int], led: int, position: tuple[float, float]):
        self.matrix: tuple[int, int] = matrix
        self.led: int = led
        self.position: tuple[float, float] = position

### KEY DEFS
# Keyname: matrix(row 1-index, column 1-index), led 0-index, physical position(y,x, float, origin at bottom left, gaps considered)

# MOD key is not included. if you wanna deal with that write your own firmware
DEF_KEYS: dict[str, Key] = {
    "LA1" : Key((1,1), 1,  (4,0.5)),
    "LA2" : Key((1,3), 0,  (4,2.5)),
    "LB1" : Key((2,1), 5,  (3,0)),
    "LB2" : Key((2,2), 4,  (3,1)),
    "LB3" : Key((2,3), 3,  (3,2)),
    "LB4" : Key((2,4), 2,  (3,3)),
    "LC1" : Key((3,1), 9,  (2,0)),
    "LC2" : Key((3,2), 8,  (2,1)),
    "LC3" : Key((3,3), 7,  (2,2)),
    "LC4" : Key((3,4), 6,  (2,3)),
    "LD1" : Key((4,1), 13, (1,0)),
    "LD2" : Key((4,2), 12, (1,1)),
    "LD3" : Key((4,3), 11, (1,2)),
    "LD4" : Key((4,4), 10, (1,3)),
    "LE1" : Key((5,1), 15, (0,0)),
    "LE2" : Key((5,2), 14, (0,2)),
    "RA1" : Key((5,3), 20, (5,4.25)),
    "RA2" : Key((5,4), 19, (5,5.75)),
    "RB1" : Key((6,1), 18, (4,4)),
    "RB2" : Key((6,2), 17, (4,5)),
    "RB3" : Key((6,3), 16, (4,6))
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

# TODO: Key controller
class KeyMatrix(LoopModule):
    def __init__(self, delta: float = 0.001):
        super().__init__(delta)
        self.matrix = DEF_KEYS

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

    def update(self):
        for row, signals in MT_ROW_DEMUL.items():
            for idx, signal in enumerate(signals):
                self.row_controls[idx].value(signal)

            col_vals = [col.value() for col in self.col_inputs]
            print(f"{row}: {col_vals}")