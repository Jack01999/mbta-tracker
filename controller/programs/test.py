from __future__ import annotations

import time
from threading import Thread
from typing import TYPE_CHECKING

from controller.data import PixelDisplay, default_font_raw, draw_lines_on, str_to_lines

if TYPE_CHECKING:
    from controller import Controller

import numpy as np
import logging

logger = logging.getLogger(__name__)

from controller.data import dimensions


class Test:
    _BG = np.zeros((dimensions.height, dimensions.width, 3), dtype=np.int32)

    def __init__(self, controller: Controller):
        self.controller = controller
        self._pixels = self._BG.copy()

    @property
    def pixels(self) -> PixelDisplay:
        """Return a copy of pixels."""
        return self._pixels

    def start(self):
        """Polling method placeholder."""
        Thread(target=self._main_loop, daemon=True).start()

    def _main_loop(self):
        """Main loop for the ball program."""

        word = "".join(default_font_raw.keys())
        lines = str_to_lines(word)
        logger.info(f"Testing lines: {lines}")

        while True:
            for i in range(0, len(lines), 4):
                self._pixels = draw_lines_on(
                    pixels=self._BG.copy(), lines=lines[i : i + 4]
                )
                time.sleep(2)
