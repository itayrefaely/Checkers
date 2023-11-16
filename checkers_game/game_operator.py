import sys
import pygame

from board import Board
from ui import UI
import constants
from move_handler import MoveHandler
from agent_move_handler import AgentMoveHandler


class GameOperator:

    def __init__(self):
        self.board = Board(board_side_length=constants.BOARD_SIDE_LENGTH)
        self.ui = UI(self.board)
        self.ui.display_game_rules()
        self.game_difficulty = self.ui.display_choose_difficulty()
        self.ui.draw()

        pygame.display.flip()

        self.move_handler = MoveHandler()
        self.agent_move_handler = AgentMoveHandler(self.game_difficulty)

    def handle_button_press(self, pressed_button):
        if pressed_button == "OFFER DRAW":
            self.handle_offer_draw()
        elif pressed_button == "RESIGN":
            self.handle_resign()
        elif pressed_button == "OPTIONS":
            self.handle_options()

        self.ui.draw()

    def handle_offer_draw(self):
        draw_accepted = self.agent_move_handler.offer_draw(self.board)
        if draw_accepted:
            self.handle_end_of_game(outcome="draw")
        else:
            self.ui.display_draw_rejected()

    def handle_resign(self):
        confirmed_resign = self.ui.display_confirm_resign()
        if confirmed_resign:
            self.handle_end_of_game(outcome="lost")

    def handle_options(self):
        chosen_option = self.ui.display_options()
        if chosen_option == "CHANGE DIFFICULTY":
            self.handle_change_difficulty()
        elif chosen_option == "GAME RULES":
            self.ui.display_game_rules(first_time=False)

    def handle_change_difficulty(self):
        new_difficulty = self.ui.display_choose_difficulty()
        if new_difficulty != self.agent_move_handler.difficulty:
            self.agent_move_handler.set_difficulty(new_difficulty)

    def handle_end_of_game(self, outcome):
        second_pressed_button = self.ui.display_end_of_game(outcome)
        if second_pressed_button == "REMATCH":
            self.board.reset()
            self.move_handler.is_player_turn = True
            self.move_handler.pressed = False
            self.ui.draw()
        elif second_pressed_button == "QUIT":
            self.quit_game()

    def run(self):
        # Main game loop
        while True:
            if self.move_handler.is_losing_team(self.board, self.board.black_team):
                # Introduce a 1-second delay
                pygame.time.delay(500)
                self.handle_end_of_game(outcome="lost")

            while self.move_handler.is_player_turn:
                if not self.move_handler.pressed:
                    self.move_handler.initialize_new_move(self.board, self.ui)

                # Event handler
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_game()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = event.pos

                        pressed_button = self.ui.button_handler.get_pressed_button(mouse_pos)
                        if pressed_button:
                            self.handle_button_press(pressed_button)
                            pygame.display.flip()

                        elif not self.move_handler.pressed:
                            # first press
                            if self.move_handler.is_legal_press(self.board, mouse_pos, is_first_press=True,
                                                                ui=self.ui):
                                self.move_handler.pressed = True
                        else:
                            # Second press
                            if self.move_handler.is_legal_press(self.board, mouse_pos, is_first_press=False,
                                                                ui=self.ui):
                                self.move_handler.pressed = False

            pygame.display.flip()

            if self.move_handler.is_losing_team(self.board, self.board.white_team):
                # Introduce a half-second delay
                pygame.time.delay(500)
                self.handle_end_of_game(outcome="won")
            else:
                self.agent_move_handler.play(self.board, self.ui)
                self.move_handler.is_player_turn = True

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()
