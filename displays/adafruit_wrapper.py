
# from displays.adafruit_driver import AdafruitDriver

class AdafruitWrapper(Adafruit):
    def __init__(self, *args, **kwargs):
        super(AdafruitWrapper, self).__init__(*args, **kwargs)

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        while True:
            for x in range(0, self.matrix.width):
                offset_canvas.SetPixel(x, x, 255, 255, 255)
                offset_canvas.SetPixel(offset_canvas.height - 1 - x, x, 255, 0, 255)

            for x in range(0, offset_canvas.width):
                offset_canvas.SetPixel(x, 0, 255, 0, 0)
                offset_canvas.SetPixel(x, offset_canvas.height - 1, 255, 255, 0)

            for y in range(0, offset_canvas.height):
                offset_canvas.SetPixel(0, y, 0, 0, 255)
                offset_canvas.SetPixel(offset_canvas.width - 1, y, 0, 255, 0)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

    # def display_matrix(matrix: LedMatrix) -> None:
    #     """Given a led matrix, display it to the user using matplotlib"""
    #     y, x = np.indices(matrix.pixels.shape[:2])
    #     #     x, y = matrix.width, matrix.height

    #     # flatten tuples into (r, g, b)
    #     colors = matrix.pixels.reshape(-1, 3) / matrix.bit_depth

    #     _, ax = plt.subplots(figsize=(8, 4), dpi=150)

    #     ax.set_xlim(-1, matrix.width_px)
    #     ax.set_ylim(-1, matrix.height_px)

    #     ax.scatter(x.ravel(), y.ravel(), c=colors, s=12)

    #     # led matrix starts at the top, plots start at the bottom
    #     ax.invert_yaxis()

    #     plt.show()


    # def draw_character(
    #     matrix: LedMatrix,
    #     character: Character,
    #     row_start: int,
    #     col_start: int,
    # ) -> LedMatrix:
    #     """Draw on, and return an led matrix. `row_start` and  `col__start`
    #     both start at zero and begin in the upper left corner"""

    #     row = row_start
    #     for px_row in character.character_value:
    #         col = col_start
    #         for i in range(character.width_px - 1, -1, -1):
    #             bit = (px_row >> i) & 1
    #             if bit:
    #                 # dot color, can make anything
    #                 matrix.pixels[row][col] = (230, 10, 0)

    #             col += 1
    #         row += 1

    #     return matrix


    # # example display
    # if __name__ == "__main__":
    #     # create background of different colors
    #     bit_depth = 255
    #     height = 32
    #     width = 64

    #     background = np.random.randint(
    #         bit_depth * 0.9,
    #         bit_depth,
    #         (height, width, 3),
    #     )

    #     led_matrix = LedMatrix(
    #         pixels=copy.deepcopy(background),
    #         bit_depth=bit_depth,
    #         height_px=height,
    #         width_px=width,
    #     )

    #     lines = ["Central SQ.", "Inbound 12", "Outbound 12"]
    #     row_index = 0
    #     for line in lines:
    #         col_index = 0
    #         for character_key in line:
    #             character = key_to_character(default_font, character_key)
    #             led_matrix = draw_character(
    #                 led_matrix,
    #                 character,
    #                 row_index + 1 if character.dropdown else row_index,
    #                 col_index,
    #             )
    #             col_index += character.width_px + 1
    #         row_index += default_font.height_px + 1
    #     display_matrix(led_matrix)

    #     # clear the background
    #     led_matrix.pixels = copy.deepcopy(background)

    #     col_index = 0
    #     row_index = 0

    #     # print every character of `default_cont`, making a new line/page if needed
    #     for character in default_font.characters:
    #         # new row is needed for this character
    #         if col_index + character.width_px >= led_matrix.width_px:
    #             col_index = 0
    #             row_index += default_font.height_px + 1

    #         # new page is needed for this character
    #         if row_index + default_font.height_px >= led_matrix.height_px + 5:
    #             # dispaly the page before clearing
    #             display_matrix(led_matrix)
    #             # clear the page
    #             row_index = 0
    #             col_index = 0
    #             led_matrix.pixels = copy.deepcopy(background)

    #         led_matrix = draw_character(
    #             led_matrix,
    #             character,
    #             row_index + 1 if character.dropdown else row_index,
    #             col_index,
    #         )

    #         # move imaginary curser over to the start of the next character
    #         col_index += character.width_px + 1

    #     display_matrix(led_matrix)
