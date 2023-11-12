import sys
import pygame

from checkers_game.board import Board
from ui import UI
from move_handler import MoveHandler
from agent_move_handler import AgentMoveHandler
import constants

pygame.init()

# Initialize the UI
board = Board(board_side_length=constants.BOARD_SIDE_LENGTH)
ui = UI(board)
ui.draw()
pygame.display.flip()

move_handler = MoveHandler()
agent_move_handler = AgentMoveHandler()

run = True
pressed = False  # Indicates whether next pawn to move already chosen

# Main game loop
while run:

    if move_handler.is_losing_team(board, board.black_team):
        print("Game Over!!! White wins")
        pygame.quit()
        sys.exit()

    while move_handler.is_player_turn:
        if not pressed:
            move_handler.initialize_new_move(board, ui)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if not pressed:
                    # first press
                    if move_handler.is_legal_press(board, mouse_pos, is_first_press=True, ui=ui):
                        pressed = True
                else:
                    # Second press
                    if move_handler.is_legal_press(board, mouse_pos, is_first_press=False, ui=ui):
                        pressed = False

    pygame.display.flip()
    
    if move_handler.is_losing_team(board, board.white_team):
        print("Game Over!!! Black wins")
        pygame.quit()
        sys.exit()

    agent_move_handler.play(board, ui)
    move_handler.is_player_turn = True

pygame.quit()
sys.exit()
