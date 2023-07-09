import src.data.state as state

from typing import List, Tuple

import pygame


class Simulate:
    width, height = (state.WIDTH, state.HEIGHT)

    # Size of each pixel
    scale = 15
    radius = scale // 2

    # Create the Pygame screen, adding extra space for the offset
    screen = pygame.display.set_mode((width * scale + scale, height * scale + scale))

    def display_matrix(self, pixels: List[List[Tuple[int, int, int]]]) -> None:
        """Given a led matrix, display it to the user using pygame"""

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