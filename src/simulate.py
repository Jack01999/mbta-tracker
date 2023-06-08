import copy
import matplotlib.pyplot as plt
import numpy as np
from datamodels.types import Character, Font, Matrix
from data.fonts import default_font


# TODO store a map rather than searching for each letter
def get_character(
    font: Font,
    key: str,
) -> Character:
    for character in font.characters:
        if character.character_key == key:
            return character
    raise ValueError


def display_matrix(matrix: Matrix) -> None:
    """Given a led matrix, display it to the user using matplotlib
    using matplotlib"""
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


def draw_character(
    matrix: Matrix,
    character: Character,
    row_start: int,
    col_start: int,
) -> Matrix:
    """Draw on, and return an led matrix. `row_start` and  `col__start`
    both start at zero and begin in the upper left corner"""

    row = row_start
    for px_row in character.character_value:
        col = col_start
        for i in range(character.width_px - 1, -1, -1):
            bit = (px_row >> i) & 1
            if bit:
                # dot color, can make anything
                matrix.pixels[row][col] = (230, 10, 0)

            col += 1
        row += 1

    return matrix


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

    led_matrix = Matrix(
        pixels=copy.deepcopy(background),
        bit_depth=bit_depth,
        height_px=height,
        width_px=width,
    )

    lines = ["Central Sq ", "In  1,2,3", "Out 1,2,3"]
    row_index = 0
    for line in lines:
        col_index = 0
        for char_key in line:
            char = get_character(default_font, char_key)

            led_matrix = draw_character(
                led_matrix,
                char,
                row_index + 1 if char.dropdown else row_index,
                col_index,
            )
            col_index += char.width_px + 1
        row_index += default_font.height_px + 1
    display_matrix(led_matrix)

    # clear the background
    led_matrix.pixels = copy.deepcopy(background)

    col_index = 0
    row_index = 0

    # print every character of `default_cont`, making a new line/page if needed
    for character in default_font.characters:
        if character in [" "]:
            continue

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
