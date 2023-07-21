import numpy as np
import src.data.state as state
from src.algs import draw_text
from typing import List


def display_error(error: List[str]):
    pixels = np.zeros((state.HEIGHT, state.WIDTH, 3), dtype=np.int)
    pixels = draw_text(pixels=pixels, lines=error)
    state.display.display_matrix(pixels=pixels)
