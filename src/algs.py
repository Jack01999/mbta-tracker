import src.data.state as state

from src.data.types import Character, Font
from typing import List, Tuple


def draw_character(
    pixels: List[List[Tuple[int, int, int]]],
    character: Character,
    row_start: int,
    col_start: int,
) -> List[List[Tuple[int, int, int]]]:
    """Draw on, and return an led matrix. `row_start` and  `col__start`
    both start at zero and begin in the upper left corner"""

    row = row_start
    for px_row in character.character_value:
        col = col_start
        for i in range(character.width_px - 1, -1, -1):
            bit = (px_row >> i) & 1
            if bit:
                # dot color, can make anything
                pixels[row][col] = state.text_color

            col += 1
        row += 1

    return pixels


# TODO store a map rather than searching for each letter
def key_to_character(
    font: Font,
    key: str,
) -> Character:
    """Given a character `key` (ex: 'G'), return the corresponging `Character`.

    See `datamodels.types.Character`

    Raise `ValueError` if the character is not found
    """
    for character in font.characters:
        if character.character_key == key:
            return character
    raise ValueError
