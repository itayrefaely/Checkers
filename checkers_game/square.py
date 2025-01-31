import copy


class Square:
    def __init__(self, size, row, col):
        self.size = size
        self.row = row
        self.col = col
        self.number = Square.compute_square_number(row, col)
        self.free = True
        self.selected = False

    def get_center(self):
        x = (self.col - 0.5) * self.size + self.size // 2
        y = self.row * self.size + self.size // 2
        return x, y

    @staticmethod
    def compute_square_number(row, col):
        return 8 * (row - 1) + col

    @staticmethod
    def compute_row_and_col(square_number):
        """"
        Returns row, col indices (between 1 and 8 inclusive)
        """
        row = 1 + (square_number - 1) // 8
        col = 1 + (square_number - 1) % 8
        return row, col

    def select(self, pawn_radius, ui):
        ui.draw_select_square(self.get_center(), pawn_radius)
        self.selected = True

    def deselect(self):
        self.selected = False

    @staticmethod
    def is_valid_square_number(square_number):
        return True if 1 <= square_number <= 64 else False

    def copy(self):
        square_copy = copy.deepcopy(self)
        square_copy.free = self.free
        square_copy.selected = self.selected
        return square_copy
