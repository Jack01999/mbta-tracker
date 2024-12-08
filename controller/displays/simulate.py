try:
    import pygame
except:
    print("Could not import pygame")


from controller.data import PixelDisplay, dimensions, validate_pixels
from controller.displays import DisplayProtocol


class Simulate(DisplayProtocol):

    def __init__(self):
        pygame.init()

        # Size of each pixel
        self.scale = 15
        self.radius = self.scale // 2

        # Create the Pygame screen, adding extra space for the offset
        # screen = None
        #
        # def start(self):
        self.screen = pygame.display.set_mode(
            (
                dimensions.width * self.scale + self.scale,
                dimensions.height * self.scale + self.scale,
            )
        )

    @validate_pixels
    def display_matrix(self, pixels: PixelDisplay) -> None:
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
