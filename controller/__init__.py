import sys
from typing import Union

import numpy as np

from controller.displays.adafruit import AdaFruit
from controller.displays.simulate import Simulate
from controller.programs.ball import Ball
from controller.programs.mbta import Mbta
from controller.programs.snake import Snake
from controller.programs.test import Test
from controller.sim_keyboard import SimKeyboard

DisplayType = Union[Simulate, AdaFruit]


class Controller:
    def __init__(self):

        self.simulate = len(sys.argv) > 1 and sys.argv[1] == "simulate"

        self.program = 0
        self.mode = 0

        self.display = Simulate() if self.simulate else AdaFruit()
        self.mbta = Mbta(self)
        self.ball = Ball(self)
        self.snake = Snake()
        self.test = Test(self)
        self.keyboard = SimKeyboard() if self.simulate else None

    def start(self):
        self._main_loop()

    def _main_loop(self):

        # if isinstance(self.display, SimKeyboard):
        #     self.display.start()
        #     self.keyboard.start()

        self.mbta.start()
        self.ball.start()
        self.snake.start()
        self.test.start()

        pixels = None
        programs = [self.mbta, self.ball, self.snake, self.test]

        while True:
            i = self.keyboard.button_a_index % len(programs)
            if i == 0:
                new_pixels = self.mbta.pixels
            elif i == 1:
                new_pixels = self.ball.pixels
            elif i == 2:
                new_pixels = self.snake.pixels
            elif i == 3:
                new_pixels = self.test.pixels
            # else:
            #     raise ValueError("Unknown program")

            if pixels is None or not np.array_equal(pixels, new_pixels):
                pixels = new_pixels
                self.display.display_matrix(pixels=pixels)
