# Regular keyboard encoders.
# The magnetic encoder will be handled in dial files
import hardware_defs
from button import Button
from rotary_irq_rp2 import RotaryIRQ

class Encoder(Button):
    def __init__(self, name: str, matrix: tuple[int, int], pins: tuple[int, int]):
        super().__init__(name, matrix)

        self.encoder: RotaryIRQ = RotaryIRQ(
            pin_num_clk=pins[0],
            pin_num_dt=pins[1],
            min_val=0,
            max_val=-1, # unbounded
            incr=1,
            reverse=False,
            range_mode=RotaryIRQ.RANGE_UNBOUNDED,
            pull_up=True,
            half_step=False,
            invert=False
        )

        self.last_encoder_value: int = 0

        self.encoder.add_listener(self.encoder_change_handler)

        self.change_callbacks = []


    def add_change_callback(self, callback):
        self.change_callbacks.append(callback)

    def encoder_change_handler(self):
        if self.encoder.value() > self.last_encoder_value:
            self.rot_clockwise()
        else:
            self.rot_counterclockwise()

        for callback in self.change_callbacks:
            callback(self.encoder.value())

        self.last_encoder_value = self.encoder.value()

    def rot_clockwise(self):
        print(f"{self.name} CW -> {self.encoder.value()}")
        return # TODO

    def rot_counterclockwise(self):
        print(f"{self.name} CCW -> {self.encoder.value()}")
        return #TODO


## ENCODERS
# (row, column)
DEF_ENCODERS: dict[str, Encoder] = {
    "RENC1" : Encoder("RENC1", (1,2), (hardware_defs.P_RENC1_A, hardware_defs.P_RENC1_B)),
    "RENC2" : Encoder("RENC2", (1,4), (hardware_defs.P_RENC2_A, hardware_defs.P_RENC2_B))
}