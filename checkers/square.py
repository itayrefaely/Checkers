import pygame
import constants
import copy


class Square:
    def __init__(self, size, row, col):
        self.size = size
        self.row = row
        self.col = col
        self.number = Square.compute_square_number(row, col)
        self.color = constants.LIGHT_SQUARE if (row + col) % 2 == 0 else constants.DARK_SQUARE
        self.free = True
        self.selected = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         pygame.Rect(self.col * self.size, self.row * self.size, self.size, self.size))

    def get_center(self):
        x = self.col * self.size + self.size // 2
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

    def select(self, board, pawn_radius):
        pygame.draw.circle(board.screen, constants.SELECT_COLOR, self.get_center(), pawn_radius, 4)
        self.selected = True

    def deselect(self, board, pawn_radius):
        pygame.draw.circle(board.screen, constants.DARK_SQUARE, self.get_center(), pawn_radius, 4)
        self.selected = False

    @staticmethod
    def is_valid_square_number(square_number):
        return True if 1 <= square_number <= 64 else False

    @staticmethod
    def is_marginal_column(square_number):
        return True if (square_number % 8) == 0 or (square_number % 8) == 1 else False

    def copy(self):
        square_copy = copy.deepcopy(self)
        square_copy.free = self.free
        square_copy.selected = self.selected
        return square_copy
