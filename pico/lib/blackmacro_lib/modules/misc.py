from blackmacro_lib.modules.module_base import SpeedEditorModule
from blackmacro_lib.settings import SpeedEditorSettings


class InitModule(SpeedEditorModule):
    feature_id = 0x01

    def get_feature_report(self):
        return bytearray.fromhex("4D 02 25 7B 01 05 02") # I have no idea what these bytes mean


class SerialNumberModule(SpeedEditorModule):
    feature_id = 0x08

    def get_feature_report(self):
        # Yes the serial looks like hex, but it's transmitted as ascii
        return bytearray(SpeedEditorSettings.STR_SERIAL.encode("ascii"))