import copy
import matplotlib.pyplot as plt
import numpy as np
from datamodels.types import Character, LedMatrix
from data.fonts import default_font
from src.algs import key_to_character


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



# example display
if __name__ == "__main__":
    # create background of different colors
    bit_depth = 255
    height = 32
    width = 64

    background = np.random.randint(
        bit_depth * 0.9,
        bit_depth,
        (height, width, 3),
    )

    led_matrix = LedMatrix(
        pixels=copy.deepcopy(background),
        bit_depth=bit_depth,
        height_px=height,
        width_px=width,
    )

    lines = ["Central SQ.", "Inbound 12", "Outbound 12"]
    row_index = 0
    for line in lines:
        col_index = 0
        for character_key in line:
            character = key_to_character(default_font, character_key)
            led_matrix = draw_character(
                led_matrix,
                character,
                row_index + 1 if character.dropdown else row_index,
                col_index,
            )
            col_index += character.width_px + 1
        row_index += default_font.height_px + 1
    display_matrix(led_matrix)

    # clear the background
    led_matrix.pixels = copy.deepcopy(background)

    col_index = 0
    row_index = 0

    # print every character of `default_cont`, making a new line/page if needed
    for character in default_font.characters:
        # new row is needed for this character
        if col_index + character.width_px >= led_matrix.width_px:
            col_index = 0
            row_index += default_font.height_px + 1

        # new page is needed for this character
        if row_index + default_font.height_px >= led_matrix.height_px + 5:
            # dispaly the page before clearing
            display_matrix(led_matrix)
            # clear the page
            row_index = 0
            col_index = 0
            led_matrix.pixels = copy.deepcopy(background)

        led_matrix = draw_character(
            led_matrix,
            character,
            row_index + 1 if character.dropdown else row_index,
            col_index,
        )

        # move imaginary curser over to the start of the next character
        col_index += character.width_px + 1

    display_matrix(led_matrix)
