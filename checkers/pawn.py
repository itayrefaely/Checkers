import pygame
import constants
from square import Square 

class Pawn():
    def __init__(self, col, row, square_size, color, radius, queen = False):
        self.col = col
        self.row = row
        self.pos = (col * square_size + square_size // 2, row * square_size + square_size // 2)
        self.square_number = Square.computeSquareNumber(row, col)
        self.color_type = color
        self.color = constants.BLUE if self.color_type == "blue" else constants.RED
        self.radius = radius
        self.queen = queen
        self.highlighted = False
        self.selected = False
        self.can_eat = False
        self.ate_this_turn = False

    def draw(self, screen):
        inner_color = tuple([abs(c - 20) for c in self.color])
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        pygame.draw.circle(screen, inner_color, self.pos, self.radius - 8)
        pygame.draw.circle(screen, self.color, self.pos, self.radius - 15)
    
    def getNextSquares(self, board):
        """"
        Returns a set of the pawn's next possible squares
        """
        # If the pawn has capturing moves
        if self.can_eat: 
            return self.getNextJumpingSquares(board)

        possible_squares = self.computePossibleSquares()
        next_squares = self.filterInvalidSquares(possible_squares, board)
        return next_squares

    def computePossibleSquares(self):
        """"
        Returns a set of the initial possible squares for the pawn to move to
        """
        possible_squares = set()
        square_number = self.square_number 

        if self.color_type == "red":
            # Leftmost col
            if square_number % 8 == 1:
                possible_squares.add(square_number - 7)
            # Rightmost col
            elif square_number % 8 == 0:
                possible_squares.add(square_number - 9)
            else:
                possible_squares.add(square_number - 9)
                possible_squares.add(square_number - 7)
        # color_type = "blue"
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
    
    def filterInvalidSquares(self, possible_squares, board):
        """"
        Removes the invalid squares from the possible squares set
        """
        next_squares = set(possible_squares)
        to_remove = set()
        for square_number in next_squares:
            if not board.isSquareValidAndFree(square_number):
                to_remove.add(square_number)

        next_squares -= to_remove
        return next_squares
    
    def getNextJumpingSquares(self, board):
        """"
        Returns a set of squares that the pawn can move to after a single capture
        """
        jumping_squares = set()

        for jump_square_number in self.getPossibleJumpSquares():
            if self.isLegalJumpSquare(board, jump_square_number):
                jumping_squares.add(jump_square_number)

        self.can_eat = bool(jumping_squares)
        
        return jumping_squares
    
    def getPossibleJumpSquares(self):
        """"
        Returns an initial list of tuples of rows and columns that the pawn can jump to
        """
        possible_jump_squares = []
        
        for square_number in [self.square_number - 18, self.square_number -14, self.square_number + 14, self.square_number + 18]:
                _, col = Square.computeRowAndCol(square_number)
                if Square.isValidSquareNumber(square_number) and abs(self.col - col) <= 2:
                    possible_jump_squares.append(square_number)
        
        return possible_jump_squares

    def isLegalJumpSquare(self, board, jump_square_number):
        """"
        Indicates whether the pawn can jump to the given square
        """
        jump_square = board.squares[jump_square_number]

        if jump_square.free:
            opponent_square_number = Pawn.computeOpponentSquareNumber(self.square_number, jump_square_number)
            opponent = board.getOccupyingPawn(opponent_square_number)
            
            if not opponent or self.isSameTeam(opponent):
                return False

            opponent_row = opponent.row
            if self.isLegalCapture(opponent_row):
                return True
        
        return False

    def computeOpponentSquareNumber(start_square_number, jump_square_number):
        """"
        Computes the opponent's square number according to given jump square
        """
        return int((start_square_number + jump_square_number) / 2)

    def isSameTeam(self, opponent):
        return self.color_type == opponent.color_type

    def isLegalCapture(self, opponent_row):
        # Only queens can capture backwards
        return self.queen or (self.color_type == "red" and self.row > opponent_row) or (self.color_type == "blue" and self.row < opponent_row)
    
    def highlight(self, board):
        center = self.pos
        pygame.draw.circle(board.screen, constants.HIGHLIGHT_COLOR, center, self.radius, 4)
        self.highlighted = True

    def unhighlight(self, board):
        center = self.pos
        pygame.draw.circle(board.screen, constants.RED, center, self.radius, 4)
        self.highlighted = False

    def select(self, board):
        center = self.pos
        pygame.draw.circle(board.screen, constants.SELECT_COLOR, center, self.radius, 4)
        self.selected = True

    def deselect(self, board):
        center = self.pos
        pygame.draw.circle(board.screen, constants.RED, center, self.radius, 4)
        self.selected = False

    def isPromotion(self):
        # Queen can't be promoted again
        if self.queen:
            return False
        # Check if pawn made it to opponent's base row
        if (self.color_type == "blue" and self.row == 8) or (self.color_type == "red" and self.row == 1):
            return True
        
        return False