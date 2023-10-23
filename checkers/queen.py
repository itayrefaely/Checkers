import pygame
import constants
from square import Square 
from pawn import Pawn
from PIL import Image

class Queen(Pawn):
    def __init__(self, col, row, square_size, color, radius, screen):
        # Call the constructor of the parent class (Pawn) to initialize common attributes
        super().__init__(col, row, square_size, color, radius, queen=True)

        # Load the crown image
        self.crown = self.loadCrown()

        # Draw the queen object when created (is not part of the board initialization)
        self.draw(screen)

    def loadCrown(self):
        crown_image = pygame.image.load('./checkers/crown-vector-icon.png')

        # Scale the crown image to fit on top of the pawn
        crown_size = (1.5 * self.radius, 1.5 * self.radius)
        crown_surface = pygame.transform.scale(crown_image, crown_size)

        return crown_surface

    def draw(self, screen):
        # Call the draw method of the parent class (Pawn) to draw the pawn
        super().draw(screen)

        # Calculate the position to center the crown on top of the pawn
        crown_x = self.pos[0] - 0.75 * self.radius  
        crown_y = self.pos[1] - 0.9 * self.radius  

        # Draw the crown image on top of the pawn
        screen.blit(self.crown, (crown_x, crown_y))

    
    def computePossibleSquares(self):
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