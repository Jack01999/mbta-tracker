import sys
import time
from asyncio import new_event_loop
from typing import Union

import numpy as np

from controller.displays.adafruit import AdaFruit
from controller.displays.simulate import Simulate
from controller.programs.ball import Ball
from controller.programs.clock import Clock
from controller.programs.mbta import Mbta
from controller.programs.snake import Snake
from controller.programs.test import Test
from controller.sim_keyboard import SimKeyboard

DisplayType = Union[Simulate, AdaFruit]


class Controller:
    def __init__(self):

        self.simulate = len(sys.argv) > 1 and sys.argv[1] == "simulate"

        self._program = 0
        self.mode = 0

        self.display = Simulate() if self.simulate else AdaFruit()
        self.clock = Clock(self)
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

        self.clock.start()
        self.mbta.start()
        self.ball.start()
        self.snake.start()
        self.test.start()

        pixels = None
        programs = [self.clock, self.mbta, self.ball, self.snake, self.test]

        s_delta = 10
        p_time = time.monotonic()

        while True:

            c_time = time.monotonic()
            if c_time - p_time > s_delta:
                self._program = (self._program + 1) % len(programs)
                p_time = c_time

            new_pixels = programs[self._program].pixels

            if pixels is None or not np.array_equal(pixels, new_pixels):
                pixels = new_pixels
                self.display.display_matrix(pixels=pixels)

            time.sleep(0.01)
