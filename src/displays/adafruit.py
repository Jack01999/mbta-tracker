import argparse
import sys
import os
import time

import numpy as np
from PIL import Image
from src.data.types import LedMatrix
from src.algs import draw_character, key_to_character
import src.data.state as state

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except:
    print("Failed to import afafruit rgbmatrix")

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))


class AdaFruit(object):
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument(
            "-r",
            "--led-rows",
            action="store",
            # help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32",
            help=f"Display rows. 16 for 16x32, 32 for 32x32. Default: {state.height}",
            default=state.height,
            type=int,
        )
        self.parser.add_argument(
            "--led-cols",
            action="store",
            # help="Panel columns. Typically 32 or 64. (Default: 64)",
            help=f"Panel columns. Typically 32 or 64. (Default: {state.width})",
            default=state.width,
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
            default="adafruit-hat-pwm",
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
            help="Slow down writing to GPIO. Range: 0..4. Default: 0",
            default=0,
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

        self.parser.add_argument(
            "--led-limit-refresh",
            action="store",
            help="Limit refresh rate to this frequency in Hz. Useful to keep a constant refresh rate on loaded system. 0=no limit. Default: 120",
            default=120,
            type=int,
        )
        self.parser.add_argument(
            "--led-pwm-dither-bits",
            action="store",
            help="Time dithering of lower bits.  Default: 0",
            default=0,
            type=int,
        )

        self.parser.set_defaults(drop_privileges=True)

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

        options.pwm_dither_bits = self.args.led_pwm_dither_bits
        options.limit_refresh_rate_hz = self.args.led_limit_refresh

        if self.args.led_show_refresh:
            options.show_refresh_rate = 1

        if self.args.led_slowdown_gpio != None:
            options.gpio_slowdown = self.args.led_slowdown_gpio
        if self.args.led_no_hardware_pulse:
            options.disable_hardware_pulsing = True
        if not self.args.drop_privileges:
            options.drop_privileges = False

        self.matrix = RGBMatrix(options=options)
        # self.offset_canvas = self.matrix.CreateFrameCanvas()

    def display_matrix(self, matrix_to_display: LedMatrix):
        print("8 ", time.time())

        # for row_count, row_value in enumerate(matrix_to_display.pixels):
        #     for col_count, col_value in enumerate(row_value):
        #         # print("9 ", time.time())
        #         self.offset_canvas.SetPixel(
        #             col_count, row_count, col_value[0], col_value[1], col_value[2]
        #         )
        
        # self.offset_canvas.SetPixels

        np_pixels = np.array(matrix_to_display.pixels, dtype=np.uint8)
        np_pixels_reshaped = np_pixels.reshape(32, 64, 3)
        img = Image.fromarray(np_pixels_reshaped)

        self.matrix.Clear()
        self.matrix.SetImage(img)


                # print("10 ", time.time())
        print("9 ", time.time())

        # self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)
        print("11 ", time.time())
