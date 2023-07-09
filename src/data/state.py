import copy
import numpy as np

from typing import List, Tuple, Union


##############################################
## Could be refered to as settiings
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

text_color: Tuple[int, int, int] = (bit_depth, bit_depth // 2, 0)  # orange
"""Color of any text to be dispalyed"""

pixel_pitch: int = 6
"""Center to center pixel distance, in mm. """

from src.peripherals.adafruit import AdaFruit
from src.peripherals.simulate import Simulate

display: Union[AdaFruit, Simulate] = None
"""The display that is being used"""


##############################################
## Program manager
##############################################
from src.programs.ball import Ball
from src.programs.display_image import DisplayImage
from src.programs.snake import Snake
from src.programs.strobe import Strobe

program: int = 0
"""The program number that is running"""

mode: int = 0
"""the mode numbner that is selected"""

num_programs: int = 5
"""ex: 
        3 programs => [0, 1, 2] """

num_modes: int = 10
"""number of modes"""

##############################################
## Program states
##############################################

snake: Snake = None

strobe: Strobe = None

ball: Ball = None

display_image: DisplayImage = None
