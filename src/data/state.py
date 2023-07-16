import numpy as np

from typing import List, Tuple


##############################################
## Could be refered to as settiings
##############################################
BIT_DEPTH: int = 255
"""The depth of each color (r, g, b).

255 is brightest, 1 is black
"""

HEIGHT: int = 32
"""Height (rows) of the matrix in pixels."""

WIDTH: int = 64
"""Width (columns) of the matrix in pixels."""

BACKGROUND: List[List[Tuple[int, int, int]]] = np.zeros(
    (HEIGHT, WIDTH, 3), dtype=np.int
)
# background = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)
""" The background of the led_matrix (`state.led_matrix`). 
"""

TEXT_COLOR: Tuple[int, int, int] = (BIT_DEPTH, BIT_DEPTH // 2, 0)  # orange
"""Color of any text to be dispalyed"""

PIXEL_PITCH: int = 6
"""Center to center pixel distance, in mm"""

##############################################
## Peripherals
##############################################
display = None
"""The display that is being used"""

##############################################
## Program states
##############################################
program: int = 0
"""The program number that is running"""

mode: int = 0
"""The mode numbner that is selected"""

snake: int = None
"""Snake program state"""

ball: int = None
"""Ball program state"""

display_image: int = None
"""Image program stage"""
