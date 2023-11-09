import numpy as np
import pygame
from pawn import Pawn
from queen import Queen
from square import Square
import constants


class Board:
    def __init__(self, width, height, is_initial_board=True):
        pygame.init()

        # Initiate teams
        self.red_team = set()
        self.blue_team = set()

        # Initiate squares array with a dummy square
        self.squares = [Square(0, -1, -1)]

        self.board_size = 10

        # Define parameters
        self.square_size = min(width, height) // self.board_size  # 72
        self.board_width = self.board_size * self.square_size  # 720
        self.board_height = self.board_size * self.square_size  # 720
        self.pawn_radius = (self.square_size // 2) - 5
        self.is_initial_board = is_initial_board

        if is_initial_board:
            # Create a pygame surface
            self.screen = pygame.display.set_mode((self.board_width, self.board_height))
            pygame.display.set_caption("Checkers")

            # Add the board squares and pawns
            self.init_squares()
            self.init_blue_pawns()
            self.init_red_pawns()

    def init_squares(self):
        for row in range(1, self.board_size - 1):
            for col in range(1, self.board_size - 1):
                square = Square(self.square_size, row, col)
                self.squares.append(square)

    def init_blue_pawns(self):
        for row in range(1, 4):
            for col in range(1, self.board_size - 1):
                if (row + col) % 2 != 0:
                    pawn = Pawn(col, row, self.square_size, "blue", self.pawn_radius)
                    self.blue_team.add(pawn)

                    # Mark the relevant square as not free
                    self.squares[pawn.square_number].free = False

    def init_red_pawns(self):
        for row in range(6, 9):
            for col in range(1, self.board_size - 1):
                if (row + col) % 2 != 0:
                    pawn = Pawn(col, row, self.square_size, "red", self.pawn_radius)
                    self.red_team.add(pawn)

                    # Mark the relevant square as not free
                    self.squares[pawn.square_number].free = False

    def get_square_size(self):
        return self.square_size

    def draw_frame(self):
        """"
        Draws the game board frame, including the inner and outer frames, as well as row and column labels.
        """
        frame_color = constants.WHITE
        frame_thickness = 5

        self.draw_inner_frame(frame_color, frame_thickness)
        self.draw_outer_frame(frame_color, frame_thickness)
        self.label_rows_and_columns(frame_color)

    def draw_inner_frame(self, color, thickness):
        inner_frame_rect = pygame.Rect(0.1 * self.board_width - 5, 0.1 * self.board_height - 5,
                                       0.8 * self.board_width + 10, 0.8 * self.board_height + 10)
        pygame.draw.rect(self.screen, color, inner_frame_rect, thickness)

    def draw_outer_frame(self, color, thickness):
        outer_frame_rect = pygame.Rect(0, 0, self.board_width, self.board_height)
        pygame.draw.rect(self.screen, color, outer_frame_rect, thickness)

    def label_rows_and_columns(self, color):
        font = pygame.font.SysFont('Arial', 30)

        for i in range(1, self.board_size - 1):
            row_label = font.render(str(self.board_size - i - 1), True, color)
            row_rect1, row_rect2 = row_label.get_rect(), row_label.get_rect()
            row_rect1.center, row_rect2.center = (self.square_size // 2, (i + 0.5) * self.square_size), (
                self.board_width - (self.square_size // 2), (i + 0.5) * self.square_size)
            self.screen.blit(row_label, row_rect1)
            self.screen.blit(row_label, row_rect2)

            col_label = font.render(chr(ord('A') + i - 1), True, color)
            col_rect1, col_rect2 = col_label.get_rect(), col_label.get_rect()
            col_rect1.center, col_rect2.center = (
                (i + 0.5) * self.square_size, self.board_height - self.square_size // 2), (
                (i + 0.5) * self.square_size, self.board_height - (self.board_height - self.square_size // 2))
            self.screen.blit(col_label, col_rect1)
            self.screen.blit(col_label, col_rect2)

    def draw(self):
        """"
        Draws the game board frame, the board itself and pawns
        """
        self.draw_frame()
        for square in self.squares[1:]:
            square.draw(self.screen)
        for pawn in self.blue_team:
            pawn.draw(self.screen)
        for pawn in self.red_team:
            pawn.draw(self.screen)

    def get_occupying_pawn(self, square_number):
        """"
        Retrieve the pawn occupying a given square, if not occupied returns None
        """
        square_number = int(square_number)
        # Square is not occupied
        if self.squares[square_number].free == True:
            return None

        for pawn in self.red_team:
            if pawn.square_number == square_number:
                return pawn

        for pawn in self.blue_team:
            if pawn.square_number == square_number:
                return pawn

    def delete_pawn(self, pawn):
        square_number = pawn.square_number
        self.squares[square_number].free = True

        if self.is_initial_board:
            # Draw a square on top of the pawn 
            self.squares[square_number].draw(self.screen)

        if pawn.color_type == "red":
            self.red_team.remove(pawn)
        else:
            self.blue_team.remove(pawn)

        del pawn

    def add_pawn(self, pawn):
        square_number = pawn.square_number
        self.squares[square_number].free = False
        if pawn.color_type == "red":
            self.red_team.add(pawn)
        else:
            self.blue_team.add(pawn)

    def is_square_valid_and_free(self, square_number):
        return Square.is_valid_square_number(square_number) and self.squares[square_number].free

    def promote_pawn(self, pawn):
        copy = pawn.copy()
        self.delete_pawn(pawn)
        queen = Queen(copy.col, copy.row, self.square_size, copy.color_type, self.pawn_radius, self.screen)
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

                    if pawn.color_type == 'blue':
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

    def play_move_on_deserialized_board(deserialized_board, start_square_number, end_square_number, is_capture):
        start_row, start_col = Square.compute_row_and_col(start_square_number)
        end_row, end_col = Square.compute_row_and_col(end_square_number)

        prev_pawn_value = deserialized_board[start_row - 1, start_col - 1]
        cur_pawn_value = Board.get_deserialized_pawn_value(prev_pawn_value, end_square_number)

        # Update move on the board
        if is_capture:
            capture_square_number = Pawn.compute_opponent_square_number(start_square_number, end_square_number)
            capture_row, capture_col = Square.compute_row_and_col(capture_square_number)
            deserialized_board[capture_row - 1, capture_col - 1] = 0
        deserialized_board[start_row - 1, start_col - 1] = 0
        deserialized_board[end_row - 1, end_col - 1] = cur_pawn_value

        return deserialized_board

    def get_deserialized_pawn_value(prev_pawn_value, end_square_number):
        # end_square is a promotion square
        if (prev_pawn_value == 1 and 57 <= end_square_number <= 64) or \
                (prev_pawn_value == -1 and 1 <= end_square_number <= 8):
            new_pawn_value = 3 * prev_pawn_value
            return new_pawn_value

        return prev_pawn_value

    def copy(self):
        board_copy = Board(self.board_width, self.board_height, is_initial_board=False)

        # Copy the squares, except the dummy
        for square in self.squares[1:]:
            board_copy.squares.append(square.copy())

        # Copy the pawns
        for pawn in self.red_team:
            board_copy.red_team.add(pawn.copy())
        for pawn in self.blue_team:
            board_copy.blue_team.add(pawn.copy())

        board_copy.screen = None

        return board_copy
