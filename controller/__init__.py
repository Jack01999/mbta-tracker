import sys
from typing import Union

import numpy as np

from controller.displays.adafruit import AdaFruit
from controller.displays.simulate import Simulate
from controller.programs.ball import Ball
from controller.programs.mbta import Mbta
from controller.programs.snake import Snake
from controller.sim_keyboard import SimKeyboard

DisplayType = Union[Simulate, AdaFruit]


def args_to_display() -> DisplayType:
    """"""
    if len(sys.argv) > 1 and sys.argv[1] == "simulate":
        return Simulate()
    return AdaFruit()


class Controller:
    def __init__(self):

        self.program = 0
        self.mode = 0

        self.display = args_to_display()
        self.mbta = Mbta(self)
        self.ball = Ball(self)
        self.snake = Snake()
        self.keyboard = SimKeyboard()

    def start(self):
        self._main_loop()

    def _main_loop(self):

        self.keyboard.start()

        self.mbta.start()
        self.ball.start()
        self.snake.start()

        pixels = None
        programs = [self.mbta, self.ball, self.snake]

        while True:
            i = self.keyboard.button_a_index % len(programs)
            if i == 0:
                p = self.mbta.pixels
            elif i == 1:
                p = self.ball.pixels
            elif i == 2:
                p = self.snake.pixels
            else:
                raise ValueError("Unknown program")

            if pixels is None or not np.array_equal(p, pixels):
                self.display.display_matrix(p)
                pixels = p

            pixels = p
            # time.sleep(1)
