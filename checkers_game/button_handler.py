from button import Button


class ButtonHandler:

    def __init__(self, board):
        self.board = board
        self.board_square_size = self.board.square_size
        self.screen_width = self.board.width + 4.5 * self.board.square_size
        self.screen_height = self.board.height + 2 * self.board.square_size

        self.button_size = (3.5 * self.board_square_size, 0.6 * self.board_square_size)
        self.general_button_size = (self.button_size[0], self.button_size[1] * 1.5)
        self.message_text_pos = (self.screen_width // 2 - self.button_size[0] * 0.5,
                                 self.screen_height // 2 - self.button_size[1] * 4)

        self.in_game_buttons = {}
        self.general_buttons = {}

        self.init_in_game_buttons()
        self.init_general_buttons()

    def init_in_game_buttons(self):
        player_rubric_size = (2.5 * self.board_square_size, 0.6 * self.board_square_size)

        # initialize the player rubrics and scorekeepers
        self.in_game_buttons["player_one"] = Button('button_texture.png',
                                                    player_rubric_size,
                                                    (0.5 * self.board_square_size, 0.2 * self.board_square_size),
                                                    "PLAYER 1")
        self.in_game_buttons["player_two"] = Button('button_texture.png',
                                                    player_rubric_size,
                                                    (0.5 * self.board_square_size,
                                                     self.board.height + 1.2 * self.board_square_size),
                                                    "PLAYER 2")

        score_keeper_rubric_size = (0.5 * self.board_square_size, player_rubric_size[1])
        self.in_game_buttons["player_one_score_keeper"] = Button('button_texture.png',
                                                                 score_keeper_rubric_size,
                                                                 (self.in_game_buttons["player_one"].pos[0] +
                                                                  player_rubric_size[0] +
                                                                  0.5 * self.board_square_size,
                                                                  self.in_game_buttons["player_one"].pos[1]),
                                                                 "12")
        self.in_game_buttons["player_two_score_keeper"] = Button('button_texture.png',
                                                                 score_keeper_rubric_size,
                                                                 (self.in_game_buttons["player_two"].pos[0] +
                                                                  player_rubric_size[0] +
                                                                  0.5 * self.board_square_size,
                                                                  self.in_game_buttons["player_two"].pos[1]),
                                                                 "12")

        # Initialize the in-game buttons
        self.in_game_buttons["offer_draw"] = Button('button_texture.png', self.button_size,
                                                    (self.board.pos[0] +
                                                     self.board.width + 0.25 * self.board_square_size,
                                                     self.board.pos[1] + 0.25 * self.board_square_size),
                                                    "OFFER DRAW")
        self.in_game_buttons["resign"] = Button('button_texture.png', self.button_size,
                                                (self.board.pos[0] +
                                                 self.board.width + 0.25 * self.board_square_size,
                                                 self.in_game_buttons["offer_draw"].pos[1] +
                                                 self.board_square_size),
                                                "RESIGN")
        self.in_game_buttons["options"] = Button('button_texture.png', self.button_size,
                                                 (self.board.pos[0] +
                                                  self.board.width + 0.25 * self.board_square_size,
                                                  self.in_game_buttons["resign"].pos[1] +
                                                  self.board_square_size),
                                                 "OPTIONS")

    def init_general_buttons(self):
        self.general_buttons["rematch"] = Button('button_texture.png', self.general_button_size,
                                                 (self.screen_width // 2 - self.button_size[0] * 1.2,
                                                  self.screen_height // 2 - self.button_size[1] * 0.75),
                                                 "REMATCH")
        self.general_buttons["quit"] = Button('button_texture.png', self.general_button_size,
                                              (self.screen_width // 2 + self.button_size[0] * 0.2,
                                               self.screen_height // 2 - self.button_size[1] * 0.75),
                                              "QUIT")
        self.general_buttons["yes_resign"] = Button('button_texture.png', self.general_button_size,
                                                    (self.general_buttons["rematch"].pos[0],
                                                     self.general_buttons["rematch"].pos[1]),
                                                    "YES")
        self.general_buttons["no_resign"] = Button('button_texture.png', self.general_button_size,
                                                   (self.general_buttons["quit"].pos[0],
                                                    self.general_buttons["quit"].pos[1]),
                                                   "NO")
        self.general_buttons["easy"] = Button('button_texture.png', self.general_button_size,
                                              (self.screen_width // 2 - self.button_size[0] * 1.6,
                                               self.screen_height // 2 - self.button_size[1] * 0.75),
                                              "EASY")
        self.general_buttons["medium"] = Button('button_texture.png', self.general_button_size,
                                                (self.screen_width // 2 - self.button_size[0] * 0.5,
                                                 self.screen_height // 2 - self.button_size[1] * 0.75),
                                                "MEDIUM")
        self.general_buttons["hard"] = Button('button_texture.png', self.general_button_size,
                                              (self.screen_width // 2 + self.button_size[0] * 0.6,
                                               self.screen_height // 2 - self.button_size[1] * 0.75),
                                              "HARD")
        self.general_buttons["change_difficulty"] = Button('button_texture.png', self.general_button_size,
                                                           (self.general_buttons["rematch"].pos[0],
                                                            self.general_buttons["rematch"].pos[1]),
                                                           "CHANGE DIFFICULTY")
        self.general_buttons["game_rules"] = Button('button_texture.png', self.general_button_size,
                                                    (self.general_buttons["quit"].pos[0],
                                                     self.general_buttons["quit"].pos[1]),
                                                    "GAME RULES")
        self.general_buttons["got_it_draw"] = Button('button_texture.png', self.general_button_size,
                                                     (self.general_buttons["medium"].pos[0],
                                                      self.general_buttons["medium"].pos[1]),
                                                     "GOT IT")
        self.general_buttons["got_it_game_rules"] = Button('button_texture.png', self.general_button_size,
                                                           (self.general_buttons["medium"].pos[0],
                                                            self.screen_height * 0.825),
                                                           "GOT IT")

    def get_pressed_button(self, mouse_pos):
        if self.is_click_on_in_game_button(mouse_pos, "offer_draw"):
            return "OFFER DRAW"
        elif self.is_click_on_in_game_button(mouse_pos, "resign"):
            return "RESIGN"
        elif self.is_click_on_in_game_button(mouse_pos, "options"):
            return "OPTIONS"
        else:
            return None

    def is_click_on_in_game_button(self, mouse_pos, button_name):
        x, y = self.in_game_buttons[button_name].pos
        width, height = self.in_game_buttons[button_name].size
        return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

    def is_click_on_general_button(self, mouse_pos, button_name):
        x, y = self.general_buttons[button_name].pos
        width, height = self.general_buttons[button_name].size
        return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height
