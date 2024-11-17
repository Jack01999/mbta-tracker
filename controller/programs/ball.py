from __future__ import annotations

import logging
import random
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller import Controller

import numpy as np

from controller.data import dimensions


class Ball:
    def __init__(self, controller: Controller):

        self.controller = controller
        self.ball_last_update = time.time()

        self.ball_frequency_hz = 10

        # ball_width:ball_height ratio must not be the same as width:height,
        # otherwise the animation will repeat every 1-4 loops
        self.ball_width = 4
        self.ball_height = 4

        self.ball_dx = 1
        self.ball_dy = 1

        self.ball_x_position = dimensions.width // 2 - self.ball_width
        self.ball_y_position = dimensions.height // 2 - self.ball_height

        self.ball_distance_traveled = 0  # in mm

        self.ball_color = (255, 255 // 2, 255 // 2)

    def update(self):
        # wait until it is time to update
        time_between = 1 / self.ball_frequency_hz
        time_delta = time.time() - self.ball_last_update
        if time_delta < time_between:
            # waiting rather than returning until the next loop iteration
            # to get an accuracte frequency
            time.sleep(time_between - time_delta)

        logging.info(
            f"ball bounce {time.time() - self.ball_last_update - time_between} seconds to slow"
        )

        pixels = np.zeros((dimensions.height, dimensions.width, 3), dtype=np.int32)

        # move
        self.ball_x_position += self.ball_dx
        self.ball_y_position += self.ball_dy

        # Draw the logo at the new position
        for i in range(self.ball_height):
            for j in range(self.ball_width):
                pixels[(self.ball_y_position + i) % dimensions.height][
                    (self.ball_x_position + j) % dimensions.width
                ] = self.ball_color

        # Check for bouncing
        if (
            self.ball_x_position <= 0
            or self.ball_x_position >= dimensions.width - self.ball_width
        ):
            self.ball_dx *= -1
            self.ball_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
        if (
            self.ball_y_position <= 0
            or self.ball_y_position >= dimensions.height - self.ball_height
        ):
            self.ball_dy *= -1
            self.ball_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

        # display the ball
        self.controller.display.display_matrix(pixels=pixels)

        # set marker for update
        self.ball_last_update = time.time()
