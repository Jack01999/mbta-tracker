import copy
import matplotlib.pyplot as plt
import numpy as np
import src.data.state as state
from src.datamodels.types import LedMatrix
from src.data.fonts import default_font
from src.algs import draw_character, key_to_character


def display_matrix(matrix: LedMatrix) -> None:
    """Given a led matrix, display it to the user using matplotlib"""
    y, x = np.indices(matrix.pixels.shape[:2])
    #     x, y = matrix.width, matrix.height

    # flatten tuples into (r, g, b)
    colors = matrix.pixels.reshape(-1, 3) / matrix.bit_depth

    _, ax = plt.subplots(figsize=(8, 4), dpi=150)

    ax.set_xlim(-1, matrix.width_px)
    ax.set_ylim(-1, matrix.height_px)

    ax.scatter(x.ravel(), y.ravel(), c=colors, s=12)

    # led matrix starts at the top, plots start at the bottom
    ax.invert_yaxis()

    plt.show()



if __name__ == "__main__":
    # example code that will not be run, unless specifically chosen

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
    display_matrix(state.led_matrix)

    # clear the background
    state.led_matrix.pixels = copy.deepcopy(state.background)

    col_index = 0
    row_index = 0

    # print every character of `default_cont`, making a new line/page if needed
    for character in default_font.characters:

        # a new row is needed for this character
        if col_index + character.width_px >= state.led_matrix.width_px:
            col_index = 0
            row_index += default_font.height_px + 1

        # a new page is needed for this character
        if row_index + default_font.height_px >= state.led_matrix.height_px + 5:
            
            # disiplay the page before clearing
            display_matrix(state.led_matrix)
            
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

    display_matrix(state.led_matrix)
