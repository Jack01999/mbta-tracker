import numpy as np
import src.data.state as state

from PIL import Image

import time


def get_image(image_name):
    img = Image.open(f"src/data/images/{image_name}")
    img = img.resize((state.width, state.height))
    img = img.convert("RGB")
    return np.array(img)


class DisplayImage:
    def __init__(self):
        self.images = [
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

        self.image_index = 0

        self.image_display_time = 0.75
        """How many seconds each image will be displayd for"""

        self.image_last_update = time.time()

    def update(self):
        # wait until next image
        if self.image_last_update + self.image_display_time > time.time():
            return

        # increment
        self.image_index = (self.image_index + 1) % len(self.images)

        state.display.display_matrix(self.images[self.image_index])

        self.image_last_update = time.time()


def display_image():
    if state.display_image is None:
        state.display_image = DisplayImage()
    state.display_image.update()
