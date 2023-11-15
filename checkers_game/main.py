import sys
import pygame
from board import Board
from agent_move_handler import AgentMoveHandler
from move_handler import MoveHandler
from ui import UI
import constants


def handle_button_press():
    if pressed_button == "OFFER DRAW":
        draw_accepted = agent_move_handler.offer_draw(board)
        if draw_accepted:
            handle_end_of_game(outcome="draw")
        else:
            ui.display_draw_rejected()
            ui.draw()
    if pressed_button == "RESIGN":
        confirmed_resign = ui.display_confirm_resign()
        if confirmed_resign:
            handle_end_of_game(outcome="lost")
        else:
            ui.draw()
    elif pressed_button == "OPTIONS":
        chosen_option = ui.display_options()
        if chosen_option == "CHANGE DIFFICULTY":
            new_difficulty = ui.display_choose_difficulty()
            if new_difficulty != agent_move_handler.difficulty:
                agent_move_handler.set_difficulty(new_difficulty)
        elif chosen_option == "GAME RULES":
            ui.display_game_rules(first_time=False)

        ui.draw()


def handle_end_of_game(outcome):
    second_pressed_button = ui.display_end_of_game(outcome)
    if second_pressed_button == "REMATCH":
        board.reset()
        move_handler.is_player_turn = True
        move_handler.pressed = False
        ui.draw()
    elif second_pressed_button == "QUIT":
        quit_game()


def quit_game():
    pygame.quit()
    sys.exit()


pygame.init()

# Initialize the UI
board = Board(board_side_length=constants.BOARD_SIDE_LENGTH)
ui = UI(board)
ui.display_game_rules()
difficulty = ui.display_choose_difficulty()
ui.draw()
pygame.display.flip()

move_handler = MoveHandler()
agent_move_handler = AgentMoveHandler(difficulty)

run = True

# Main game loop
while run:

    if move_handler.is_losing_team(board, board.black_team):
        handle_end_of_game(outcome="lost")

    while move_handler.is_player_turn:
        if not move_handler.pressed:
            move_handler.initialize_new_move(board, ui)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                pressed_button = ui.button_handler.get_pressed_button(mouse_pos)
                if pressed_button:
                    handle_button_press()
                    pygame.display.flip()

                elif not move_handler.pressed:
                    # first press
                    if move_handler.is_legal_press(board, mouse_pos, is_first_press=True, ui=ui):
                        move_handler.pressed = True
                else:
                    # Second press
                    if move_handler.is_legal_press(board, mouse_pos, is_first_press=False, ui=ui):
                        move_handler.pressed = False

    pygame.display.flip()

    if move_handler.is_losing_team(board, board.white_team):
        handle_end_of_game(outcome="won")

    else:
        agent_move_handler.play(board, ui)
        move_handler.is_player_turn = True

quit_game()
