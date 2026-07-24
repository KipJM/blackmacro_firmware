# Extracted into separate file to prevent circular dependency issues :(

class Button:
    def __init__(self, name: str, matrix: tuple[int, int]):
        self.name: str = name
        self.matrix: tuple[int, int] = matrix

        self.pressed: bool = False

    def is_pressed(self) -> bool:
        return self.pressed

    def update_pressed(self, pressed: bool):
        if self.pressed != pressed:
            # state change
            # TODO: subscribable events?
            print(f"{self.name} {pressed}")
            self.pressed = pressed
