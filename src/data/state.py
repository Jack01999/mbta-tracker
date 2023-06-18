import copy
import time
import numpy as np
from typing import List, Tuple
from src.data.types import LedMatrix

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
"""The background of the led_matrix (`state.led_matrix`). 

See `datamodels.types.LedMatrix.pixels` for a reference.
"""

led_matrix: LedMatrix = LedMatrix(
    pixels=copy.deepcopy(background),
)
"""led matrix that is to be dispalyed"""

text_color: Tuple[int, int, int] = (bit_depth, bit_depth // 2, 0)
"""Color of any text to be dispalyed"""


##############################################
## Strobe Program
##############################################
last_strobe_time = time.time()

strobe_on = False

strobe_frequency_hz = 10

##############################################
## Ball Bounce Program
##############################################

update_frequency_hz = 30
last_ball_update = time.time()

logo_width = 4
logo_height = 4

dx = 1
dy = 1

x_pos = 10
y_pos = 10

logo_color = (bit_depth, bit_depth // 2, bit_depth//2)


