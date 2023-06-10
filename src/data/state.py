import copy
import numpy as np
from typing import List, Tuple
from src.datamodels.types import LedMatrix

# Could be refered to as "initial settiings"

bit_depth: int = 255
"""The depth of each color (r, g, b).

ex: 255 is white, 0 is black
"""

height: int = 32
"""Height (rows) of the matrix in pixels."""

width: int = 64
"""Width (columns) of the matrix in pixels."""

background: List[List[Tuple[int, int, int]]] = np.zeros(
    (height, width, 3), dtype=np.int
)
"""The background of the led_matrix (`state.led_matrix`). 

See `datamodels.types.LedMatrix.pixels` for a reference.
"""

led_matrix: LedMatrix = LedMatrix(
    pixels=copy.deepcopy(background),
    bit_depth=bit_depth,
    height_px=height,
    width_px=width,
)
"""Ked matrix that is to be dispalyed"""

text_color: Tuple[int, int, int] = (bit_depth, bit_depth // 2, 0)
"""Color of any text to be dispalyed"""
