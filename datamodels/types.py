from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Character:
    character_key: str
    """ex: 'a'"""

    character_value: List[int]
    """ex: '[0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000]'"""

    width_px: int
    """ex: 5"""

    dropdown: bool


@dataclass
class Font:
    characters: List[Character]

    height_px: int

    # TODO store a map rather than searching for each letter
    def get_character(key: str) -> Character:
        for character in Font.characters:
            if character.character_key == key:
                return character
        raise ValueError


@dataclass
class Matrix:
    pixels: List[List[Tuple[int, int, int]]]

    bit_depth: int

    width_px: int

    height_px: int
