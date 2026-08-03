# Extracted into separate file to prevent circular dependency issues :(

class Button:
    def __init__(self, name: str, matrix: tuple[int, int]):
        self.name: str = name
        self.matrix: tuple[int, int] = matrix

        self.pressed: bool = False

        self.update_callbacks = []

    def register_update_callback(self, callback):
        self.update_callbacks.append(callback)

    def is_pressed(self) -> bool:
        return self.pressed

    def update_pressed(self, pressed: bool) -> bool:
        """
        :param pressed:
        :return: True if state changed, else False
        """
        if self.pressed != pressed:
            # state change
            print(f"{self.name} {pressed}")
            self.pressed = pressed
            for callback in self.update_callbacks:
                callback(self, pressed)
            return True
        return False
