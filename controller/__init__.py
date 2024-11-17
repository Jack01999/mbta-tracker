import logging
import sys
import time
from typing import Union

from controller.displays.adafruit import AdaFruit
from controller.displays.simulate import Simulate
from controller.programs.ball import Ball
from controller.programs.mbta import Mbta

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logging.basicConfig(level=logging.INFO)

DisplayType = Union[Simulate, AdaFruit]


def parse_display() -> DisplayType:
    """"""
    if len(sys.argv) > 1 and sys.argv[1] == "simulate":
        return Simulate()
    return AdaFruit()


class Controller:
    def __init__(self):

        self.display = parse_display()
        self.mbta = Mbta(self)
        self.ball = Ball(self)

        self.program = 0
        self.mode = 0

        self.button_a_index = 0
        self.button_b_index = 0

        self._button_a_last_press = 0
        self._button_b_last_press = 0

    def start(self):
        """ """
        self.main_loop()

    def button_a_press(self):
        """Increment the a button index by one"""
        curr_time = time.monotonic()
        if curr_time - self._button_a_last_press > 0.25:
            self.button_a_index += 1
            self._button_a_last_press = curr_time
            logging.info(f"Button A pressed {self.button_a_index} times")

    def button_b_press(self):
        """Increment the b button index by one"""
        curr_time = time.monotonic()
        if curr_time - self._button_b_last_press > 0.5:
            self.button_b_index += 1
            self._button_a_last_press = curr_time
            logging.info(f"Button B pressed {self.button_b_index} times")

    def main_loop(self):
        times = []
        loop_num = 0

        while True:
            start_time = time.time()

            try:
                self.mbta.display_train_arrival_times()

            except Exception as e:
                logging.exception("An unexpected error occurred: %s", e)
                time.sleep(1)

            times.append(time.time() - start_time)
            times = times[-50:]
            loop_num += 1
            logging.info("\nLoop: %s", loop_num)

            logging.info("Frequency: %s Hz", str(round(len(times) / sum(times), 2)))
