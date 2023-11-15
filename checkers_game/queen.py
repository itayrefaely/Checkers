import os
import pygame
from pawn import Pawn


class Queen(Pawn):
    def __init__(self, col, row, square_size, color, radius, is_original_queen=True):
        # Call the constructor of the parent class (Pawn) to initialize common attributes
        super().__init__(col, row, square_size, color, radius, queen=True, is_original_pawn=is_original_queen)

        if is_original_queen:
            # Load the crown image
            self.crown_texture = self.load_crown_texture('crown_vector_icon.png')

    def load_crown_texture(self, crown_file_name):
        # Get the directory of the current script
        current_script_directory = os.path.dirname(os.path.abspath(__file__))

        # Add the file name to the sys.path
        file_path = os.path.join(current_script_directory, crown_file_name)

        crown_image = pygame.image.load(file_path)

        # Scale the crown image to fit on top of the pawn
        crown_size = (1.5 * self.radius, 1.5 * self.radius)
        crown_texture = pygame.transform.scale(crown_image, crown_size)

        return crown_texture

    def get_crown_x_and_y(self):
        crown_x = self.center[0] - 0.725 * self.radius
        crown_y = self.center[1] - 0.8 * self.radius
        return crown_x, crown_y

    def compute_possible_squares(self):
        """
        Overrides the original computePossibleSquares method of the Pawn class.

        Queens can move backwards.
        """
        square_number = self.square_number
        possible_squares = {
            square_number - 9,
            square_number - 7,
            square_number + 7,
            square_number + 9
        }

        # Leftmost col
        if square_number % 8 == 1:
            possible_squares.remove(square_number - 9)
            possible_squares.remove(square_number + 7)
        # Rightmost col
        elif square_number % 8 == 0:
            possible_squares.remove(square_number - 7)
            possible_squares.remove(square_number + 9)

        return possible_squares

    def copy(self):
        queen_copy = Queen(self.col, self.row, self.square_size, self.color_type, self.radius, is_original_queen=False)
        queen_copy.highlighted = self.highlighted
        queen_copy.selected = self.selected
        queen_copy.can_eat = self.can_eat
        queen_copy.ate_this_turn = self.ate_this_turn
        return queen_copy
