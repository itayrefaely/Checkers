import os
import pygame
from square import Square


class Pawn:
    def __init__(self, col, row, square_size, color, radius, queen=False, is_original_pawn=True):
        self.col = col
        self.row = row
        self.square_number = Square.compute_square_number(row, col)
        self.radius = radius
        self.color_type = color
        self.queen = queen
        self.can_eat = False
        self.ate_this_turn = False
        self.square_size = square_size

        if is_original_pawn:
            self.center = ((col - 0.5) * square_size + square_size // 2, row * square_size + square_size // 2)
            self.highlighted = False
            self.selected = False
            self.texture = self.load_texture('textures/white_pawn_icon.png') if self.color_type == "white" else (
                self.load_texture('textures/black_pawn_icon.png'))

    def load_texture(self, pawn_file_name):
        # Get the directory of the current script
        current_script_directory = os.path.dirname(os.path.abspath(__file__))

        # Add the file name to the sys.path
        file_path = os.path.join(current_script_directory, pawn_file_name)

        pawn_image = pygame.image.load(file_path)

        # Scale the board texture to fit the board size
        pawn_size = (4 * self.radius, 4 * self.radius)
        pawn_texture = pygame.transform.scale(pawn_image, pawn_size)

        return pawn_texture

    def get_x_and_y(self):
        pawn_x = self.center[0] - 2 * self.radius
        pawn_y = self.center[1] - 2 * self.radius
        return pawn_x, pawn_y

    def get_next_squares(self, board):
        """"
        Returns a set of the pawn's next possible squares
        """
        # If the pawn has capturing moves
        if self.can_eat:
            return self.get_next_jumping_squares(board)

        possible_squares = self.compute_possible_squares()
        next_squares = self.filter_invalid_squares(possible_squares, board)
        return next_squares

    def compute_possible_squares(self):
        """"
        Returns a set of the initial possible squares for the pawn to move to
        """
        possible_squares = set()
        square_number = self.square_number

        if self.color_type == "black":
            # Leftmost col
            if square_number % 8 == 1:
                possible_squares.add(square_number - 7)
            # Rightmost col
            elif square_number % 8 == 0:
                possible_squares.add(square_number - 9)
            else:
                possible_squares.add(square_number - 9)
                possible_squares.add(square_number - 7)
        # color_type = "white"
        else:
            # Leftmost col
            if square_number % 8 == 1:
                possible_squares.add(square_number + 9)
            # Rightmost col
            elif square_number % 8 == 0:
                possible_squares.add(square_number + 7)
            else:
                possible_squares.add(square_number + 9)
                possible_squares.add(square_number + 7)

        return possible_squares

    @staticmethod
    def filter_invalid_squares(possible_squares, board):
        """"
        Removes the invalid squares from the possible squares set
        """
        next_squares = set(possible_squares)
        to_remove = set()
        for square_number in next_squares:
            if not board.is_square_valid_and_free(square_number):
                to_remove.add(square_number)

        next_squares -= to_remove
        return next_squares

    def get_next_jumping_squares(self, board):
        """"
        Returns a set of squares that the pawn can move to after a single capture
        """
        jumping_squares = set()

        for jump_square_number in self.get_possible_jump_squares():
            if self.is_legal_jump_square(board, jump_square_number):
                jumping_squares.add(jump_square_number)

        self.can_eat = bool(jumping_squares)

        return jumping_squares

    def get_possible_jump_squares(self):
        """"
        Returns an initial list of tuples of rows and columns that the pawn can jump to
        """
        possible_jump_squares = []

        for square_number in [self.square_number - 18, self.square_number - 14, self.square_number + 14,
                              self.square_number + 18]:
            _, col = Square.compute_row_and_col(square_number)
            if Square.is_valid_square_number(square_number) and abs(self.col - col) <= 2:
                possible_jump_squares.append(square_number)

        return possible_jump_squares

    def is_legal_jump_square(self, board, jump_square_number):
        """"
        Indicates whether the pawn can jump to the given square
        """
        jump_square = board.squares[jump_square_number]

        if jump_square.free:
            opponent_square_number = Pawn.compute_opponent_square_number(self.square_number, jump_square_number)
            opponent = board.get_occupying_pawn(opponent_square_number)

            if not opponent or self.is_same_team(opponent):
                return False

            opponent_row = opponent.row
            if self.is_legal_capture(opponent_row):
                return True

        return False

    @staticmethod
    def compute_opponent_square_number(start_square_number, jump_square_number):
        """"
        Computes the opponent's square number according to given jump square
        """
        return int((start_square_number + jump_square_number) / 2)

    def is_same_team(self, opponent):
        return self.color_type == opponent.color_type

    def is_legal_capture(self, opponent_row):
        # Only queens can capture backwards
        return self.queen or (self.color_type == "black" and self.row > opponent_row) or (
                    self.color_type == "white" and self.row < opponent_row)

    def highlight(self, ui):
        ui.draw_highlight_pawn(self.center, self.radius)
        self.highlighted = True

    def unhighlight(self):
        self.highlighted = False

    def select(self, ui):
        ui.draw_select_pawn(self.center, self.radius)
        self.selected = True

    def deselect(self):
        self.selected = False

    def is_promotion(self):
        # Queen can't be promoted again
        if self.queen:
            return False
        # Check if pawn made it to opponent's base row
        if (self.color_type == "white" and self.row == 8) or (self.color_type == "black" and self.row == 1):
            return True

        return False

    def copy(self):
        pawn_copy = Pawn(self.col, self.row, self.square_size, self.color_type, self.radius, self.queen,
                         is_original_pawn=False)
        pawn_copy.highlighted = self.highlighted
        pawn_copy.selected = self.selected
        pawn_copy.can_eat = self.can_eat
        pawn_copy.ate_this_turn = self.ate_this_turn
        return pawn_copy
