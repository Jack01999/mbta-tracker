import argparse
import copy
import time
import sys
import os

import numpy as np
from datamodels.types import Character, LedMatrix
from data.fonts import default_font

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from rgbmatrix import RGBMatrix, RGBMatrixOptions


class AdafruitDriver(object):
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument(
            "-r",
            "--led-rows",
            action="store",
            help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32",
            default=64,
            type=int,
        )
        self.parser.add_argument(
            "--led-cols",
            action="store",
            help="Panel columns. Typically 32 or 64. (Default: 64)",
            default=32,
            type=int,
        )
        self.parser.add_argument(
            "-c",
            "--led-chain",
            action="store",
            help="Daisy-chained boards. Default: 1.",
            default=1,
            type=int,
        )
        self.parser.add_argument(
            "-P",
            "--led-parallel",
            action="store",
            help="For Plus-models or RPi2: parallel chains. 1..3. Default: 1",
            default=1,
            type=int,
        )
        self.parser.add_argument(
            "-p",
            "--led-pwm-bits",
            action="store",
            help="Bits used for PWM. Something between 1..11. Default: 11",
            default=11,
            type=int,
        )
        self.parser.add_argument(
            "-b",
            "--led-brightness",
            action="store",
            help="Sets brightness level. Default: 100. Range: 1..100",
            default=100,
            type=int,
        )
        self.parser.add_argument(
            "-m",
            "--led-gpio-mapping",
            help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm",
            choices=["regular", "regular-pi1", "adafruit-hat", "adafruit-hat-pwm"],
            default="adafruit-hat",
            type=str,
        )
        self.parser.add_argument(
            "--led-scan-mode",
            action="store",
            help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)",
            default=1,
            choices=range(2),
            type=int,
        )
        self.parser.add_argument(
            "--led-pwm-lsb-nanoseconds",
            action="store",
            help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130",
            default=130,
            type=int,
        )
        self.parser.add_argument(
            "--led-show-refresh",
            action="store_true",
            help="Shows the current refresh rate of the LED panel",
        )
        self.parser.add_argument(
            "--led-slowdown-gpio",
            action="store",
            help="Slow down writing to GPIO. Range: 0..4. Default: 1",
            default=1,
            type=int,
        )
        self.parser.add_argument(
            "--led-no-hardware-pulse",
            action="store_true",
            help="Don't use hardware pin-pulse generation",
        )
        self.parser.add_argument(
            "--led-rgb-sequence",
            action="store",
            help="Switch if your matrix has led colors swapped. Default: RGB",
            default="RGB",
            type=str,
        )
        self.parser.add_argument(
            "--led-pixel-mapper",
            action="store",
            help='Apply pixel mappers. e.g "Rotate:90"',
            default="",
            type=str,
        )
        self.parser.add_argument(
            "--led-row-addr-type",
            action="store",
            help="0 = default; 1=AB-addressed panels; 2=row direct; 3=ABC-addressed panels; 4 = ABC Shift + DE direct",
            default=0,
            type=int,
            choices=[0, 1, 2, 3, 4],
        )
        self.parser.add_argument(
            "--led-multiplexing",
            action="store",
            help="Multiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZStripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven... (Default: 0)",
            default=0,
            type=int,
        )
        self.parser.add_argument(
            "--led-panel-type",
            action="store",
            help="Needed to initialize special panels. Supported: 'FM6126A'",
            default="",
            type=str,
        )
        self.parser.add_argument(
            "--led-no-drop-privs",
            dest="drop_privileges",
            help="Don't drop privileges from 'root' after initializing the hardware.",
            action="store_false",
        )
        self.parser.set_defaults(drop_privileges=True)

    def usleep(self, value):
        time.sleep(value / 1000000.0)

    def run(self):
        print("Running")

    def process(self):
        self.args = self.parser.parse_args()

        options = RGBMatrixOptions()

        if self.args.led_gpio_mapping != None:
            options.hardware_mapping = self.args.led_gpio_mapping
        options.rows = self.args.led_rows
        options.cols = self.args.led_cols
        options.chain_length = self.args.led_chain
        options.parallel = self.args.led_parallel
        options.row_address_type = self.args.led_row_addr_type
        options.multiplexing = self.args.led_multiplexing
        options.pwm_bits = self.args.led_pwm_bits
        options.brightness = self.args.led_brightness
        options.pwm_lsb_nanoseconds = self.args.led_pwm_lsb_nanoseconds
        options.led_rgb_sequence = self.args.led_rgb_sequence
        options.pixel_mapper_config = self.args.led_pixel_mapper
        options.panel_type = self.args.led_panel_type

        if self.args.led_show_refresh:
            options.show_refresh_rate = 1

        if self.args.led_slowdown_gpio != None:
            options.gpio_slowdown = self.args.led_slowdown_gpio
        if self.args.led_no_hardware_pulse:
            options.disable_hardware_pulsing = True
        if not self.args.drop_privileges:
            options.drop_privileges = False

        self.matrix = RGBMatrix(options=options)

        try:
            # Start loop
            print("Press CTRL-C to stop sample")
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True


