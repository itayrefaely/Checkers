import pygame
import constants

class Square():
    def __init__(self, size, row, col):
        self.size = size
        self.row = row
        self.col = col
        self.number = Square.computeSquareNumber(row, col)
        self.color = constants.LIGHT_SQUARE if (row + col) % 2 == 0 else constants.DARK_SQUARE
        self.free = True
        self.selected = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.col * self.size, self.row * self.size, self.size, self.size))
    
    def getCenter(self):
        x = self.col * self.size + self.size // 2
        y = self.row * self.size + self.size // 2
        return x, y
    
    def computeSquareNumber(row, col):
        return 8 * (row - 1) + col
    
    def computeRowAndCol(square_number):
        """"
        Returns row, col indeces (between 1 and 8 inclusive)
        """
        row = 1 + (square_number - 1) // 8
        col = 1 + (square_number - 1) % 8
        return row, col
    
    def select(self, board, pawn_radius):
        pygame.draw.circle(board.screen, constants.SELECT_COLOR, self.getCenter(), pawn_radius, 4)
        self.selected = True
    
    def deselect(self, board, pawn_radius):
        pygame.draw.circle(board.screen, constants.DARK_SQUARE, self.getCenter(), pawn_radius, 4)
        self.selected = False

    def isValidSquareNumber(square_number):
        return True if 1 <= square_number <= 64 else False
    
    def isMarginalColumn(square_number):
        return True if (square_number % 8) == 0 or (square_number % 8) == 1 else False