import numpy as np

from typing import List, Tuple


##############################################
## Could be refered to as settiings
##############################################
BIT_DEPTH: int = 255
"""The depth of each color (r, g, b).

ex: 255 is white, 1 is black
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
"""Center to center pixel distance, in mm. """

##############################################
## Peripherals
##############################################
display = None
"""The display that is being used"""


##############################################
## Program manager
##############################################
# from src.programs.ball import Ball
# from src.programs.display_image import DisplayImage
# from src.programs.snake import Snake
# from src.programs.strobe import Strobe

program: int = 0
"""The program number that is running"""

mode: int = 0
"""the mode numbner that is selected"""

##############################################
## Program states
##############################################
snake: int = None

strobe: int = None

ball: int = None

display_image: int = None
