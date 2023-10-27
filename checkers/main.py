import sys
import pygame
from board import Board
from move_handler import MoveHandler
from agent_move_handler import AgentMoveHandler

pygame.init()

board = Board(960, 720)
square_size = board.square_size

move_handler = MoveHandler()
agent_move_handler = AgentMoveHandler()

run = True
pressed = False # indicates wheter next pawn to move already chosen
pygame.time.delay(1000)

# main game loop
while run:

    if move_handler.is_game_over(board, board.blue_team):
    ########## NEEDS MODIFICATION ##########
        print("Game Over!!! Red wins")
        pygame.quit()
        sys.exit() 
    ########## NEEDS MODIFICATION ##########

    pygame.time.delay(1000)
    # Make agent play a move
    agent_move_handler.play(board)
    move_handler.is_player_turn = True

    if move_handler.is_game_over(board, board.red_team):
    ########## NEEDS MODIFICATION ##########
        print("Game Over!!! Blue wins")
        pygame.quit()
        sys.exit() 
    ########## NEEDS MODIFICATION ##########
        
    while move_handler.is_player_turn:
        if not pressed:
            move_handler.initialize_new_move(board)
        # event handler

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
   
pygame.quit()
sys.exit() 