from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class Program(Enum):
    MBTA = 1
    BALL_BOUNCE = 2
    STROBE = 3

@dataclass
class Character:
    character_key: str
    """ex: 'a' """

    character_value: List[int]
    """ The pixel representation of the character key.
    
     ex: '[0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000]' """

    width_px: int
    """The width of the character values (pixel representation), in pixels"""

    dropdown: bool
    """Whether or not the character should drop down by one pixel."""


@dataclass
class Font:
    characters: List[Character]
    """List of characters contained in the font."""

    height_px: int
    """The hight of any character, before it may be dropped down by one pixel."""


@dataclass
class LedMatrix:
    pixels: List[List[Tuple[int, int, int]]]
    """A 2d list ([x0, x1, ...],[y0, y1, ...]), each containing an (r, g, b) color.
    Starting in the upper left most corner, incremending down and to the right.
    
    See `LedMatrix.bit_depth` for how large the colors can be
    """

