from button import Button


class ButtonComponent(Button):

    def __init__(self, texture_file_name, texture_size, pos):
        super().__init__(texture_file_name, texture_size, pos, text=None)
