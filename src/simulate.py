import matplotlib.pyplot as plt
import numpy as np
from datamodels.types import Matrix
from data.fonts import default_font

def display_matrix(matrix: Matrix) -> None:
    """Given a led matrix, display it to the user using matplotlib
    using matplotlib"""
    y, x = np.indices(matrix.pixels.shape[:2])
    #     x, y = matrix.width, matrix.height

    # flatten tuples into (r, g, b)
    colors = matrix.pixels.reshape(-1, 3) / matrix.bit_depth

    _, ax = plt.subplots(figsize=(8, 4), dpi=150)

    ax.set_xlim(-1, matrix.width)
    ax.set_ylim(-1, matrix.height)

    ax.scatter(x.ravel(), y.ravel(), c=colors, s=12)

    # led matrix starts at the top, plots start at the bottom
    ax.invert_yaxis()

    plt.show()


def draw_letter(
    matrix: Matrix,
    letter: str,
    row_start: int,
    col_start: int,
) -> Matrix:
    """Draw on, and return an led matrix. `row_start` and  `col__start`
    both start at zero and begin in the upper left corner"""

    row = row_start
    for horizontal in default_font.character_to_bytes[letter]:
        col = col_start
        for i in range(default_font.character_width - 1, -1, -1):
            bit = (horizontal >> i) & 1
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

    pixels = np.random.randint(
        200,
        255,
        (height, width, 3),
    )

    led_matrix = Matrix(
        pixels=pixels, bit_depth=bit_depth, height=height, width=width
    )

    col_index = 0
    row_index = 0

    # print the whole default_font
    for character in default_font.character_to_bytes.keys():
        if character in [" "]:
            continue

        # new row
        if col_index + default_font.character_width >= led_matrix.width:
            col_index = 0
            row_index += default_font.character_height + 1

        # new page
        if row_index + default_font.character_height >= led_matrix.height + 5:
            display_matrix(led_matrix)
            row_index = 0
            col_index = 0
            # clear the background
            led_matrix.pixels = np.random.randint(
                200, led_matrix.bit_depth, (led_matrix.height, led_matrix.width, 3)
            )

        led_matrix = draw_letter(
            led_matrix,
            character,
            row_index + 1 if character in default_font.dropdown_letters else row_index,
            col_index,
        )

        # next letter
        col_index += default_font.character_width + 1

    display_matrix(led_matrix)