def draw_character(
    matrix: LedMatrix,
    character: Character,
    row_start: int,
    col_start: int,
) -> LedMatrix:
    """Draw on, and return an led matrix. `row_start` and  `col__start`
    both start at zero and begin in the upper left corner"""

    row = row_start
    for px_row in character.character_value:
        col = col_start
        for i in range(character.width_px - 1, -1, -1):
            bit = (px_row >> i) & 1
            if bit:
                matrix.pixels[row][col] = (
                    matrix.bit_depth,
                    matrix.bit_depth // 2,
                    0,
                )  # orange

            col += 1
        row += 1

    return matrix


class AdafruitWrapper(AdafruitDriver):
    def __init__(self, *args, **kwargs):
        super(AdafruitWrapper, self).__init__(*args, **kwargs)

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()

        bit_depth = 255
        height = 32
        width = 64

        background = np.random.randint(
            bit_depth * 0.9,
            bit_depth,
            (height, width, 3),
        )

        led_matrix = LedMatrix(
            pixels=copy.deepcopy(background),
            bit_depth=bit_depth,
            height_px=height,
            width_px=width,
        )

        def display_matrix(matrix: LedMatrix, offset_canvas):
            for row_count, row_value in enumerate(matrix.pixels):
                for col_count, col_value in enumerate(row_value):
                    offset_canvas.SetPixel(
                        row_count, col_count, col_value[0], col_value[1], col_value[2]
                    )

            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

        while True:
            # background = np.random.randint(
            #     0,
            #     255,
            #     (height, width, 3),
            # )

            background = np.zeros((height, width, 3), dtype=np.int)

            led_matrix = LedMatrix(
                pixels=copy.deepcopy(background),
                bit_depth=bit_depth,
                height_px=height,
                width_px=width,
            )
            # display_matrix(led_matrix, offset_canvas)
            # time.sleep(0.25)

            # clear the background
            led_matrix.pixels = copy.deepcopy(background)

            col_index = 0
            row_index = 0

            # print every character of `default_cont`, making a new line/page if needed
            for character in default_font.characters:
                # new row is needed for this character
                if col_index + character.width_px >= led_matrix.width_px:
                    col_index = 0
                    row_index += default_font.height_px + 1

                # new page is needed for this character
                if row_index + default_font.height_px >= led_matrix.height_px + 5:
                    # clear the page
                    row_index = 0
                    col_index = 0
                    led_matrix.pixels = copy.deepcopy(background)

                led_matrix = draw_character(
                    led_matrix,
                    character,
                    row_index + 1 if character.dropdown else row_index,
                    col_index,
                )

                # move imaginary curser over to the start of the next character
                col_index += character.width_px + 1

            display_matrix(led_matrix, offset_canvas)

            time.sleep(5)

            # for x in range(0, self.matrix.width):
            #     offset_canvas.SetPixel(x, x, 255, 255, 255)
            #     offset_canvas.SetPixel(offset_canvas.height - 1 - x, x, 255, 0, 255)

            # for x in range(0, offset_canvas.width):
            #     offset_canvas.SetPixel(x, 0, 255, 0, 0)
            #     offset_canvas.SetPixel(x, offset_canvas.height - 1, 255, 255, 0)

            # for y in range(0, offset_canvas.height):
            #     offset_canvas.SetPixel(0, y, 0, 0, 255)
            #     offset_canvas.SetPixel(offset_canvas.width - 1, y, 0, 255, 0)
            # offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
