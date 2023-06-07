import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

BIT_DEPTH = 255

MATRIX_WIDTH = 64
MATRIX_HEIGHT = 32

LETTER_WIDTH = 5
LETTER_HEIGHT = 7

# font source: https://fontstruct.com/fontstructions/show/1660063/calculator-matrix

font_lowercase = {
    " ": [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
    "a": [0b00000, 0b00000, 0b01110, 0b00001, 0b01111, 0b10001, 0b01111],
    "b": [0b10000, 0b10000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10110],
    "c": [0b00000, 0b00000, 0b01110, 0b10000, 0b10000, 0b10001, 0b01110],
    "d": [0b00001, 0b00001, 0b01101, 0b10011, 0b10001, 0b10001, 0b01111],
    "e": [0b00000, 0b00000, 0b01110, 0b10001, 0b11111, 0b10000, 0b01110],
    "f": [0b00110, 0b01001, 0b01000, 0b11100, 0b01000, 0b01000, 0b01000],
    "g": [0b00000, 0b01111, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
    "h": [0b10000, 0b10000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10001],
    "i": [0b00100, 0b00000, 0b01100, 0b00100, 0b00100, 0b00100, 0b01110],
    "j": [0b00001, 0b00000, 0b00011, 0b00001, 0b00001, 0b01001, 0b00110],
    "k": [0b10000, 0b10000, 0b10010, 0b10100, 0b11100, 0b10010, 0b10001],
    "l": [0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    "m": [0b00000, 0b00000, 0b00000, 0b11010, 0b10101, 0b10001, 0b10001],
    "n": [0b00000, 0b00000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10001],
    "o": [0b00000, 0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b01110],
    "p": [0b00000, 0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000],
    "q": [0b00000, 0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00001],
    "r": [0b00000, 0b00000, 0b10110, 0b11001, 0b10000, 0b10000, 0b10000],
    "s": [0b00000, 0b00000, 0b01111, 0b10000, 0b01110, 0b00001, 0b11110],
    "t": [0b01000, 0b01000, 0b11100, 0b01000, 0b01000, 0b01001, 0b00110],
    "u": [0b00000, 0b00000, 0b10001, 0b10001, 0b10001, 0b10011, 0b01101],
    "v": [0b00000, 0b00000, 0b10001, 0b10001, 0b01010, 0b01010, 0b00100],
    "w": [0b00000, 0b00000, 0b10001, 0b10001, 0b10101, 0b10101, 0b01010],
    "x": [0b00000, 0b00000, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001],
    "y": [0b00000, 0b10001, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
    "z": [0b00000, 0b00000, 0b11111, 0b00010, 0b00100, 0b01000, 0b11111],
}

font_uppercase = {
    " ": [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
    "A": [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    "B": [0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110],
    "C": [0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110],
    "D": [0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110],
    "E": [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111],
    "F": [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000],
    "G": [0b01110, 0b10001, 0b10000, 0b10011, 0b10001, 0b10001, 0b01110],
    "H": [0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    "I": [0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    "J": [0b00001, 0b00001, 0b00001, 0b00001, 0b00001, 0b10001, 0b01110],
    "K": [0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001],
    "L": [0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
    "M": [0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001],
    "N": [0b10001, 0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001],
    "O": [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "P": [0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000],
    "Q": [0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101],
    "R": [0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001],
    "S": [0b01110, 0b10001, 0b10000, 0b01110, 0b00001, 0b10001, 0b01110],
    "T": [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    "U": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "V": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
    "W": [0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b10101, 0b01010],
    "X": [0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001],
    "Y": [0b10001, 0b10001, 0b10001, 0b01110, 0b00100, 0b00100, 0b00100],
    "Z": [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111],
}

font_lowercase_numbers = {
    "0": [0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "1": [0b00000, 0b00010, 0b00110, 0b00010, 0b00010, 0b00010, 0b01111],
    "2": [0b00000, 0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0b11111],
    "3": [0b00000, 0b01110, 0b10001, 0b00001, 0b00110, 0b00001, 0b11110],
    "4": [0b00000, 0b00001, 0b00011, 0b00101, 0b01001, 0b01111, 0b00001],
    "5": [0b00000, 0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b11110],
    "6": [0b00000, 0b01110, 0b10001, 0b10000, 0b11110, 0b10001, 0b01110],
    "7": [0b00000, 0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000],
    "8": [0b00000, 0b01110, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    "9": [0b00000, 0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
}

font_uppercase_numbers = {
    "0": [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "1": [0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    "2": [0b11110, 0b00001, 0b00001, 0b00010, 0b00100, 0b01000, 0b11111],
    "3": [0b11110, 0b00001, 0b00001, 0b00110, 0b00001, 0b00001, 0b11110],
    "4": [0b10001, 0b10001, 0b10001, 0b11111, 0b00001, 0b00001, 0b00001],
    "5": [0b11111, 0b10000, 0b10000, 0b11110, 0b00001, 0b00001, 0b11110],
    "6": [0b01110, 0b10000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110],
    "7": [0b11111, 0b00001, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000],
    "8": [0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    "9": [0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00001, 0b01110],
}

font_symbols = {
    ".": [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b01100, 0b01100],
    ",": [0b00000, 0b00000, 0b00000, 0b00000, 0b0000, 0b01000, 0b10000],
    '"': [0b00000, 0b00000, 0b10001, 0b10001, 0b01010, 0b01010, 0b00100],
    "'": [0b00000, 0b00000, 0b00100, 0b00100, 0b01000, 0b00000, 0b00000],
    "?": [0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0b00000, 0b00100],
    "!": [0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00000, 0b00100],
    "@": [0b01110, 0b10001, 0b10101, 0b10111, 0b10100, 0b10001, 0b01110],
    "_": [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111],
    "*": [0b00100, 0b10101, 0b01110, 0b10101, 0b00100, 0b00000, 0b00000],
    "#": [0b00000, 0b01010, 0b01010, 0b11111, 0b010100, 0b11111, 0b01010, 0b01010],
    "$": [0b00010, 0b01111, 0b10100, 0b01110, 0b00101, 0b11110, 0b0010],
    "%": [0b11000, 0b11001, 0b00010, 0b00100, 0b01000, 0b10011, 0b00011],
    "&": [0b00110, 0b01001, 0b01001, 0b00110, 0b10011, 0b10011, 0b01101],
    "(": [0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010],
    ")": [0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000],
    "+": [0b00000, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0b00000],
    "-": [0b00000, 0b00000, 0b00000, 0b11111, 0b00000, 0b00000, 0b00000],
    "/": [0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b00000, 0b00000],
    ":": [0b00000, 0b00100, 0b00000, 0b00000, 0b00100, 0b00000, 0b00000],
    ";": [0b00000, 0b00100, 0b00000, 0b00000, 0b00100, 0b00100, 0b00000],
    "<": [0b00010, 0b00100, 0b01000, 0b10000, 0b01000, 0b00100, 0b00010],
}

all_fonts = (
    font_lowercase
    | font_uppercase
    | font_lowercase_numbers
    | font_uppercase_numbers
    | font_symbols
)


def display_matrix(matrix: List[List[Tuple[int, int, int]]]) -> None:
    """Given a led matrix, display it to the user using matplotlib
    using matplotlib"""
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
    """Draw on, and return an led matrix. `row_start` and  `col__start`
    both start at zero and begin in the upper left corner"""

    row = row_start
    for horizontal in all_fonts[letter]:
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

    col_index = 0
    row_index = 0
    drop_down_letters = ["g", "j", "p", "q", "y"]

    for letter in all_fonts.keys():
        if letter in [" "]:
            continue

            # new row
        if col_index + LETTER_WIDTH >= MATRIX_WIDTH:
            col_index = 0
            row_index += LETTER_HEIGHT + 1

            # new page
        if row_index + LETTER_HEIGHT >= MATRIX_HEIGHT + 5:
            display_matrix(led_matrix)
            row_index = 0
            col_index = 0
            # clear the  background
            led_matrix = np.random.randint(
                200, BIT_DEPTH, (MATRIX_HEIGHT, MATRIX_WIDTH, 3)
            )

        print("col", col_index)
        print("row", row_index, "\n")
        led_matrix = draw_letter(
            led_matrix,
            letter,
            row_index + 1 if letter in drop_down_letters else row_index,
            col_index,
        )

        col_index += LETTER_WIDTH + 1

        # led_matrix = draw_letter(led_matrix, "b", 0, LETTER_WIDTH)
        # led_matrix = draw_letter(led_matrix, "c", 0, LETTER_WIDTH * 2)
        # led_matrix = draw_letter(led_matrix, "d", 0, LETTER_WIDTH * 3)
        # led_matrix = draw_letter(led_matrix, "d", 0, LETTER_WIDTH * 3)
        # led_matrix = draw_letter(led_matrix, "d", 0, LETTER_WIDTH * 3)
        # led_matrix = draw_letter(led_matrix, "d", 0, LETTER_WIDTH * 3)
    display_matrix(led_matrix)
