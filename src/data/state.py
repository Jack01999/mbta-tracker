import copy
import time
import numpy as np
from typing import List, Tuple

##############################################
## Could be refered to as "initial settiings"
##############################################
bit_depth: int = 255
"""The depth of each color (r, g, b).

ex: 255 is white, 1 is black
"""

height: int = 32
"""Height (rows) of the matrix in pixels."""

width: int = 64
"""Width (columns) of the matrix in pixels."""

background: List[List[Tuple[int, int, int]]] = np.zeros(
    (height, width, 3), dtype=np.int
)
# background = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)
""" The background of the led_matrix (`state.led_matrix`). 
"""

led_matrix: List[List[Tuple[int, int, int]]] = copy.deepcopy(background)
""" led matrix that is to be dispalyed.

    A 2d list ([x0, x1, ...],[y0, y1, ...]), each containing an (r, g, b) color.
    Starting in the upper left most corner, incremending down and to the right.
"""

text_color: Tuple[int, int, int] = (bit_depth, bit_depth // 2, 0)
"""Color of any text to be dispalyed"""


##############################################
## Strobe Program
##############################################
strobe_frequency_hz = 10

strobe_on = False

strobe_last_update = time.time()


##############################################
## Ball Bounce Program
##############################################
ball_last_update = time.time()

ball_frequency_hz = 10

ball_width = 6
ball_height = 3

ball_dx = 1
ball_dy = 1

ball_x_position = width // 2 - ball_width
ball_y_position = height // 2 - ball_height

ball_color = (bit_depth, bit_depth // 2, bit_depth // 2)
