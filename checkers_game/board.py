import os
import numpy as np
import pygame

from pawn import Pawn
from queen import Queen
from square import Square


class Board:
    def __init__(self, board_side_length, is_original_board=True):
        pygame.init()

        # Define parameters
        self.num_rows = 8
        self.square_size = board_side_length // self.num_rows
        self.width = self.num_rows * self.square_size
        self.height = self.num_rows * self.square_size
        self.pawn_radius = (self.square_size // 2) - 5

        self.is_original_board = is_original_board

        # Initiate squares array with a dummy square
        self.squares = [Square(0, -1, -1)]

        # Initiate teams
        self.white_team = set()
        self.black_team = set()

        if is_original_board:
            # Define parameters
            self.pos = (0.5 * self.square_size, self.square_size)
            # Load the game board texture
            self.texture = self.load_texture('textures/board_texture.png', self.width, self.height)
            # Initialize the board squares and pawns
            self.init_squares()
            self.init_white_pawns()
            self.init_black_pawns()

    def load_texture(self, texture_file_name, width, height):
        file_path = self.get_file_path(texture_file_name)
        board_image = pygame.image.load(file_path)

        # Scale the board texture to fit the board size
        texture_size = (width, height)
        texture = pygame.transform.scale(board_image, texture_size)

        return texture

    @staticmethod
    def get_file_path(filename):
        """
        Get the full path to the file based on the provided filename.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_directory, filename)
        return full_path

    def init_squares(self):
        for row in range(1, self.num_rows + 1):
            for col in range(1, self.num_rows + 1):
                square = Square(self.square_size, row, col)
                self.squares.append(square)

    def init_white_pawns(self):
        for row in range(1, 4):
            for col in range(1, self.num_rows + 1):
                if (row + col) % 2 != 0:
                    pawn = Pawn(col, row, self.square_size, "white", self.pawn_radius)
                    self.white_team.add(pawn)

                    # Mark the relevant square as not free
                    self.squares[pawn.square_number].free = False

    def init_black_pawns(self):
        for row in range(6, 9):
            for col in range(1, self.num_rows + 1):
                if (row + col) % 2 != 0:
                    pawn = Pawn(col, row, self.square_size, "black", self.pawn_radius)
                    self.black_team.add(pawn)

                    # Mark the relevant square as not free
                    self.squares[pawn.square_number].free = False

    def get_occupying_pawn(self, square_number):
        """"
        Retrieve the pawn occupying a given square, if not occupied returns None
        """
        square_number = int(square_number)
        # Square is not occupied
        if self.squares[square_number].free:
            return None

        for pawn in self.black_team:
            if pawn.square_number == square_number:
                return pawn

        for pawn in self.white_team:
            if pawn.square_number == square_number:
                return pawn

    def delete_pawn(self, pawn, ui):
        square_number = pawn.square_number
        self.squares[square_number].free = True

        if pawn.color_type == "black":
            self.black_team.remove(pawn)
        else:
            self.white_team.remove(pawn)

        if self.is_original_board:
            # Draw the updated board
            ui.draw()
        del pawn

    def add_pawn(self, pawn):
        square_number = pawn.square_number
        self.squares[square_number].free = False
        if pawn.color_type == "black":
            self.black_team.add(pawn)
        else:
            self.white_team.add(pawn)

    def is_square_valid_and_free(self, square_number):
        return Square.is_valid_square_number(square_number) and self.squares[square_number].free

    def promote_pawn(self, pawn, ui):
        copy = pawn.copy()
        self.delete_pawn(pawn, ui)
        queen = Queen(copy.col, copy.row, self.square_size, copy.color_type, self.pawn_radius)
        self.add_pawn(queen)

    def deserialize(self):
        board_array = np.zeros((8, 8), dtype=int)
        for row in range(8):
            for col in range(8):
                if (row % 2) == (col % 2):
                    # Unusable square
                    continue
                else:
                    square_number = Square.compute_square_number(row + 1, col + 1)
                    pawn = self.get_occupying_pawn(square_number)
                    if not pawn:
                        # Empty square
                        continue

                    if pawn.color_type == 'white':
                        if pawn.queen:
                            board_array[row, col] = '3'
                        else:
                            board_array[row, col] = '1'
                    else:
                        if pawn.queen:
                            board_array[row, col] = '-3'
                        else:
                            board_array[row, col] = '-1'

        return board_array

    def copy(self):
        board_copy = Board(self.width, is_original_board=False)

        # Copy the squares, except the dummy
        for square in self.squares[1:]:
            board_copy.squares.append(square.copy())

        # Copy the pawns
        for pawn in self.black_team:
            board_copy.black_team.add(pawn.copy())
        for pawn in self.white_team:
            board_copy.white_team.add(pawn.copy())

        board_copy.screen = None

        return board_copy
    
    def reset(self):
        self.squares = [Square(0, -1, -1)]
        self.white_team = set()
        self.black_team = set()

        self.init_squares()
        self.init_white_pawns()
        self.init_black_pawns()
