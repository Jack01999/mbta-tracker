import numpy as np
import src.data.state as state

import time


class Strobe:
    def __init__(self):
        self.strobe_frequency_hz = 10

        self.strobe_on = False

        self.strobe_last_update = time.time()

    def update(self, display):
        # wait until it is time to flip the strobe on/off
        time_between = 1 / self.strobe_frequency_hz

        time_delta = time.time() - self.strobe_last_update
        if time_delta < time_between:
            # waiting rather than returning until the next loop iteration
            # to get an accuracte strobe frequency
            time.sleep(time_between - time_delta)

        print(f"strobe {time_delta - time_between} seconds to slow")

        # create strobe pattern
        if self.strobe_on:
            pixels = np.zeros((state.height, state.width, 3), dtype=np.int)
        else:
            pixels = np.full(
                (state.height, state.width, 3), state.bit_depth, dtype=np.int
            )

        self.strobe_on = not self.strobe_on

        # display the strobe
        display.display_matrix(pixels=pixels)

        # set marker for this strobe transition
        self.strobe_last_update = time.time()


def strobe(display):
    if state.strobe is None:
        state.strobe = Strobe()
    state.strobe.update(display=display)
