import sys
import pygame
from board import Board
from move_handler import MoveHandler
from agent_move_handler import AgentMoveHandler
import constants

pygame.init()

# Initialize the game board and display
board = Board(board_side_length=constants.BOARD_SIDE_LENGTH)
board.draw()
pygame.display.flip()

move_handler = MoveHandler()
agent_move_handler = AgentMoveHandler()

run = True
pressed = False  # Indicates whether next pawn to move already chosen

# Main game loop
while run:

    if move_handler.is_losing_team(board, board.red_team):
        print("Game Over!!! Blue wins")
        pygame.quit()
        sys.exit()

    while move_handler.is_player_turn:
        if not pressed:
            move_handler.initialize_new_move(board)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if not pressed:
                    # first press
                    if move_handler.is_legal_press(board, mouse_pos, is_first_press=True):
                        pressed = True
                else:
                    # Second press
                    if move_handler.is_legal_press(board, mouse_pos, is_first_press=False):
                        pressed = False

    pygame.display.flip()
    
    if move_handler.is_losing_team(board, board.blue_team):
        print("Game Over!!! Red wins")
        pygame.quit()
        sys.exit()

    agent_move_handler.play(board)
    move_handler.is_player_turn = True

pygame.quit()
sys.exit()
