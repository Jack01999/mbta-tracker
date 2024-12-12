import json
from dataclasses import dataclass
from functools import wraps
from math import floor
from typing import Callable, List, Tuple

import numpy as np
from networkx import draw
from pyparsing import col

PixelDisplay = np.ndarray

Duration = float
"""Duration in seconds"""


@dataclass
class Character:
    character_key: str
    """ex: 'a' """

    character_value: List[int]
    """ The pixel representation of the character key.
    
     ex: '[0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000]' """

    width_px: int
    """The width of the character values (pixel representation), in pixels"""

    height_px: int
    """The height of the character values (pixel representation), in pixels"""


Font = List[Character]


@dataclass(frozen=True)
class DisplayDimensions:
    width: int
    height: int
    data_type: np.dtype


dimensions = DisplayDimensions(width=64, height=32, data_type=np.dtype(np.int32))


def save_json(data: dict, filename: str):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def validate_pixels(func: Callable):
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


def draw_character_on(
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


def word_width(word: str) -> int:
    """Return the estimates width of the word in pixels.

    ex "-" = 5
       "--" = 11 (1 space between characters)
    """
    return sum(key_to_character(c).width_px + 1 for c in word) - 1


# @validate_pixels
def draw_lines_on(
    pixels: PixelDisplay,
    lines: List[str],
    color: Tuple[int, int, int] = (255, 255, 255),
    raise_on_overflow=False,
    horizontal_shift=0,
) -> PixelDisplay:
    """Given a list of lines, draw the text on and return `pixels`."""

    row_index = 0
    for line in lines:
        # col_index = 0
        character = None
        line_width = 0
        col_index = horizontal_shift

        # line_width = word_width(line)
        # if lines starts with -left- or -right- or -center- then adjust the text
        if line.startswith("-left-"):
            line = line[6:]
            line_width = word_width(line)

        elif line.startswith("-right-"):
            line = line[7:]
            line_width = word_width(line)

            col_index = dimensions.width - line_width
        elif line.startswith("-center-"):
            line = line[8:]
            line_width = word_width(line)
            col_index = floor((dimensions.width - line_width) / 2)
        else:
            line_width = word_width(line)

            # print(f"colum index: {col_index}")

        for character_key in line:
            character = key_to_character(character_key)

            if raise_on_overflow:
                if col_index + character.width_px > dimensions.width:
                    raise ValueError(
                        f"Text too long: '{line}' for {line} got {col_index + character.width_px}"
                    )

                if row_index + character.height_px > dimensions.width:
                    raise ValueError(
                        f"Text too long: '{line}' got {row_index + character.height_px}"
                    )

            draw_character_on(
                pixels,
                character,
                row_index,
                col_index,
                color,
            )
            col_index += character.width_px + 1
        row_index += character.height_px + 1 if character else 0

    return pixels


def str_to_lines(
    st: str,
) -> List[str]:
    """Given a string `st`, return a list of lines that fit within the display dimensions."""

    col_index = 0
    lines = []
    line = ""

    for s in st:
        width = key_to_character(s).width_px
        if width > dimensions.width:
            raise ValueError(f"Character too wide: '{s}'")

        # Same line
        if col_index + width < dimensions.width:
            line += s
            col_index += width + 1

        # New line
        else:
            lines.append(line)
            line = s
            col_index = width + 1

    # Add last line
    if len(line) > 0:
        lines.append(line)

    return lines


# TODO store a map rather than searching for each letter
def key_to_character(
    key: str,
) -> Character:
    """Given a character `key` (ex: 'G'), return the corresponding `Character`.

    See `datamodels.types.Character`

    Raise `ValueError` if the character is not found
    """
    for character in font:
        if character.character_key == key:
            return character
    raise ValueError(f"Character '{key}' not found in font")


def parse_raw_font(raw_font: dict) -> Font:
    characters: Font = []
    for char_key, char_values in raw_font.items():
        try:
            v = char_values.get("bytes")
            if not v:
                raise ValueError("Invalid character value")
            w = char_values.get("width_px")
            if not w:
                raise ValueError("Invalid character width")
            characters.append(
                Character(
                    character_key=char_key,
                    character_value=v,
                    width_px=w,
                    height_px=7,
                )
            )
        except KeyError:
            raise ValueError(f"Invalid character '{char_key}'")
    return characters


def parse_bdf_font_to_raw(bdf_filename) -> dict:
    with open(bdf_filename, "r") as f:
        lines = f.readlines()

    font_raw = {}
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        if line.startswith("STARTCHAR"):
            char_data = {}
            char_name = line.split(" ", 1)[1]
            idx += 1
            while not lines[idx].strip().startswith("ENDCHAR"):
                line = lines[idx].strip()
                if line.startswith("ENCODING"):
                    encoding = int(line.split(" ", 1)[1])
                    char_data["encoding"] = encoding
                elif line.startswith("BBX"):
                    bbx_parts = line.split(" ")
                    bbx = {
                        "width_px": int(bbx_parts[1]),
                        "height": int(bbx_parts[2]),
                        "xoffset": int(bbx_parts[3]),
                        "yoffset": int(bbx_parts[4]),
                    }
                    char_data["bbx"] = bbx
                elif line == "BITMAP":
                    idx += 1
                    bitmap_lines = []
                    while lines[idx].strip() != "ENDCHAR":
                        bitmap_line = lines[idx].strip()
                        if bitmap_line != "":
                            bitmap_lines.append(bitmap_line)
                        idx += 1
                    char_data["bitmap"] = bitmap_lines
                    break
                idx += 1

            # Process the bitmap data
            width = char_data["bbx"]["width_px"]
            height = char_data["bbx"]["height"]
            x_offset = char_data["bbx"]["xoffset"]
            y_offset = char_data["bbx"]["yoffset"]
            bitmap = char_data["bitmap"]

            # Initialize the canvas with empty pixels
            canvas_height = height + abs(y_offset)
            canvas = ["0b0" * width for _ in range(canvas_height)]

            # Adjust for y_offset
            if y_offset < 0:
                start_row = -y_offset
            else:
                start_row = 0

            # Process the bitmap lines
            processed_bytes = []
            for hex_line in bitmap:
                bin_line = bin(int(hex_line, 16))[2:].zfill(8)

                # Adjust for x_offset
                if x_offset < 0:
                    bin_line = bin_line[-x_offset:].ljust(8, "0")
                elif x_offset > 0:
                    bin_line = bin_line[:-x_offset].rjust(8, "0")

                # Extract the leftmost 'width' bits
                bits = bin_line[:width]

                # Convert bits to integer
                byte_value = int(bits, 2)
                processed_bytes.append(byte_value)

            # Map the character
            char_key = chr(char_data["encoding"])
            font_raw[char_key] = {
                "bytes": processed_bytes,
                "width_px": width,
            }

        idx += 1
    return font_raw


default_font_raw = {
    " ": {
        "bytes": [
            0b0,
            0b0,
            0b0,
            0b0,
            0b0,
            0b0,
            0b0,
        ],
        "width_px": 1,
    },
    "a": {
        "bytes": [
            0b00000,
            0b00000,
            0b01110,
            0b00001,
            0b01111,
            0b10001,
            0b01111,
        ],
        "width_px": 5,
    },
    "b": {
        "bytes": [
            0b10000,
            0b10000,
            0b10110,
            0b11001,
            0b10001,
            0b10001,
            0b11110,
        ],
        "width_px": 5,
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
        "width_px": 5,
    },
    "d": {
        "bytes": [
            0b00001,
            0b00001,
            0b01101,
            0b10011,
            0b10001,
            0b10001,
            0b01111,
        ],
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
    },
    "h": {
        "bytes": [
            0b10000,
            0b10000,
            0b10110,
            0b11001,
            0b10001,
            0b10001,
            0b10001,
        ],
        "width_px": 5,
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
        "width_px": 3,
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
        "width_px": 4,
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
        "width_px": 5,
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
        "width_px": 3,
    },
    "m": {
        "bytes": [
            0b00000,
            0b00000,
            0b00000,
            0b11010,
            0b10101,
            0b10001,
            0b10001,
        ],
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
    },
    "t": {
        "bytes": [
            0b01000,
            0b01000,
            0b11100,
            0b01000,
            0b01000,
            0b01001,
            0b00110,
        ],
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 3,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
    },
    #
    # lowercase numbers
    #
    # "0": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    #     "width_px": 5
    # },
    # "1": {
    #     "bytes": [0b00000, 0b00010, 0b00110, 0b00010, 0b00010, 0b00010, 0b01111],
    #     "width_px": 5
    # },
    # "2": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0b11111],
    #     "width_px": 5
    # },
    # "3": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b00001, 0b00110, 0b00001, 0b11110],
    #     "width_px": 5
    # },
    # "4": {
    #     "bytes": [0b00000, 0b00001, 0b00011, 0b00101, 0b01001, 0b01111, 0b00001],
    #     "width_px": 5
    # },
    # "5": {
    #     "bytes": [0b00000, 0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b11110],
    #     "width_px": 5
    # },
    # "6": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b10000, 0b11110, 0b10001, 0b01110],
    #     "width_px": 5
    # },
    # "7": {
    #     "bytes": [0b00000, 0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000],
    #     "width_px": 5
    # },
    # "8": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    #     "width_px": 5
    # },
    # "9": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
    #     "width_px": 5
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
        "width_px": 5,
    },
    "1": {
        "bytes": [
            0b110,
            0b010,
            0b010,
            0b010,
            0b010,
            0b010,
            0b111,
        ],
        "width_px": 3,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 1,
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
        "width_px": 2,
    },
    "'": {
        "bytes": [
            0b1,
            0b1,
            0b0,
            0b0,
            0b0,
            0b0,
            0b0,
        ],
        "width_px": 1,
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
        "width_px": 5,
    },
    "!": {
        "bytes": [
            0b1,
            0b1,
            0b1,
            0b1,
            0b1,
            0b0,
            0b1,
        ],
        "width_px": 1,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
    },
    "&": {
        "bytes": [
            0b00110,
            0b01001,
            0b01001,
            0b01110,
            0b10010,
            0b10011,
            0b01101,
        ],
        "width_px": 5,
    },
    "(": {
        "bytes": [
            0b001,
            0b010,
            0b100,
            0b100,
            0b100,
            0b010,
            0b001,
        ],
        "width_px": 3,
    },
    ")": {
        "bytes": [
            0b100,
            0b010,
            0b001,
            0b001,
            0b001,
            0b010,
            0b100,
        ],
        "width_px": 3,
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
        "width_px": 5,
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
        "width_px": 5,
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
        "width_px": 5,
    },
    ":": {
        "bytes": [
            0b0,
            0b1,
            0b0,
            0b0,
            0b1,
            0b0,
            0b0,
        ],
        "width_px": 1,
    },
    ";": {
        "bytes": [
            0b0,
            0b1,
            0b0,
            0b0,
            0b1,
            0b1,
            0b0,
        ],
        "width_px": 1,
    },
    "<": {
        "bytes": [
            0b0001,
            0b0010,
            0b0100,
            0b1000,
            0b0100,
            0b0010,
            0b0001,
        ],
        "width_px": 4,
    },
    ">": {
        "bytes": [
            0b1000,
            0b0100,
            0b0010,
            0b0001,
            0b0010,
            0b0100,
            0b1000,
        ],
        "width_px": 4,
    },
    "=": {
        "bytes": [
            0b00000,
            0b00000,
            0b11111,
            0b00000,
            0b11111,
            0b00000,
            0b00000,
        ],
        "width_px": 5,
    },
    "[": {
        "bytes": [
            0b111,
            0b100,
            0b100,
            0b100,
            0b100,
            0b100,
            0b111,
        ],
        "width_px": 3,
    },
    "]": {
        "bytes": [
            0b111,
            0b001,
            0b001,
            0b001,
            0b001,
            0b001,
            0b111,
        ],
        "width_px": 3,
    },
    "{": {
        "bytes": [
            0b0011,
            0b0010,
            0b0010,
            0b1100,
            0b0010,
            0b0010,
            0b0011,
        ],
        "width_px": 4,
    },
    "}": {
        "bytes": [
            0b1100,
            0b0100,
            0b0100,
            0b0011,
            0b0100,
            0b0100,
            0b1100,
        ],
        "width_px": 4,
    },
    "|": {
        "bytes": [
            0b1,
            0b1,
            0b1,
            0b0,
            0b1,
            0b1,
            0b1,
        ],
        "width_px": 1,
    },
    "`": {
        "bytes": [
            0b10,
            0b01,
            0b00,
            0b00,
            0b00,
            0b00,
            0b00,
        ],
        "width_px": 2,
    },
    "~": {
        "bytes": [
            0b00000,
            0b00000,
            0b01101,
            0b10010,
            0b00000,
            0b00000,
            0b00000,
        ],
        "width_px": 5,
    },
    "^": {
        "bytes": [
            0b00100,
            0b01010,
            0b10001,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
        ],
        "width_px": 5,
    },
    '"': {
        "bytes": [
            0b101,
            0b101,
            0b000,
            0b000,
            0b000,
            0b000,
            0b000,
        ],
        "width_px": 3,
    },
    "\\": {
        "bytes": [
            0b00000,
            0b10000,
            0b01000,
            0b00100,
            0b00010,
            0b00001,
            0b00000,
        ],
        "width_px": 5,
    },
    "°": {
        "bytes": [
            0b010,
            0b101,
            0b010,
            0b000,
            0b000,
            0b000,
            0b000,
        ],
        "width_px": 3,
    },
}
Color = Tuple[int, int, int]
R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)
W = (255, 255, 255)
B = (0, 0, 0)
# def draw

font_5x7 = parse_raw_font(parse_bdf_font_to_raw("controller/fonts/5x7.bdf"))
font_6x9 = parse_raw_font(parse_bdf_font_to_raw("controller/fonts/6x9.bdf"))
font = parse_raw_font(default_font_raw)

assert word_width("a") == 5
assert word_width("ab") == 11
assert word_width("abc") == 17

for f in font:
    w = f.width_px
    assert w >= 1 and w <= 5
