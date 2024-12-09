from typing import List, Tuple

# Define colors as RGB tuples
W = (255, 255, 255)  # White
B = (0, 0, 0)  # Black


def draw_circle(radius: int, thickness: int) -> List[List[Tuple[int, int, int]]]:
    """
    Draws a circle of a given radius and thickness using the midpoint circle algorithm.

    The resulting circle is drawn on a square canvas with a black background and a white circle.
    The canvas is sized to fit the circle, and the circle is centered.

    Parameters:
        radius (int): The radius of the circle to be drawn.
        thickness (int): The thickness of the circle's line (how "thick" the perimeter appears).

    Returns:
        List[List[Tuple[int,int,int]]]: A 2D list (canvas) of RGB tuples representing the final drawing.
    """
    # Compute the canvas size to fit the circle.
    # For a circle of radius r, a canvas of size (2r+1) ensures the circle fits entirely.
    canvas_size = radius * 2 + 1

    # The center is set to the midpoint of the canvas
    center_x = canvas_size // 2
    center_y = canvas_size // 2

    # Initialize the canvas with the background color (black).
    canvas = [[B for _ in range(canvas_size)] for _ in range(canvas_size)]

    def plot_points(cx, cy, x, y, color):
        """
        Plots the eight symmetric points of a circle for the given (x, y) coordinate.
        Utilizing the 8-way symmetry of a circle, we only compute one octant and mirror the points.

        Parameters:
            cx (int): Center x-coordinate of the circle.
            cy (int): Center y-coordinate of the circle.
            x, y (int): A point on the circle relative to the center.
            color (Tuple[int,int,int]): The color to plot.
        """
        points = [
            (cx + x, cy + y),
            (cx - x, cy + y),
            (cx + x, cy - y),
            (cx - x, cy - y),
            (cx + y, cy + x),
            (cx - y, cy + x),
            (cx + y, cy - x),
            (cx - y, cy - x),
        ]

        # Plot each point if it lies within the canvas boundaries.
        for px, py in points:
            if 0 <= px < canvas_size and 0 <= py < canvas_size:
                canvas[py][px] = color

    # To achieve thickness, we draw multiple concentric circles:
    # Starting from the outer radius and decreasing until we've drawn 'thickness' number of circles.
    for r in range(radius, radius - thickness, -1):
        # Midpoint circle algorithm initialization:
        # Start at the top of the circle on the y-axis (x=0, y=r).
        x = 0
        y = r
        # Initial decision parameter p:
        # p < 0 means we're inside the circle boundary, p > 0 means outside.
        p = 1 - r

        # Plot the initial points
        plot_points(center_x, center_y, x, y, W)

        # Iterate through x until it meets y to draw the full quadrant
        while x < y:
            x += 1
            if p < 0:
                # Move in the x-direction only
                p += 2 * x + 1
            else:
                # Move both in x and y directions
                y -= 1
                p += 2 * (x - y) + 1

            # Plot the new points after the increment step
            plot_points(center_x, center_y, x, y, W)

    return canvas


if __name__ == "__main__":
    # Example usage:
    # Draw a circle with radius 6 and thickness 1
    result = draw_circle(radius=4, thickness=1)

    # Print out a simplified text-based representation:
    # 'W' for white pixels, 'B' for black pixels.
    for row in result:
        print("[" + ",".join(["W" if pixel == W else "B" for pixel in row]) + "],")
