class Key:
    def __init__(self, matrix: tuple, led: int, position: tuple):
        self.matrix = matrix
        self.led = led
        self.position = position

### KEY DEFS
# Keyname: matrix(row 1-index, column 1-index), led 0-index, physical position(y,x, float, origin at bottom left, gaps considered)

# MOD key is not included. if you wanna deal with that write your own firmware
DEF_KEYS = {
    "LA1": Key((1,1), 1,  (4,0.5)),
    "LA2": Key((1,3), 0,  (4,2.5)),
    "LB1": Key((2,1), 5,  (3,0)),
    "LB2": Key((2,2), 4,  (3,1)),
    "LB3": Key((2,3), 3,  (3,2)),
    "LB4": Key((2,4), 2,  (3,3)),
    "LC1": Key((3,1), 9,  (2,0)),
    "LC2": Key((3,2), 8,  (2,1)),
    "LC3": Key((3,3), 7,  (2,2)),
    "LC4": Key((3,4), 6,  (2,3)),
    "LD1": Key((4,1), 13, (1,0)),
    "LD2": Key((4,2), 12, (1,1)),
    "LD3": Key((4,3), 11, (1,2)),
    "LD4": Key((4,4), 10, (1,3)),
    "LE1": Key((5,1), 15, (0,0)),
    "LE2": Key((5,2), 14, (0,2)),
    "RA1": Key((5,3), 20, (5,6.25)),
    "RA2": Key((5,4), 19, (5,7.75)),
    "RB1": Key((6,1), 18, (4,6)),
    "RB2": Key((6,2), 17, (4,7)),
    "RB3": Key((6,3), 16, (4,8))
}