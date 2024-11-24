from dataclasses import dataclass
from functools import wraps
from typing import List, Tuple

import numpy as np

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


@validate_pixels
def draw_text(
    pixels: PixelDisplay,
    lines: List[str,],
    color: Tuple[int, int, int] = (255, 255, 255),
    center=False,
) -> PixelDisplay:
    """Given a list of lines, draw the text on and reurn `pixels`."""

    row_index = 0
    for line in lines:
        col_index = 0
        character = None
        line_width = 0
        col_index = 0
        if center:
            for character_key in line:
                character = key_to_character(font, character_key)
                line_width += character.width_px
            col_index = int((dimensions.width - line_width) / 2)

        for character_key in line:
            character = key_to_character(font, character_key)

            if col_index + character.width_px >= dimensions.width:
                raise ValueError(f"Text too long: '{line}'")

            if row_index + character.height_px >= dimensions.width:
                raise ValueError(f"Text too long: '{line}'")

            draw_character(
                pixels,
                character,
                row_index,
                col_index,
                color,
            )
            col_index += character.width_px
        row_index += character.height_px if character else 0

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

    space_width = key_to_character(font, " ").width_px

    col_index = 0
    lines = []
    line = ""
    for word in words:
        # Calculate the width of the word
        word_width = 0
        for c in word:
            char = key_to_character(font, c)
            word_width += char.width_px
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
            col_index += space_width + word_width

        # Otherwise, we need a new line
        else:
            lines.append(line)
            line = word
            col_index = word_width

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
            w = char_values.get("width")
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
                        "width": int(bbx_parts[1]),
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
            width = char_data["bbx"]["width"]
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
                "width": width,
            }

        idx += 1
    return font_raw


font_5_7 = parse_raw_font(parse_bdf_font_to_raw("controller/fonts/5x7.bdf"))
font_6_9 = parse_raw_font(parse_bdf_font_to_raw("controller/fonts/6x9.bdf"))
font = font_6_9
