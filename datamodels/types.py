from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Font:
    character_to_bytes: Dict[str, List[int]]

    character_width: int

    character_height: int

    dropdown_letters: List[int]


@dataclass
class Matrix:
    pixels: List[List[Tuple[int, int, int]]]

    bit_depth: int

    width: int

    height: int
