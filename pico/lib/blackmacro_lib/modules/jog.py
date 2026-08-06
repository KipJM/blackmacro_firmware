import math
import struct

from blackmacro_lib.modules.module_base import SpeedEditorModule
from blackmacro_lib.hid_keys import SpeedEditorJogMode, SpeedEditorJogConstant


class JogModule(SpeedEditorModule):
    input_id = 0x03
    output_id = 0x03

    def __init__(self, interface):
        super().__init__(interface)
        self.angle: int = 0
        self.delta: int = 0

        self.jog_mode: int = SpeedEditorJogMode.RELATIVE

    def set_output_report(self, report_data:bytes) -> bool:
        print(report_data.hex())
        _, mode, _, _ = struct.unpack('<BBIB', report_data)
        if mode < 0 or mode > 3:
            print(f"Invalid jog mode {mode} received!")
            return False

        self.jog_mode = mode

        if self.jog_mode == SpeedEditorJogMode.RELATIVE or self.jog_mode == SpeedEditorJogMode.RELATIVE_FINE:
            # Reset any loops
            self.angle = self.get_wrapped_angle(self.angle)
        elif self.jog_mode == SpeedEditorJogMode.ABSOLUTE_CONTINUOUS or self.jog_mode == SpeedEditorJogMode.ABSOLUTE_DEADZERO:
            # Reset angle to zero
            self.angle = 0

        # Reset deltas
        self.delta = 0

        self.send_jog_update()

        print(f"Jog mode now set to {mode}")
        return True


    def get_wrapped_angle(self, angle: int) -> int:
        range_len = SpeedEditorJogConstant.MAX_VAL - SpeedEditorJogConstant.MIN_VAL
        return (angle - SpeedEditorJogConstant.MIN_VAL) % range_len + SpeedEditorJogConstant.MIN_VAL


    # Angle can be over -4096/4096, detected as turned more than half a turn
    def set_angle(self, new_angle: int):
        self.angle = new_angle

        self.send_jog_update()

    def set_angle_degrees(self, new_angle: float, delta: float):
        """
        :param new_angle: Degrees, top = 0, clockwise, within 360
        """
        self.delta = int(delta / 360 * SpeedEditorJogConstant.MAX_VAL * 2)
        ang = int(new_angle / 360 * SpeedEditorJogConstant.MAX_VAL * 2)
        if ang > SpeedEditorJogConstant.MAX_VAL:
            ang = -(2 * SpeedEditorJogConstant.MAX_VAL - ang)
        self.set_angle(ang)

    def set_angle_radians(self, new_angle: float):
        """
        :param new_angle: Radians, where 0 = pointing right. Bigger values = rotating counterclockwise.
        """
        range_len = (SpeedEditorJogConstant.MAX_VAL - SpeedEditorJogConstant.MIN_VAL) / 2
        self.set_angle(int(-(range_len * new_angle - (range_len/2) * math.pi) / math.pi))

    def get_angle_radians(self) -> float:
        """
        :return: Radians, where 0 = pointing right. Bigger values = rotating counterclockwise. Values may be bigger than 2pi.
        """
        range_len = (SpeedEditorJogConstant.MAX_VAL - SpeedEditorJogConstant.MIN_VAL) / 2
        return -self.angle * math.pi / range_len + (math.pi / 2.0)

    # this func is done with AI since I really cant bother with this
    def get_angle_symbol(self) -> str:
        clocks = [
            "🕛", "🕧", "🕐", "🕜", "🕑", "🕝",
            "🕒", "🕞", "🕓", "🕟", "🕔", "🕠",
            "🕕", "🕡", "🕖", "🕢", "🕗", "🕣",
            "🕘", "🕤", "🕙", "🕥", "🕚", "🕦"
        ]

        # Convert value → angle in degrees
        angle = (self.angle / 8192) * 360  # 8192 = full rotation

        # Normalize to [0, 360)
        angle %= 360

        # Convert angle to clock index (24 steps)
        index = round(angle / 15) % 24  # 360 / 24 = 15 degrees per step

        return clocks[index]


    # returns the angle data which will be composed into a complete jog report.
    def get_report_data(self) -> int:
        # print(self.jog_mode)
        # print(self.angle, self.delta)
        # print()
        # Calculate rotate report
        if self.jog_mode == SpeedEditorJogMode.RELATIVE:
            report_data = self.delta
        elif self.jog_mode == SpeedEditorJogMode.ABSOLUTE_CONTINUOUS:
            report_data = int(math.fmod(self.angle, SpeedEditorJogConstant.MAX_VAL)) #TODO: maybe remove modulo
        elif self.jog_mode == SpeedEditorJogMode.RELATIVE_FINE:
            report_data = self.delta * SpeedEditorJogConstant.FINE_MULTIPLIER # yes this is the same as mode 0
        elif self.jog_mode == SpeedEditorJogMode.ABSOLUTE_DEADZERO:
            if SpeedEditorJogConstant.DEADZERO_MIN < self.angle < SpeedEditorJogConstant.DEADZERO_MAX:
                report_data = 0
            else:
                report_data = self.angle
        else:
            print("Error updating dial angle: INVALID JOG MODE!")
            return 0

        return report_data

    def send_jog_update(self):
        data = self.get_report_data()
        self.k.send_encoded_report(self.output_id, struct.pack("<BiB", self.jog_mode, data, 1)) # TODO: What should be the last val?

    def get_input_report(self):
        data = self.get_report_data()
        return bytearray(struct.pack("<BiB", self.jog_mode, data, 1))  # TODO: What should be the last val?
