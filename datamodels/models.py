from typing import List, Optional, Tuple


# @dataclass
class Font:
    character_to_bytes: dict[str, List[int]]

    character_width: int

    character_wheight: int


# @dataclass
class LedMatrix:
    led_values: Optional[List[List[Tuple[int, int, int]]]]

    bit_depth = int

    width = int

    height = int
