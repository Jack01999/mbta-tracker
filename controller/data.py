from dataclasses import dataclass
from tkinter import W
from typing import List, Tuple

import numpy as np

PixelDisplay = np.ndarray

Duration = float
"""Duration in seconds"""

from functools import wraps


@dataclass(frozen=True)
class DisplayDimensions:
    width: int
    height: int
    data_type: np.dtype


dimensions = DisplayDimensions(width=64, height=32, data_type=np.dtype(np.int32))


def validate_pixels(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pixels = kwargs.get("pixels")
        if pixels is None:
            raise ValueError("pixels is a required property")
        if not isinstance(pixels, np.ndarray):
            raise ValueError("pixels must be a numpy array")
        if pixels.shape != (dimensions.height, dimensions.width, 3):
            raise ValueError(
                f"pixels must be of shape ({dimensions.height}, {dimensions.width}, 3)"
            )
        if pixels.dtype != dimensions.data_type:
            raise ValueError(f"pixels must be of dtype {dimensions.data_type}")
        return func(*args, **kwargs)

    return wrapper


@dataclass
class Character:
    character_key: str
    """ex: 'a' """

    character_value: List[int]
    """ The pixel representation of the character key.
    
     ex: '[0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000]' """

    width_px: int
    """The width of the character values (pixel representation), in pixels"""


@dataclass
class Font:
    characters: List[Character]
    """List of characters contained in the font."""

    height_px: int
    """The hight of any character"""


# @validate_pixels
# def draw_logo(
#     pixels: PixelDisplay,
#     color: Tuple[int, int, int,],
#     logo: List[str,],
#     row_start: int = 0,
#     col_start: int = 0,
# ) -> PixelDisplay:
#     """ """

#     def inner(
#         pixels: PixelDisplay,
#         pattern: List[str,],
#         row_start: int,
#         col_start: int,
#         color: Tuple[int, int, int,],
#     ):
#         for i, p in enumerate(pattern):
#             p = p.replace(" ", "")
#             pattern[i] = p

#         # print(pattern)
#         for row_offset, line in enumerate(pattern):
#             for col_offset, char in enumerate(line):
#                 if char == "1":
#                     row = row_start + row_offset
#                     col = col_start + col_offset
#                     if 0 <= row < pixels.shape[0] and 0 <= col < pixels.shape[1]:
#                         pixels[row][col] = color

#     inner(pixels, logo, row_start, col_start, color)

#     return pixels


@validate_pixels
def draw_text(
    pixels: PixelDisplay,
    lines: List[str,],
    color: Tuple[int, int, int] = (255, 255, 255),
) -> PixelDisplay:
    """Given a list of lines, draw the text on and reurn `pixels`."""


    row_index = 0
    for line in lines:
        col_index = 0

        for character_key in line:
            character = key_to_character(font1, character_key)

            if col_index + character.width_px >= dimensions.width:
                raise ValueError(f"Text too long: '{line}'")

            if row_index + font1.height_px >= dimensions.width:
                raise ValueError(f"Text too long: '{line}'")

            draw_character(
                pixels,
                character,
                row_index,
                col_index,
                color,
            )
            col_index += character.width_px
        row_index += font1.height_px +1

    return pixels




# @validate_pixels
def str_to_lines(
    st: str,
) -> List[str]:
    """Given a list of words such as 
    ['Red', 'Line:', 'Delays', 'of', 'about', '25', 'minutes', 'between', 'Alewife', 'and', 'Harvard', 'due', 'to', 'a', 'disabled', 'train', 'near', 'Harvard.', 'Trains', 'may', 'stand', 'by', 'at', 'stations.']
    return a list of lines that can be drawn on the display.
    each line should be less than 64 characters long.
    """
    words = st.split()

    space_width = key_to_character(font1, " ").width_px

    col_index = 0
    lines = []
    line = ""
    for word in words:
        # Calculate the width of the word
        word_width = 0
        for c in word:
            char = key_to_character(font1, c)
            word_width += char.width_px
        
        # account for the pixel space between character

        # word_width += len(word) - 1

        if word_width > dimensions.width:
            raise ValueError(f"Word too long: '{word}'")
        
        # Check if the word fits as the first word in the line,
        # ie. the line is empty and no prefixing space is needed
        if len(line) == 0 and word_width < dimensions.width:
            line += word
            col_index += word_width

        # Check if the word fits as not the first word in the line,
        # ie. a prefixing space is needed
        elif len(line) > 0 and col_index + space_width + word_width < dimensions.width:
            line += " " + word
            col_index += space_width + word_width + 1

        # Otherwise, we need a new line
        else:
            lines.append(line)
            line = word
            col_index = word_width + 1

    # Add the last line
    if len(line) > 0:
        lines.append(line)

    return lines

    
def draw_character(
    pixels: PixelDisplay,
    character: Character,
    row_start: int,
    col_start: int,
    color: Tuple[
        int,
        int,
        int,
    ],
):
    row = row_start
    for px_row in character.character_value:
        col = col_start
        for i in range(character.width_px - 1, -1, -1):
            bit = (px_row >> i) & 1
            if bit:
                if 0 <= row < pixels.shape[0] and 0 <= col < pixels.shape[1]:
                    pixels[row][col] = color
            col += 1
        row += 1


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
    raise ValueError(f"Character '{key}' not found in font")


def parse_raw_font(raw_font: dict) -> Font:
    characters = []
    for char_key, char_values in raw_font.items():
        try:
            v = char_values.get("bytes")
            if not v:
                raise ValueError("Invalid character value")
            w = char_values.get("width")
            if not w:
                raise ValueError("Invalid character width")
            characters.append(
                Character(
                    character_key=char_key,
                    character_value=v,
                    width_px=w,
                )
            )
        except KeyError:
            raise ValueError(f"Invalid character '{char_key}'")
    return Font(characters=characters, height_px=7)


DEFAULT_FONT_RAW = {
    " ": {
        "bytes": [0b0, 0b0, 0b0, 0b0, 0b0, 0b0, 0b0],
        "width": 1,
    },
    "a": {
        "bytes": [
            0b00000,
            0b00000,
            0b01100,
            0b00010,
            0b01110,
            0b10010,
            0b01111,
        ],
        "width": 5,
    },
    "b": {
        "bytes": [
            0b10000,
            0b10000,
            0b10000,
            0b11111,
            0b10001,
            0b10001,
            0b11110,
        ],
        "width": 5,
    },
    "c": {
        "bytes": [
            0b00000,
            0b00000,
            0b01110,
            0b10000,
            0b10000,
            0b10001,
            0b01110,
        ],
        "width": 5,
    },
    "d": {
        "bytes": [
            0b00001,
            0b00001,
            0b00001,
            0b01111,
            0b10001,
            0b10001,
            0b01111,
        ],
        "width": 5,
    },
    "e": {
        "bytes": [
            0b00000,
            0b00000,
            0b01110,
            0b10001,
            0b11111,
            0b10000,
            0b01110,
        ],
        "width": 5,
    },
    "f": {
        "bytes": [
            0b00110,
            0b01001,
            0b01000,
            0b11100,
            0b01000,
            0b01000,
            0b01000,
        ],
        "width": 5,
    },
    "g": {
        "bytes": [
            0b00000,
            0b01111,
            0b10001,
            0b10001,
            0b01111,
            0b00001,
            0b01110,
        ],
        "width": 5,
    },
    "h": {
        "bytes": [
            0b10000,
            0b10000,
            0b10000,
            0b11110,
            0b10001,
            0b10001,
            0b10001,
        ],
        "width": 5,
    },
    "i": {
        "bytes": [
            0b010,
            0b000,
            0b110,
            0b010,
            0b010,
            0b010,
            0b111,
        ],
        "width": 3,
    },
    "j": {
        "bytes": [
            0b0001,
            0b0000,
            0b0011,
            0b0001,
            0b0001,
            0b1001,
            0b0110,
        ],
        "width": 4,
    },
    "k": {
        "bytes": [
            0b10000,
            0b10000,
            0b10010,
            0b10100,
            0b11100,
            0b10010,
            0b10001,
        ],
        "width": 5,
    },
    "l": {
        "bytes": [
            0b110,
            0b010,
            0b010,
            0b010,
            0b010,
            0b010,
            0b111,
        ],
        "width": 3,
    },
    "m": {
        "bytes": [
            0b00000,
            0b00000,
            0b00000,
            0b01010,
            0b10101,
            0b10001,
            0b10001,
        ],
        "width": 5,
    },
    "n": {
        "bytes": [
            0b00000,
            0b00000,
            0b10110,
            0b11001,
            0b10001,
            0b10001,
            0b10001,
        ],
        "width": 5,
    },
    "o": {
        "bytes": [
            0b00000,
            0b00000,
            0b01110,
            0b10001,
            0b10001,
            0b10001,
            0b01110,
        ],
        "width": 5,
    },
    "p": {
        "bytes": [
            0b00000,
            0b11110,
            0b10001,
            0b10001,
            0b11110,
            0b10000,
            0b10000,
        ],
        "width": 5,
    },
    "q": {
        "bytes": [
            0b00000,
            0b01110,
            0b10001,
            0b10001,
            0b01111,
            0b00001,
            0b00001,
        ],
        "width": 5,
    },
    "r": {
        "bytes": [
            0b00000,
            0b00000,
            0b10110,
            0b11001,
            0b10000,
            0b10000,
            0b10000,
        ],
        "width": 5,
    },
    "s": {
        "bytes": [
            0b00000,
            0b00000,
            0b01111,
            0b10000,
            0b01110,
            0b00001,
            0b11110,
        ],
        "width": 5,
    },
    "t": {
        "bytes": [
            0b00100,
            0b00100,
            0b11111,
            0b00100,
            0b00100,
            0b00101,
            0b00010,
        ],
        "width": 5,
    },
    "u": {
        "bytes": [
            0b00000,
            0b00000,
            0b10001,
            0b10001,
            0b10001,
            0b10011,
            0b01101,
        ],
        "width": 5,
    },
    "v": {
        "bytes": [
            0b00000,
            0b00000,
            0b10001,
            0b10001,
            0b01010,
            0b01010,
            0b00100,
        ],
        "width": 5,
    },
    "w": {
        "bytes": [
            0b00000,
            0b00000,
            0b10001,
            0b10001,
            0b10101,
            0b10101,
            0b01010,
        ],
        "width": 5,
    },
    "x": {
        "bytes": [
            0b00000,
            0b00000,
            0b10001,
            0b01010,
            0b00100,
            0b01010,
            0b10001,
        ],
        "width": 5,
    },
    "y": {
        "bytes": [
            0b00000,
            0b10001,
            0b10001,
            0b10001,
            0b01111,
            0b00001,
            0b01110,
        ],
        "width": 5,
    },
    "z": {
        "bytes": [
            0b00000,
            0b00000,
            0b11111,
            0b00010,
            0b00100,
            0b01000,
            0b11111,
        ],
        "width": 5,
    },
    "A": {
        "bytes": [
            0b01110,
            0b10001,
            0b10001,
            0b11111,
            0b10001,
            0b10001,
            0b10001,
        ],
        "width": 5,
    },
    "B": {
        "bytes": [
            0b11110,
            0b10001,
            0b10001,
            0b11110,
            0b10001,
            0b10001,
            0b11110,
        ],
        "width": 5,
    },
    "C": {
        "bytes": [
            0b01110,
            0b10001,
            0b10000,
            0b10000,
            0b10000,
            0b10001,
            0b01110,
        ],
        "width": 5,
    },
    "D": {
        "bytes": [
            0b11110,
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b11110,
        ],
        "width": 5,
    },
    "E": {
        "bytes": [
            0b11111,
            0b10000,
            0b10000,
            0b11110,
            0b10000,
            0b10000,
            0b11111,
        ],
        "width": 5,
    },
    "F": {
        "bytes": [
            0b11111,
            0b10000,
            0b10000,
            0b11110,
            0b10000,
            0b10000,
            0b10000,
        ],
        "width": 5,
    },
    "G": {
        "bytes": [
            0b01110,
            0b10001,
            0b10000,
            0b10011,
            0b10001,
            0b10001,
            0b01110,
        ],
        "width": 5,
    },
    "H": {
        "bytes": [
            0b10001,
            0b10001,
            0b10001,
            0b11111,
            0b10001,
            0b10001,
            0b10001,
        ],
        "width": 5,
    },
    "I": {
        "bytes": [
            0b111,
            0b010,
            0b010,
            0b010,
            0b010,
            0b010,
            0b111,
        ],
        "width": 3,
    },
    "J": {
        "bytes": [
            0b00001,
            0b00001,
            0b00001,
            0b00001,
            0b00001,
            0b10001,
            0b01110,
        ],
        "width": 5,
    },
    "K": {
        "bytes": [
            0b10001,
            0b10010,
            0b10100,
            0b11000,
            0b10100,
            0b10010,
            0b10001,
        ],
        "width": 5,
    },
    "L": {
        "bytes": [
            0b10000,
            0b10000,
            0b10000,
            0b10000,
            0b10000,
            0b10000,
            0b11111,
        ],
        "width": 5,
    },
    "M": {
        "bytes": [
            0b10001,
            0b11011,
            0b10101,
            0b10101,
            0b10001,
            0b10001,
            0b10001,
        ],
        "width": 5,
    },
    "N": {
        "bytes": [
            0b10001,
            0b10001,
            0b11001,
            0b10101,
            0b10011,
            0b10001,
            0b10001,
        ],
        "width": 5,
    },
    "O": {
        "bytes": [
            0b01110,
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b01110,
        ],
        "width": 5,
    },
    "P": {
        "bytes": [
            0b11110,
            0b10001,
            0b10001,
            0b11110,
            0b10000,
            0b10000,
            0b10000,
        ],
        "width": 5,
    },
    "Q": {
        "bytes": [
            0b01110,
            0b10001,
            0b10001,
            0b10001,
            0b10101,
            0b10010,
            0b01101,
        ],
        "width": 5,
    },
    "R": {
        "bytes": [
            0b11110,
            0b10001,
            0b10001,
            0b11110,
            0b10100,
            0b10010,
            0b10001,
        ],
        "width": 5,
    },
    "S": {
        "bytes": [
            0b01110,
            0b10001,
            0b10000,
            0b01110,
            0b00001,
            0b10001,
            0b01110,
        ],
        "width": 5,
    },
    "T": {
        "bytes": [
            0b11111,
            0b00100,
            0b00100,
            0b00100,
            0b00100,
            0b00100,
            0b00100,
        ],
        "width": 5,
    },
    "U": {
        "bytes": [
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b01110,
        ],
        "width": 5,
    },
    "V": {
        "bytes": [
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b01010,
            0b00100,
        ],
        "width": 5,
    },
    "W": {
        "bytes": [
            0b10001,
            0b10001,
            0b10001,
            0b10101,
            0b10101,
            0b10101,
            0b01010,
        ],
        "width": 5,
    },
    "X": {
        "bytes": [
            0b10001,
            0b10001,
            0b01010,
            0b00100,
            0b01010,
            0b10001,
            0b10001,
        ],
        "width": 5,
    },
    "Y": {
        "bytes": [
            0b10001,
            0b10001,
            0b10001,
            0b01110,
            0b00100,
            0b00100,
            0b00100,
        ],
        "width": 5,
    },
    "Z": {
        "bytes": [
            0b11111,
            0b00001,
            0b00010,
            0b00100,
            0b01000,
            0b10000,
            0b11111,
        ],
        "width": 5,
    },
    #
    # lowercase numbers
    #
    # "0": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110,],
    #     "width": 5,
    #
    # },
    # "1": {
    #     "bytes": [0b00000, 0b00010, 0b00110, 0b00010, 0b00010, 0b00010, 0b01111,],
    #     "width": 5,
    #
    # },
    # "2": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0b11111,],
    #     "width": 5,
    #
    # },
    # "3": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b00001, 0b00110, 0b00001, 0b11110,],
    #     "width": 5,
    #
    # },
    # "4": {
    #     "bytes": [0b00000, 0b00001, 0b00011, 0b00101, 0b01001, 0b01111, 0b00001,],
    #     "width": 5,
    #
    # },
    # "5": {
    #     "bytes": [0b00000, 0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b11110,],
    #     "width": 5,
    #
    # },
    # "6": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b10000, 0b11110, 0b10001, 0b01110,],
    #     "width": 5,
    #
    # },
    # "7": {
    #     "bytes": [0b00000, 0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000,],
    #     "width": 5,
    #
    # },
    # "8": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110,],
    #     "width": 5,
    #
    # },
    # "9": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110,],
    #     "width": 5,
    #
    # },
    "0": {
        "bytes": [
            0b01110,
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b01110,
        ],
        "width": 5,
    },
    "1": {
        "bytes": [
            0b01100,
            0b00100,
            0b00100,
            0b00100,
            0b00100,
            0b00100,
            0b01110,
        ],
        "width": 5,
    },
    "2": {
        "bytes": [
            0b01110,
            0b10001,
            0b00001,
            0b00010,
            0b00100,
            0b01000,
            0b11111,
        ],
        "width": 5,
    },
    "3": {
        "bytes": [
            0b11110,
            0b00001,
            0b00001,
            0b00110,
            0b00001,
            0b00001,
            0b11110,
        ],
        "width": 5,
    },
    "4": {
        "bytes": [
            0b10001,
            0b10001,
            0b10001,
            0b11111,
            0b00001,
            0b00001,
            0b00001,
        ],
        "width": 5,
    },
    "5": {
        "bytes": [
            0b11111,
            0b10000,
            0b10000,
            0b11110,
            0b00001,
            0b00001,
            0b11110,
        ],
        "width": 5,
    },
    "6": {
        "bytes": [
            0b01110,
            0b10000,
            0b10000,
            0b11110,
            0b10001,
            0b10001,
            0b01110,
        ],
        "width": 5,
    },
    "7": {
        "bytes": [
            0b11111,
            0b00001,
            0b00001,
            0b00010,
            0b00100,
            0b01000,
            0b10000,
        ],
        "width": 5,
    },
    "8": {
        "bytes": [
            0b01110,
            0b10001,
            0b10001,
            0b01110,
            0b10001,
            0b10001,
            0b01110,
        ],
        "width": 5,
    },
    "9": {
        "bytes": [
            0b01110,
            0b10001,
            0b10001,
            0b01111,
            0b00001,
            0b00001,
            0b01110,
        ],
        "width": 5,
    },
    ".": {
        "bytes": [
            0b0,
            0b0,
            0b0,
            0b0,
            0b0,
            0b0,
            0b1,
        ],
        "width": 1,
    },
    ",": {
        "bytes": [
            0b00,
            0b00,
            0b00,
            0b00,
            0b00,
            0b01,
            0b10,
        ],
        "width": 2,
    },
    '"': {
        "bytes": [
            0b00000,
            0b00000,
            0b10001,
            0b10001,
            0b01010,
            0b01010,
            0b00100,
        ],
        "width": 5,
    },
    "'": {
        "bytes": [
            0b00000,
            0b00000,
            0b00100,
            0b00100,
            0b01000,
            0b00000,
            0b00000,
        ],
        "width": 5,
    },
    "?": {
        "bytes": [
            0b01110,
            0b10001,
            0b00001,
            0b00010,
            0b00100,
            0b00000,
            0b00100,
        ],
        "width": 5,
    },
    "!": {
        "bytes": [
            0b00100,
            0b00100,
            0b00100,
            0b00100,
            0b00100,
            0b00000,
            0b00100,
        ],
        "width": 5,
    },
    "@": {
        "bytes": [
            0b01110,
            0b10001,
            0b10101,
            0b10111,
            0b10100,
            0b10001,
            0b01110,
        ],
        "width": 5,
    },
    "_": {
        "bytes": [
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b11111,
        ],
        "width": 5,
    },
    "*": {
        "bytes": [
            0b00100,
            0b10101,
            0b01110,
            0b10101,
            0b00100,
            0b00000,
            0b00000,
        ],
        "width": 5,
    },
    "#": {
        "bytes": [
            0b01010,
            0b01010,
            0b11111,
            0b01010,
            0b11111,
            0b01010,
            0b01010,
        ],
        "width": 5,
    },
    "$": {
        "bytes": [
            0b00010,
            0b01111,
            0b10100,
            0b01110,
            0b00101,
            0b11110,
            0b00100,
        ],
        "width": 5,
    },
    "%": {
        "bytes": [
            0b11000,
            0b11001,
            0b00010,
            0b00100,
            0b01000,
            0b10011,
            0b00011,
        ],
        "width": 5,
    },
    "&": {
        "bytes": [
            0b00110,
            0b01001,
            0b01001,
            0b00110,
            0b10011,
            0b10011,
            0b01101,
        ],
        "width": 5,
    },
    "(": {
        "bytes": [
            0b00010,
            0b00100,
            0b01000,
            0b01000,
            0b01000,
            0b00100,
            0b00010,
        ],
        "width": 5,
    },
    ")": {
        "bytes": [
            0b01000,
            0b00100,
            0b00010,
            0b00010,
            0b00010,
            0b00100,
            0b01000,
        ],
        "width": 5,
    },
    "+": {
        "bytes": [
            0b00000,
            0b00100,
            0b00100,
            0b11111,
            0b00100,
            0b00100,
            0b00000,
        ],
        "width": 5,
    },
    "-": {
        "bytes": [
            0b00000,
            0b00000,
            0b00000,
            0b11111,
            0b00000,
            0b00000,
            0b00000,
        ],
        "width": 5,
    },
    "/": {
        "bytes": [
            0b00000,
            0b00001,
            0b00010,
            0b00100,
            0b01000,
            0b10000,
            0b00000,
        ],
        "width": 5,
    },
    ":": {
        "bytes": [
            0b0,
            0b0,
            0b1,
            0b0,
            0b0,
            0b1,
            0b0,
        ],
        "width": 1,
    },
    ";": {
        "bytes": [
            0b00000,
            0b00100,
            0b00000,
            0b00000,
            0b00100,
            0b00100,
            0b00000,
        ],
        "width": 5,
    },
    "<": {
        "bytes": [
            0b00010,
            0b00100,
            0b01000,
            0b10000,
            0b01000,
            0b00100,
            0b00010,
        ],
        "width": 5,
    },
}


font1 = parse_raw_font(DEFAULT_FONT_RAW)
