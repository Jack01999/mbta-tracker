import copy, datetime, random, requests, sys, time
import os
import numpy as np
import src.data.state as state

from PIL import Image
from threading import Thread
from src.algs import draw_character, draw_text, key_to_character
from src.displays.adafruit import AdaFruit
from src.data.fonts import default_font
from src.displays.simulate import Simulate
from typing import List, Tuple
from src.programs.mbta import display_train_arrival_times

try:
    import RPi.GPIO as GPIO
except:
    print("Could not import RPi.GPIO, are you running in simulate mode?")

def print_default_font(display):
    """Display the entire default font one page at a time,
    displaying each page for 1 second"""

    pixels = copy.deepcopy(state.background)

    col_index = 0
    row_index = 0

    for character in default_font.characters:
        # new row is needed for this character
        if col_index + character.width_px >= state.width:
            col_index = 0
            row_index += default_font.height_px + 1

        # new page is needed for this character
        if row_index + default_font.height_px >= state.height:
            display.display_matrix(pixels)
            time.sleep(1)

            # clear the page
            row_index = 0
            col_index = 0
            pixels = copy.deepcopy(state.background)

        pixels = draw_character(
            pixels,
            character,
            row_index + 1 if character.dropdown else row_index,
            col_index,
        )

        # move imaginary curser to the start of the next character
        col_index += character.width_px + 1

    display.display_matrix(pixels)
    time.sleep(1)


def strobe(display):
    # wait until it is time to flip the strobe on/off
    time_between = 1 / state.strobe_frequency_hz
    time_delta = time.time() - state.strobe_last_update
    if time_delta < time_between:
        # waiting rather than returning until the next loop iteration
        # to get an accuracte strobe frequency
        time.sleep(time_between - time_delta)

    print(f"strobe {time_delta - time_between} seconds to slow")

    # create strobe pattern
    if state.strobe_on:
        pixels = np.zeros((state.height, state.width, 3), dtype=np.int)
    else:
        pixels = np.full((state.height, state.width, 3), state.bit_depth, dtype=np.int)

    state.strobe_on = not state.strobe_on

    # display the strobe
    display.display_matrix(pixels=pixels)

    # set marker for this strobe transition
    state.strobe_last_update = time.time()


def ball_bounce(display):
    # wait until it is time to update
    time_between = 1 / state.ball_frequency_hz
    time_delta = time.time() - state.ball_last_update
    if time_delta < time_between:
        # waiting rather than returning until the next loop iteration
        # to get an accuracte strobe frequency
        time.sleep(time_between - time_delta)

    print(
        f"ball bounce {time.time() - state.ball_last_update - time_between} seconds to slow"
    )

    pixels = np.zeros((state.height, state.width, 3), dtype=np.int)

    # move
    state.ball_x_position += state.ball_dx
    state.ball_y_position += state.ball_dy

    state.ball_distance_traveled += (state.ball_dx**2 + state.ball_dy**2) ** 0.5 * state.pixel_pitch

    # draw text
    pixels = draw_text(
        pixels=pixels, lines=[f"{round(state.ball_distance_traveled/1000, 1)} m"]
    )

    # Draw the logo at the new position
    for i in range(state.ball_height):
        for j in range(state.ball_width):
            pixels[(state.ball_y_position + i) % state.height][
                (state.ball_x_position + j) % state.width
            ] = state.ball_color

    # Check for bouncing
    if (
        state.ball_x_position <= 0
        or state.ball_x_position >= state.width - state.ball_width
    ):
        state.ball_dx *= -1
        state.ball_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
    if (
        state.ball_y_position <= 0
        or state.ball_y_position >= state.height - state.ball_height
    ):
        state.ball_dy *= -1
        state.ball_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    # display the ball
    display.display_matrix(pixels=pixels)

    # set marker for update
    state.ball_last_update = time.time()


def display_image(display):
    # wait until next image
    if state.image_last_update + state.image_display_time > time.time():
        return

    # increment
    state.image_index = (state.image_index + 1) % len(state.images)

    display.display_matrix(state.images[state.image_index])

    state.image_last_update = time.time()


def buttons_press():
    GPIO.setmode(GPIO.BCM)

    def program_button_press():
        pin = 19

        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        while True:
            button_pressed = not GPIO.input(pin)

            if button_pressed:
                state.program = (state.program + 1) % state.num_programs

                print(f"Incrementing to program: {state.program+1}{state.num_programs}")
                time.sleep(0.25)  # remove flicker

    def mode_button_press():
        pin = 25

        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        while True:
            button_pressed = not GPIO.input(pin)

            if button_pressed:
                state.mode = (state.mode + 1) % state.num_modes

                print(f"Incrementing to mode: {state.mode+1}/{state.num_modes}")
                time.sleep(0.25)  # remove flicker

    program_button_thread = Thread(target=program_button_press)
    program_button_thread.start()

    mode_button_thread = Thread(target=mode_button_press)
    mode_button_thread.start()


if __name__ == "__main__":
    # Main function of the entire program

    # select display output and start button thread
    if len(sys.argv) > 1 and sys.argv[-1] == "simulate":
        display = Simulate()
    else:
        buttons_thread = Thread(target=buttons_press)
        buttons_thread.start()
        display = AdaFruit()

    try:
        print("Press CTRL-C to stop")

        state.num_programs = 5
        state.num_modes = 10

        times = []
        loop_num = 0
        while True:
            # try:
            start_time = time.time()
            
            if state.program == 0:
                print('api-key : ', api_key)
                display_train_arrival_times(display)
            elif state.program == 1:
                display_image(display)

            elif state.program == 2:
                print_default_font(display)

            elif state.program == 3:
                ball_bounce(display)

            elif state.program == 4:
                strobe(display)

            times.append(time.time() - start_time)
            times = times[-50:]
            loop_num += 1
            print("\nLoop: ", loop_num)
            print("Loops per second: ", len(times) / sum(times))

            # except Exception as e:
            #     print(e, "waiting 3 seconds and trying again")
            #     time.sleep(3)

    except KeyboardInterrupt:
        print("Exiting\n")
        sys.exit(0)
