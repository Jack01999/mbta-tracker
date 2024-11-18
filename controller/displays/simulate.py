from typing import List, Tuple

import pygame

from controller.data import PixelDisplay, dimensions
from controller.displays import DisplayProtocol


class Simulate(DisplayProtocol):

    # Size of each pixel
    scale = 15
    radius = scale // 2

    # Create the Pygame screen, adding extra space for the offset
    screen = pygame.display.set_mode(
        (dimensions.width * scale + scale, dimensions.height * scale + scale)
    )

    def display_matrix(self, pixels: PixelDisplay) -> None:
        """Given a led matrix, display it to the user using pygame"""
        print("Updating pygame display")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Fill the screen with black
        self.screen.fill((0, 0, 0))

        # Draw each pixel
        for y, row in enumerate(pixels):
            for x, color in enumerate(row):
                # Add the offset of radius to x and y coordinates
                pygame.draw.circle(
                    self.screen,
                    color,
                    ((x * self.scale + self.radius), (y * self.scale + self.radius)),
                    self.radius,
                )

        # Update the display
        pygame.display.flip()
