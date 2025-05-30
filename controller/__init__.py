import sys
import time
import logging
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s.%(funcName)s %(levelname)s: %(message)s",
    datefmt="%Y.%m.%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

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
        self.clock.start()
        self.mbta.start()
        self.ball.start()
        self.snake.start()
        self.test.start()

        pixels = None
        # Example list of programs; adjust as needed:
        programs = [self.mbta, self.clock, self.ball, self.snake, self.test]

        # Track the last seen counts from the keyboard
        last_button_a = 0
        last_button_b = 0

        while True:
            # If keyboard is available, check for new presses.
            if self.keyboard is not None:
                # When button A is pressed, switch programs.
                if self.keyboard.button_a_index > last_button_a:
                    last_button_a = self.keyboard.button_a_index
                    self._program = (self._program + 1) % len(programs)
                    logger.info(f"Switched program to index {self._program}")

                # When button B is pressed, print the count.
                if self.keyboard.button_b_index > last_button_b:
                    last_button_b = self.keyboard.button_b_index
                    logger.info(f"Button B pressed, count: {last_button_b}")
            # Update the display only if pixels change.
            new_pixels = programs[self._program].pixels
            if pixels is None or not np.array_equal(pixels, new_pixels):
                pixels = new_pixels
                self.display.display_matrix(pixels=pixels)

            time.sleep(0.005)
