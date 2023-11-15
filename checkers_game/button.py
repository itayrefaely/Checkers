import os
import pygame


class Button:

    def __init__(self, texture_file_name, texture_size, pos, text):
        self.texture = self.load_button_rubric_texture(texture_file_name, texture_size)
        self.pos = pos
        self.size = texture_size
        self.text = text

    @staticmethod
    def get_file_path(filename):
        """
        Get the full path to the file based on the provided filename.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_directory, filename)
        return full_path

    def load_button_rubric_texture(self, button_rubric_file_name, size):
        file_path = self.get_file_path(button_rubric_file_name)
        button_rubric_image = pygame.image.load(file_path)

        # Scale the board texture to fit the board size
        button_rubric_texture = pygame.transform.scale(button_rubric_image, size)

        return button_rubric_texture
