import time
from threading import Thread
from typing import Union

try:
    from pynput import keyboard
except:
    print("Could not import pynput keyboard")

from controller.data import Duration


class SimKeyboard:

    _DEBOUNCE: Duration = 0.1

    def __init__(self):

        self.button_a_index = 0
        self.button_b_index = 0

        self._button_a_last_press = 0
        self._button_b_last_press = 0

    def start(self):
        Thread(target=self._listener, daemon=True).start()

    def _listener(self):
        """"""

        def pressed(key: Union[keyboard.Key, keyboard.KeyCode, None]):
            if key == keyboard.KeyCode.from_char("a"):
                self._button_a_press()
            elif key == keyboard.KeyCode.from_char("b"):
                self._button_b_press()
            else:
                print("Unknown key pressed")

        with keyboard.Listener(on_press=pressed) as listener:
            listener.join()

    def _button_a_press(self):
        """Increment the a button index by one"""
        curr_time = time.monotonic()
        if curr_time - self._button_a_last_press > self._DEBOUNCE:
            self.button_a_index += 1
            self._button_a_last_press = curr_time
            print(f"Button A pressed {self.button_a_index} times")

    def _button_b_press(self):
        """Increment the b button index by one"""
        curr_time = time.monotonic()
        if curr_time - self._button_b_last_press > self._DEBOUNCE:
            self.button_b_index += 1
            self._button_a_last_press = curr_time
            print(f"Button B pressed {self.button_b_index} times")
