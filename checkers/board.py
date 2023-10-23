import numpy as np
import pygame
from pawn import Pawn
from queen import Queen
from square import Square 
import constants

class Board():
    def __init__(self, width, height):
        pygame.init()

        # Initiate teams
        self.red_team = set()
        self.blue_team = set()

        # Initiate squares array with a dummy square
        self.squares = [Square]

        self.board_size = 10

        # Define number and size of squares
        self.square_size = min(width, height) // self.board_size # 72
        self.board_width = self.board_size * self.square_size    # 720
        self.board_height = self.board_size * self.square_size   # 720

        # Create a pygame surface
        self.screen = pygame.display.set_mode((self.board_width, self.board_height))
        pygame.display.set_caption("Checkers")

        # Draw the board squares
        self.initSquares()

        # Add pawns
        self.pawnRadius = (self.square_size // 2) - 5
        self.initBluePawns()
        self.initRedPawns()

        ####### Add debugging pawns #######
        # pawn = Pawn(4, 5, self.square_size, "blue", self.pawnRadius)
        # self.blue_team.add(pawn)
        # pawn.draw(self.screen)
        # self.squares[pawn.square_number].free = False
        
        # pawn = Pawn(4, 3, self.square_size, "blue", self.pawnRadius)
        # self.blue_team.add(pawn)
        # pawn.draw(self.screen)
        # self.squares[pawn.square_number].free = False

        # pawn = Pawn(6, 3, self.square_size, "blue", self.pawnRadius)
        # self.blue_team.add(pawn)
        # pawn.draw(self.screen)
        # self.squares[pawn.square_number].free = False

        # pawn = Pawn(2, 5, self.square_size, "blue", self.pawnRadius)
        # self.blue_team.add(pawn)
        # pawn.draw(self.screen)
        # self.squares[pawn.square_number].free = False

        # Draw frame
        self.drawFrame()
        
        # Update the display
        pygame.display.flip()

    def initSquares(self):
        for row in range(1, self.board_size - 1):
            for col in range(1, self.board_size - 1):
                square = Square(self.square_size, row, col)
                self.squares.append(square)
                square.draw(self.screen)

    def initBluePawns(self):
        for row in range(1, 4):
            for col in range(1, self.board_size - 1):
                if (row + col) % 2 != 0:
                    pawn = Pawn(col, row, self.square_size, "blue", self.pawnRadius)
                    self.blue_team.add(pawn)
                    pawn.draw(self.screen)

                    # Mark the relevant square as not free
                    self.squares[pawn.square_number].free = False

    def initRedPawns(self):
        for row in range(6, 9):
            for col in range(1, self.board_size - 1):
                if (row + col) % 2 != 0:
                    pawn = Pawn(col, row, self.square_size, "red", self.pawnRadius)
                    self.red_team.add(pawn)
                    pawn.draw(self.screen)
                   
                    # Mark the relevant square as not free
                    self.squares[pawn.square_number].free = False

    def getSquareSize(self):
        return self.square_size
    
    def drawFrame(self):
        """"
        Draws the game board frame, including the inner and outer frames, as well as row and column labels.
        """
        frame_color = constants.WHITE
        frame_thickness = 5

        self.drawInnerFrame(frame_color, frame_thickness)
        self.drawOuterFrame(frame_color, frame_thickness)
        self.labelRowsAndColumns(frame_color)

    def drawInnerFrame(self, color, thickness):
        inner_frame_rect = pygame.Rect(0.1 * self.board_width - 5, 0.1 * self.board_height - 5, 0.8 * self.board_width + 10, 0.8 * self.board_height + 10)
        pygame.draw.rect(self.screen, color, inner_frame_rect, thickness)

    def drawOuterFrame(self, color, thickness):
        outer_frame_rect = pygame.Rect(0, 0, self.board_width, self.board_height)
        pygame.draw.rect(self.screen, color, outer_frame_rect, thickness)

    def labelRowsAndColumns(self, color):
        font = pygame.font.SysFont('Arial', 30)
        
        for i in range(1, self.board_size - 1):
            row_label = font.render(str(self.board_size - i - 1), True, color)
            row_rect1, row_rect2 = row_label.get_rect(), row_label.get_rect()
            row_rect1.center, row_rect2.center = (self.square_size // 2, (i + 0.5) * self.square_size), (self.board_width - (self.square_size // 2), (i + 0.5) * self.square_size)
            self.screen.blit(row_label, row_rect1)
            self.screen.blit(row_label, row_rect2)

            col_label = font.render(chr(ord('A') + i - 1), True, color)
            col_rect1, col_rect2 = col_label.get_rect(), col_label.get_rect()
            col_rect1.center, col_rect2.center = ((i + 0.5) * self.square_size, self.board_height - self.square_size // 2), ((i + 0.5) * self.square_size, self.board_height - (self.board_height - self.square_size // 2))
            self.screen.blit(col_label, col_rect1)
            self.screen.blit(col_label, col_rect2)

    def draw(self):
        """"
        Draws the game board frame, the board itself and pawns
        """
        self.drawFrame()
        for square in self.squares[1:]:
            square.draw(self.screen)
        for pawn in self.blue_team:
            pawn.draw(self.screen)
        for pawn in self.red_team:
            pawn.draw(self.screen)

    def getOccupyingPawn(self, square_number):
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

    def deletePawn(self, pawn):
        square_number = pawn.square_number

        # Draw a square on top of the pawn 
        self.squares[square_number].draw(self.screen)

        self.squares[square_number].free = True
        if pawn.color_type == "red": 
            self.red_team.remove(pawn)
        else: 
            self.blue_team.remove(pawn)
        del pawn

    def addPawn(self, pawn):
        square_number = pawn.square_number
        self.squares[square_number].free = False
        if pawn.color_type == "red": 
            self.red_team.add(pawn)
        else: 
            self.blue_team.add(pawn)

    def isSquareValidAndFree(self, square_number):
        return Square.isValidSquareNumber(square_number) and self.squares[square_number].free
    
    def promotePawn(self, pawn):
        copy = pawn
        self.deletePawn(pawn)
        queen = Queen(copy.col, copy.row, self.square_size, copy.color_type, self.pawnRadius, self.screen)
        self.addPawn(queen)

    def deserialize(self):
        board_array = np.zeros((8, 8), dtype=int)
        for row in range(8):
            for col in range(8):
                if (row % 2) == (col % 2):
                    # Unusable square
                    continue 
                else:
                    square_number = Square.computeSquareNumber(row + 1, col + 1)
                    pawn = self.getOccupyingPawn(square_number)
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
        start_row, start_col = Square.computeRowAndCol(start_square_number)
        end_row, end_col = Square.computeRowAndCol(end_square_number)

        prev_pawn_value = deserialized_board[start_row - 1, start_col - 1]
        cur_pawn_value = Board.getDeserializedPawnValue(prev_pawn_value, end_square_number)

        # Update move on the board
        if is_capture:
            capture_square_number = Pawn.computeOpponentSquareNumber(start_square_number, end_square_number)
            capture_row, capture_col = Square.computeRowAndCol(capture_square_number)
            deserialized_board[capture_row - 1, capture_col - 1] = 0
        deserialized_board[start_row - 1, start_col - 1] = 0
        deserialized_board[end_row - 1, end_col - 1] = cur_pawn_value

        return deserialized_board

    def getDeserializedPawnValue(prev_pawn_value, end_square_number):
        # end_square is a promotion square
        if (prev_pawn_value == 1 and 57 <= end_square_number <= 64) or \
            (prev_pawn_value == -1 and 1 <= end_square_number <= 8):
            new_pawn_value = 3 * prev_pawn_value
            return new_pawn_value
        
        return prev_pawn_value