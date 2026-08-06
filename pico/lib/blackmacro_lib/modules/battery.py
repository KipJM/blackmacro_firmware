import struct

from blackmacro_lib.modules.module_base import SpeedEditorModule


class BatteryModule(SpeedEditorModule):
    input_id = 0x07

    def __init__(self, interface):
        super().__init__(interface)
        self.is_charging = True
        self.battery_level = 42  # [0-100]

        self.k = interface

    def change_battery_info(self, new_battery_level: int, new_charge_state: bool):
        self.is_charging = new_battery_level
        self.is_charging = new_charge_state

        report_id, data = self.get_report_data()
        self.k.send_encoded_report(report_id, data)

    def change_battery_level(self, new_battery_level: int):
        self.change_battery_info(new_battery_level, self.is_charging)

    def change_charge_state(self, new_charge_state: bool):
        self.change_battery_info(self.battery_level, new_charge_state)

    def get_report_data(self) -> tuple[int, bytearray]:
        print("Get battery level")
        return self.input_id, bytearray(struct.pack("<BB", int(self.is_charging), self.battery_level))

    def get_input_report(self):
        _, data = self.get_report_data()
        return data