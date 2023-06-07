import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

BIT_DEPTH = 255

MATRIX_WIDTH = 64
MATRIX_HEIGHT = 32

LETTER_WIDTH = 5
LETTER_HEIGHT = 7

font = {
    " ": [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
    "a": [0b00000, 0b01110, 0b00001, 0b00111, 0b01001, 0b00111, 0b00000],
    "b": [0b01000, 0b01000, 0b01110, 0b01001, 0b01001, 0b10110, 0b00000],
}


def display_matrix(matrix: List[List[Tuple[int, int, int]]]) -> None:
    """"""
    y, x = np.indices(matrix.shape[:2])

    # flatten tuples into (r, g, b)
    colors = matrix.reshape(-1, 3) / BIT_DEPTH

    _, ax = plt.subplots(figsize=(8, 4), dpi=150)

    ax.set_xlim(-1, MATRIX_WIDTH)
    ax.set_ylim(-1, MATRIX_HEIGHT)

    ax.scatter(x.ravel(), y.ravel(), c=colors, s=12)

    # led matrix starts at the top, plots start at the bottom
    ax.invert_yaxis()

    plt.show()


def draw_letter(
    matrix: List[List[Tuple[int, int, int]]],
    letter: str,
    row_start: int,
    col_start: int,
) -> List[List[Tuple[int, int, int]]]:
    row = row_start
    for horizontal in font[letter]:
        col = col_start
        for i in range(LETTER_WIDTH - 1, -1, -1):
            bit = (horizontal >> i) & 1
            if bit:
                # dot color, can make anything
                matrix[row][col] = (230, 10, 0)

            col += 1
        row += 1

    return matrix


# example display
if __name__ == "__main__":
    # create background of different colors
    led_matrix = np.random.randint(200, BIT_DEPTH, (MATRIX_HEIGHT, MATRIX_WIDTH, 3))

    led_matrix = draw_letter(led_matrix, "b", 0, 0)
    led_matrix = draw_letter(led_matrix, "b", 0, LETTER_WIDTH)
    led_matrix = draw_letter(led_matrix, "b", 0, LETTER_WIDTH * 2)
    led_matrix = draw_letter(led_matrix, "b", 0, LETTER_WIDTH * 3)
    display_matrix(led_matrix)
