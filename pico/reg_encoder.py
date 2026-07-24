# Regular keyboard encoders.
# The magnetic encoder will be handled in dial files
from key import Button


class Encoder(Button):
    def __init__(self, name: str, matrix: tuple[int, int]):
        super().__init__(name, matrix)

        self.angle: int = 0

    def rot_clockwise(self):
        pass # TODO

    def rot_counterclockwise(self):
        pass # TODO


## ENCODERS
# (row, column)
DEF_ENCODERS: dict[str, Encoder] = {
    "RENC1" : Encoder("RENC1", (1,2)),
    "RENC2" : Encoder("RENC2", (1,4))
}