import os
import sys
import pygame
import constants
from button_handler import ButtonHandler
from button_component import ButtonComponent


class UI:
    def __init__(self, board):
        pygame.init()
        self.board = self.board = board
        self.button_handler = ButtonHandler(board)

        self.screen_width = self.board.width + 4.5 * self.board.square_size
        self.screen_height = self.board.height + 2 * self.board.square_size
        # Create a pygame surface
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Checkers")

        # Define parameters
        self.board_frame_pos = (self.board.pos[0], self.board.pos[1])
        self.board_frame_size = (self.board.width, self.board.height)

        # Define button components
        self.button_components = {}
        self.init_button_components()
        self.initial_background = ButtonComponent('initial_background_texture.png',
                                                  (self.screen_width, self.screen_height), (0, 0))

        self.in_game_font = self.load_font('DragonHunter_font.otf')
        self.general_font = self.load_font('DragonHunter_font.otf', font_size=48)
        self.options_font = self.load_font('DragonHunter_font.otf', font_size=25)
        self.rendered_game_rules = []

    def init_button_components(self):
        self.button_components["top"] = ButtonComponent('horizontal_button_component_texture.png',
                                                        (self.board.width, self.board.square_size),
                                                        (0.5 * self.board.square_size, 0))
        self.button_components["bottom"] = ButtonComponent('horizontal_button_component_texture.png',
                                                           (self.board.width, self.board.square_size),
                                                           (0.5 * self.board.square_size, self.board.height +
                                                            self.board.square_size))
        self.button_components["right"] = ButtonComponent('vertical_button_component_texture.png',
                                                          (self.screen_width - self.board.width -
                                                           0.5 * self.board.square_size, self.screen_height),
                                                          (self.board.width + 0.5 * self.board.square_size, 0))
        self.button_components["left"] = ButtonComponent('vertical_button_component_texture.png',
                                                         (0.5 * self.board.square_size, self.screen_height),
                                                         (0, 0))

    @staticmethod
    def get_file_path(filename):
        """
        Get the full path to the file based on the provided filename.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_directory, filename)
        return full_path

    def load_font(self, font_file_name, font_size=35):
        font_path = self.get_file_path(font_file_name)
        font = pygame.font.Font(font_path, font_size)
        return font

    def display_game_rules(self, first_time=True):
        if first_time:
            self.init_game_rules_rendered_text()

        # Define y-position to locate the text vertically
        y_position = 50

        self.draw_background()

        # Draw each line on the screen
        for line in self.rendered_game_rules:
            text_rect = line.get_rect(topleft=(50, y_position))
            self.screen.blit(line, text_rect.topleft)
            y_position += int(line.get_height() * 1.4)  # Move to the next line

        # Draw the "GOT IT" button
        self.draw_general_button(self.button_handler.general_buttons["got_it_game_rules"], self.general_font)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    if self.button_handler.is_click_on_general_button(mouse_pos, "got_it_game_rules"):
                        return

    def init_game_rules_rendered_text(self):
        game_rules_file_path = self.get_file_path("game_rules.txt")
        with open(game_rules_file_path, 'rt') as file:
            rules_content = file.read()

        font_size_first_line = 40
        font_size_default = 22

        lines = rules_content.split('\n')  # Split the text into lines

        # Render each line separately
        for i, line in enumerate(lines):
            # Use a larger font size for the first line
            current_font_size = font_size_first_line if i == 0 else font_size_default
            line_font = self.load_font('DragonHunter_font.otf', font_size=current_font_size)
            rendered_line = self.render_text(line_font, line, text_color=constants.WHITE)
            self.rendered_game_rules.append(rendered_line)

    def display_end_of_game(self, outcome):
        self.draw_background()

        # Draw the outcome announcement
        if outcome == "lost":
            end_game_text = "YOU LOSE !"
        elif outcome == "won":
            end_game_text = "YOU WIN !"
        else:
            end_game_text = "DRAW ACCEPTED!"

        font = self.load_font('DragonHunter_font.otf', font_size=65)
        self.draw_centered_text(end_game_text, self.button_handler.message_text_pos[0],
                                self.button_handler.message_text_pos[1], self.button_handler.button_size[0],
                                font, constants.WHITE)

        # Draw the next button possibilities
        self.draw_general_button(self.button_handler.general_buttons["rematch"], self.general_font)
        self.draw_general_button(self.button_handler.general_buttons["quit"], self.general_font)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    if self.button_handler.is_click_on_general_button(mouse_pos, "rematch"):
                        return "REMATCH"
                    elif self.button_handler.is_click_on_general_button(mouse_pos, "quit"):
                        return "QUIT"
                    else:
                        continue

    def display_confirm_resign(self):
        self.draw_background()

        # Draw the resignation confirmation text
        font = self.load_font('DragonHunter_font.otf', font_size=43)
        self.draw_centered_text("ARE YOU SURE YOU WANT TO RESIGN ?", self.button_handler.message_text_pos[0],
                                self.button_handler.message_text_pos[1], self.button_handler.button_size[0],
                                font, constants.WHITE)

        # Draw the confirmation button possibilities
        self.draw_general_button(self.button_handler.general_buttons["yes_resign"], self.general_font)
        self.draw_general_button(self.button_handler.general_buttons["no_resign"], self.general_font)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    if self.button_handler.is_click_on_general_button(mouse_pos, "yes_resign"):
                        return True
                    elif self.button_handler.is_click_on_general_button(mouse_pos, "no_resign"):
                        return False
                    else:
                        continue

    def display_choose_difficulty(self):
        self.draw_background()

        # Draw the choose difficulty text
        font = self.load_font('DragonHunter_font.otf', font_size=65)
        self.draw_centered_text("CHOOSE DIFFICULTY", self.button_handler.message_text_pos[0],
                                self.button_handler.message_text_pos[1], self.button_handler.button_size[0],
                                font, constants.WHITE)

        # Draw the difficulty button possibilities
        self.draw_general_button(self.button_handler.general_buttons["easy"], self.general_font)
        self.draw_general_button(self.button_handler.general_buttons["medium"], self.general_font)
        self.draw_general_button(self.button_handler.general_buttons["hard"], self.general_font)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    if self.button_handler.is_click_on_general_button(mouse_pos, "easy"):
                        return "EASY"
                    elif self.button_handler.is_click_on_general_button(mouse_pos, "medium"):
                        return "MEDIUM"
                    elif self.button_handler.is_click_on_general_button(mouse_pos, "hard"):
                        return "HARD"
                    else:
                        continue

    def display_draw_rejected(self):
        self.draw_background()

        # Draw the outcome announcement
        font = self.load_font('DragonHunter_font.otf', font_size=65)
        self.draw_centered_text("DRAW REJECTED", self.button_handler.message_text_pos[0],
                                self.button_handler.message_text_pos[1], self.button_handler.button_size[0],
                                font, constants.WHITE)

        # Draw the got it button
        self.draw_general_button(self.button_handler.general_buttons["got_it_draw"], self.general_font)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    if self.button_handler.is_click_on_general_button(mouse_pos, "got_it_draw"):
                        return
                    else:
                        continue

    def display_options(self):
        self.draw_background()

        # Draw the options text
        font = self.load_font('DragonHunter_font.otf', font_size=65)
        self.draw_centered_text("OPTIONS", self.button_handler.message_text_pos[0],
                                self.button_handler.message_text_pos[1], self.button_handler.button_size[0],
                                font, constants.WHITE)

        # Draw the difficulty button possibilities
        self.draw_general_button(self.button_handler.general_buttons["change_difficulty"], self.options_font)
        self.draw_general_button(self.button_handler.general_buttons["game_rules"], self.options_font)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    if self.button_handler.is_click_on_general_button(mouse_pos, "change_difficulty"):
                        return "CHANGE DIFFICULTY"
                    elif self.button_handler.is_click_on_general_button(mouse_pos, "game_rules"):
                        return "GAME RULES"
                    else:
                        continue

    def draw(self):
        # Draw the board and its frame
        self.draw_board(self.board.texture, self.board.pos[0], self.board.pos[1])
        self.draw_board_frame(self.screen, frame_thickness=3, x=self.board_frame_pos[0], y=self.board_frame_pos[1],
                              width=self.board_frame_size[0], height=self.board_frame_size[1])

        self.draw_button_components()
        self.draw_pawns()
        self.draw_squares()
        self.draw_in_game_buttons()

    def draw_background(self):
        self.screen.blit(self.initial_background.texture, self.initial_background.pos)

    def draw_board(self, board_texture, x, y):
        self.screen.blit(board_texture, (x, y))

    @staticmethod
    def draw_board_frame(screen, frame_thickness, x, y, width, height):
        """
        Draws the game board frame, including the inner and outer frames, as well as row and column labels.
        """
        frame_color = constants.WHITE
        inner_frame_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, frame_color, inner_frame_rect, frame_thickness)

    def draw_button_components(self):
        for button_component in self.button_components.values():
            self.screen.blit(button_component.texture, button_component.pos)

    def draw_pawns(self):
        for pawn in self.board.white_team | self.board.black_team:
            self.draw_pawn(pawn)
            if pawn.highlighted:
                self.draw_highlight_pawn(pawn.center, pawn.radius)
            elif pawn.selected:
                self.draw_select_pawn(pawn.center, pawn.radius)

    def draw_squares(self):
        for square in self.board.squares:
            if square.selected:
                self.draw_select_square(square.get_center(), self.board.pawn_radius)

    def draw_select_square(self, center, pawn_radius):
        pygame.draw.circle(self.screen, constants.SELECT_COLOR, center, pawn_radius, 4)

    def draw_select_pawn(self, center, radius):
        pygame.draw.circle(self.screen, constants.SELECT_COLOR, center, radius, 4)

    def draw_highlight_pawn(self, center, radius):
        pygame.draw.circle(self.screen, constants.HIGHLIGHT_COLOR, center, radius, 4)

    def draw_pawn(self, pawn):
        x, y = pawn.get_x_and_y()
        self.screen.blit(pawn.texture, (x, y))

        if pawn.queen:
            crown_x, crown_y = pawn.get_crown_x_and_y()
            # Draw the crown image on top of the pawn
            self.screen.blit(pawn.crown_texture, (crown_x, crown_y))

    def draw_in_game_buttons(self):
        for button_name, button in self.button_handler.in_game_buttons.items():
            if button_name == "player_one_score_keeper":
                button.text = str(len(self.board.white_team))
            elif button_name == "player_two_score_keeper":
                button.text = str(len(self.board.black_team))

            self.draw_button(button)

    def draw_button(self, button):
        self.screen.blit(button.texture, button.pos)
        self.draw_centered_text(button.text, button.pos[0], button.pos[1], button.size[0], self.in_game_font)

    def draw_general_button(self, button, font):
        x, y = button.pos
        self.screen.blit(button.texture, (x, y))
        y += button.size[1] * 0.25
        width = button.size[0]
        self.draw_centered_text(button.text, x, y, width, font, text_color=constants.BUTTON_TEXT_COLOR)

    def draw_centered_text(self, text, dest_x, dest_y, max_width, font, text_color=constants.TEXT_COLOR):
        rendered_text = self.render_text(font, text, text_color)

        # Get the rect object of the rendered text
        text_rect = rendered_text.get_rect()

        # Center the text around the destination point
        self.center_text(text_rect, dest_x, dest_y, max_width)

        # Blit the text to the screen
        self.screen.blit(rendered_text, text_rect.topleft)

    @staticmethod
    def render_text(font, text, text_color=constants.TEXT_COLOR):
        return font.render(text, True, text_color)

    def center_text(self, text_rect, dest_x, dest_y, max_width):
        text_rect.center = (dest_x + max_width // 2, dest_y +
                            0.9 * self.button_handler.in_game_buttons["player_one"].size[1] // 2)
