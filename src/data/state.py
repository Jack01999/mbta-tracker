import copy, time
import numpy as np

from PIL import Image
from typing import List, Tuple


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

pixel_pitch = 6

##############################################
## Program manager
##############################################

program = 0
"""The program number that is running"""

num_programs = 1
"""ex: 
        3 programs => [0, 1, 2] """

mode = 0
"""the mode numbner that is selected"""

num_modes = 50
"""number of modes"""

snake = None


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

# ball_width:ball_height ratio must not be the same as width:height,
# otherwise the animation will repeat every 1-4 loops
ball_width = 4
ball_height = 4

ball_dx = 1
ball_dy = 1

ball_x_position = width // 2 - ball_width
ball_y_position = height // 2 - ball_height

ball_distance_traveled = 0  # in mm

ball_color = (bit_depth, bit_depth // 2, bit_depth // 2)


##############################################
## Image Display Program
##############################################
def get_image(image_name):
    img = Image.open(f"src/data/images/{image_name}")
    img = img.resize((width, height))
    img = img.convert("RGB")
    return np.array(img)


images = [
    get_image("1.png"),
    get_image("2.png"),
    get_image("3.png"),
    get_image("4.png"),
    get_image("5.png"),
    get_image("6.png"),
    get_image("7.png"),
    get_image("gif_1/1.jpg"),
    get_image("gif_1/2.jpg"),
    get_image("gif_1/3.jpg"),
    get_image("gif_1/4.jpg"),
    get_image("gif_1/5.jpg"),
    get_image("gif_1/6.jpg"),
    get_image("gif_1/7.jpg"),
    get_image("gif_1/8.jpg"),
]

image_index = 0

image_display_time = 0.75
"""How many seconds each image will be displayd for"""

image_last_update = time.time()
