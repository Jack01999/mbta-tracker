from abc import abstractmethod
from typing import List, Protocol, Tuple

from controller.data import PixelDisplay


class DisplayProtocol(Protocol):

    @abstractmethod
    def display_matrix(self, pixels: PixelDisplay) -> None:
        """"""
        raise NotImplementedError
