import copy
import src.data.state as state

from src.data.fonts import default_font
from src.algs import draw_character, key_to_character
from typing import List, Tuple

import pygame


class Simulate:
    width, height = (state.width, state.height)

    # Size of each pixel
    scale = 15
    radius = scale // 2

    # Create the Pygame screen, adding extra space for the offset
    screen = pygame.display.set_mode((width * scale + scale, height * scale + scale))

    def display_matrix(self, pixels: List[List[Tuple[int, int, int]]]) -> None:
        """Given a led matrix, display it to the user using pygame"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Fill the screen with black
        self.screen.fill((0, 0, 0))

        # Draw each pixel
        for y, row in enumerate(pixels):
            for x, color in enumerate(row):
                # Add the offset of radius to x and y coordinates
                pygame.draw.circle(
                    self.screen,
                    color,
                    ((x * self.scale + self.radius), (y * self.scale + self.radius)),
                    self.radius,
                )

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    # example code that will not be run, unless specifically chosen

    my_simulation = Simulate()

    lines = ["Central SQ.", "Inbound 12", "Outbound 12"]
    row_index = 0
    for line in lines:
        col_index = 0
        for character_key in line:
            character = key_to_character(default_font, character_key)
            state.led_matrix = draw_character(
                state.led_matrix,
                character,
                row_index + 1 if character.dropdown else row_index,
                col_index,
            )
            col_index += character.width_px + 1
        row_index += default_font.height_px + 1

    my_simulation.display_matrix(state.led_matrix)

    # clear the background
    state.led_matrix.pixels = copy.deepcopy(state.background)

    col_index = 0
    row_index = 0

    # print every character of `default_cont`, making a new line/page if needed
    for character in default_font.characters:
        # a new row is needed for this character
        if col_index + character.width_px >= state.width:
            col_index = 0
            row_index += default_font.height_px + 1

        # a new page is needed for this character
        if row_index + default_font.height_px >= state.height + 5:
            # disiplay the page before clearing
            my_simulation.display_matrix(state.led_matrix)

            # clear the page
            row_index = 0
            col_index = 0
            state.led_matrix.pixels = copy.deepcopy(state.background)

        state.led_matrix = draw_character(
            state.led_matrix,
            character,
            row_index + 1 if character.dropdown else row_index,
            col_index,
        )

        # move imaginary curser over to the start of the next character
        col_index += character.width_px + 1

    my_simulation.display_matrix(state.led_matrix)
