import os
import pygame
import constants


class UI:
    def __init__(self, board):
        pygame.init()
        self.board = self.board = board

        self.screen_width = self.board.width + 3 * self.board.square_size
        self.screen_height = self.board.height + 2 * self.board.square_size
        # Create a pygame surface
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Checkers")

        # Define parameters
        self.board_frame_x = self.board.x
        self.board_frame_y = self.board.y
        self.board_frame_width = self.board.width
        self.board_frame_height = self.board.height
        self.top_button_component_x = 0
        self.top_button_component_y = 0
        self.top_button_component_width = self.board.width
        self.top_button_component_height = self.board.square_size
        self.bottom_button_component_x = 0
        self.bottom_button_component_y = self.board.height + self.board.square_size
        self.right_button_component_x = self.board.width
        self.right_button_component_y = 0
        self.right_button_component_width = 3 * self.board.square_size
        self.right_button_component_height = self.board.height + 2 * self.board.square_size

        # Load the button component textures
        self.horizontal_button_component_texture = (
            self.load_button_component_texture('horizontal_button_component_texture.png',
                                               self.top_button_component_width,
                                               self.top_button_component_height))
        self.vertical_button_component_texture = (
            self.load_button_component_texture('vertical_button_component_texture.png',
                                               self.right_button_component_width,
                                               self.right_button_component_height))

    @staticmethod
    def get_file_path(filename):
        """
        Get the full path to the file based on the provided filename.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_directory, filename)
        return full_path

    def load_button_component_texture(self, button_component_file_name, width, height):
        file_path = self.get_file_path(button_component_file_name)
        button_component_image = pygame.image.load(file_path)

        # Scale the board texture to fit the board size
        button_component_size = (width, height)
        button_component_texture = pygame.transform.scale(button_component_image, button_component_size)

        return button_component_texture

    def draw(self):
        self.draw_board(self.board.texture, self.board.x, self.board.y)
        self.draw_board_frame(self.screen, frame_thickness=3, x=self.board_frame_x, y=self.board_frame_y,
                              width=self.board_frame_width, height=self.board_frame_height)
        # Draw the top button component
        self.draw_button_component(self.horizontal_button_component_texture, self.top_button_component_x,
                                   self.top_button_component_y)
        # Draw the bottom button component
        self.draw_button_component(self.horizontal_button_component_texture, self.bottom_button_component_x,
                                   self.bottom_button_component_y)
        # Draw the right button component
        self.draw_button_component(self.vertical_button_component_texture, self.right_button_component_x,
                                   self.right_button_component_y)
        # Draw the pawns
        self.draw_pawns()

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

    def draw_button_component(self, button_component_texture, x, y):
        self.screen.blit(button_component_texture, (x, y))

    def draw_pawns(self):
        for pawn in self.board.white_team | self.board.black_team:
            self.draw_pawn(pawn)

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
