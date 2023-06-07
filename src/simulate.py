import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

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

    # flatten tuples
    colors = matrix.reshape(-1, 3) / 255.0

    _, ax = plt.subplots(figsize=(8, 4), dpi=150)

    ax.set_xlim(-1, MATRIX_WIDTH)
    ax.set_ylim(-1, MATRIX_HEIGHT)

    ax.scatter(x.ravel(), y.ravel(), c=colors, s=12)

    # Invert y axis to match the matrix representation
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
                matrix[row][col] = (255, 0, 0) # dot color

            col += 1
        row += 1

    return matrix


# example
if __name__ == "__main__":
    # create background of different colors
    led_matrix = np.random.randint(200, 255, (MATRIX_HEIGHT, MATRIX_WIDTH, 3))

    led_matrix = draw_letter(led_matrix, "b", 0, 0)
    led_matrix = draw_letter(led_matrix, "b", 0, LETTER_WIDTH)
    led_matrix = draw_letter(led_matrix, "b", 0, LETTER_WIDTH * 2)
    led_matrix = draw_letter(led_matrix, "b", 0, LETTER_WIDTH * 3)
    display_matrix(led_matrix)
