import numpy as np
import src.data.state as state
from src.algs import draw_text


def display_error():
    pixels = np.zeros((state.HEIGHT, state.WIDTH, 3), dtype=np.int)
    pixels = draw_text(pixels=pixels, lines=[f"Error"])
    state.display.display_matrix(pixels=pixels)
