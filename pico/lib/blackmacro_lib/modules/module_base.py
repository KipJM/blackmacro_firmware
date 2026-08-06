## The base module that modules inherit from. After creating a module, make sure to register it through pico_main.py
## Modules are allowed to block thread wait, however it's not really recommended (don't block more than ~2 seconds)


class SpeedEditorModule:
    feature_id: int = -1
    input_id: int = -1
    output_id: int = -1

    def __init__(self, interface: SpeedEditorInterface):
        self.k = interface


        if self.feature_id != -1:
            interface.set_feature_report_handlers[self.feature_id] = self.set_feature_report
        if self.output_id != -1:
            interface.set_output_report_handlers[self.output_id] = self.set_output_report

        if self.feature_id != -1:
            interface.get_feature_report_handlers[self.feature_id] = self.get_feature_report
        if self.input_id != -1:
            interface.get_input_report_handlers[self.input_id] = self.get_input_report


    ## do not include the initial report_id byte. Interface will add it automatically
    def get_feature_report(self):
        print(f"GET FEATURE {self.feature_id} NOT IMPLEMENTED")
        return False

    def set_feature_report(self, report_data:bytes) -> bool:
        print(f"SET FEATURE {self.feature_id} NOT IMPLEMENTED")
        return False


    ## do not include the initial report_id byte. Interface will add it automatically
    def get_input_report(self):
        return False

    def set_output_report(self, report_data:bytes) -> bool:
        return False
