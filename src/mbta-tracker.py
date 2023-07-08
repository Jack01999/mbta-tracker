import sys, time
from src.programs.display_image import display_image
from src.programs.ball import ball
import src.data.state as state

from threading import Thread
from src.displays.adafruit import AdaFruit
from src.programs.snake import snake
from src.programs.mbta import display_train_arrival_times
from src.programs.strobe import strobe


try:
    from src.displays.simulate import Simulate
except:
    print("Could not import pygame")

try:
    import RPi.GPIO as GPIO
except:
    print("Could not import RPi.GPIO, are you running in simulate mode?")


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

            state.program = 1

            if state.program == 0:
                display_train_arrival_times(display)

            elif state.program == 1:
                display_image(display)

            elif state.program == 2:
                print_default_font(display)

            elif state.program == 3:
                ball(display)

            elif state.program == 4:
                snake(display)

            elif state.program == 5:
                strobe(display)

            times.append(time.time() - start_time)
            times = times[-50:]
            loop_num += 1
            print("\nLoop: ", loop_num)
            print(f"Frequency: {round(len(times) / sum(times), 2)} Hz")

            # except Exception as e:
            #     print(e, "waiting 3 seconds and trying again")
            #     time.sleep(3)

    except KeyboardInterrupt:
        print("Exiting\n")
        sys.exit(0)
