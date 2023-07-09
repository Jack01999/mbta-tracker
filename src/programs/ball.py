import random
import numpy as np
from src.algs import draw_text
import src.data.state as state

import time


class Ball:
    def __init__(self):
        self.ball_last_update = time.time()

        self.ball_frequency_hz = 10

        # ball_width:ball_height ratio must not be the same as width:height,
        # otherwise the animation will repeat every 1-4 loops
        self.ball_width = 4
        self.ball_height = 4

        self.ball_dx = 1
        self.ball_dy = 1

        self.ball_x_position = state.WIDTH // 2 - self.ball_width
        self.ball_y_position = state.HEIGHT // 2 - self.ball_height

        self.ball_distance_traveled = 0  # in mm

        self.ball_color = (state.BIT_DEPTH, state.BIT_DEPTH // 2, state.BIT_DEPTH // 2)

    def update(self):
        # wait until it is time to update
        time_between = 1 / self.ball_frequency_hz
        time_delta = time.time() - self.ball_last_update
        if time_delta < time_between:
            # waiting rather than returning until the next loop iteration
            # to get an accuracte strobe frequency
            time.sleep(time_between - time_delta)

        print(
            f"ball bounce {time.time() - self.ball_last_update - time_between} seconds to slow"
        )

        pixels = np.zeros((state.HEIGHT, state.WIDTH, 3), dtype=np.int)

        # move
        self.ball_x_position += self.ball_dx
        self.ball_y_position += self.ball_dy

        self.ball_distance_traveled += (
            self.ball_dx**2 + self.ball_dy**2
        ) ** 0.5 * state.pixel_pitch

        # draw text
        pixels = draw_text(
            pixels=pixels, lines=[f"{round(self.ball_distance_traveled/1000, 1)} m"]
        )

        # Draw the logo at the new position
        for i in range(self.ball_height):
            for j in range(self.ball_width):
                pixels[(self.ball_y_position + i) % state.HEIGHT][
                    (self.ball_x_position + j) % state.WIDTH
                ] = self.ball_color

        # Check for bouncing
        if (
            self.ball_x_position <= 0
            or self.ball_x_position >= state.WIDTH - self.ball_width
        ):
            self.ball_dx *= -1
            self.ball_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
        if (
            self.ball_y_position <= 0
            or self.ball_y_position >= state.HEIGHT - self.ball_height
        ):
            self.ball_dy *= -1
            self.ball_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

        # display the ball
        state.display.display_matrix(pixels=pixels)

        # set marker for update
        self.ball_last_update = time.time()


def ball():
    if state.ball is None:
        state.ball = Ball()
    state.ball.update()
