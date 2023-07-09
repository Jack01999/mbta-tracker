from threading import Thread
import time
import src.data.state as state

try:
    import RPi.GPIO as GPIO
except:
    print("Could not import RPi.GPIO")


def program_button_press():
    pin = 19

    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        button_pressed = not GPIO.input(pin)

        if button_pressed:
            state.program += 1
            if state.program > state.num_programs:
                state.program = 0

            print(f"Incrementing to program: {state.program+1}/{state.num_programs}")
            time.sleep(0.5)  # remove flicker


def mode_button_press():
    pin = 25

    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        button_pressed = not GPIO.input(pin)

        if button_pressed:
            state.mode += 1
            if state.mode > state.num_modes:
                state.mode = 0

            print(f"Incrementing to mode: {state.mode+1}/{state.num_modes}")
            time.sleep(0.5)  # remove flicker


def start_buttons_thread():
    GPIO.setmode(GPIO.BCM)
    threads_to_start = [program_button_press, program_button_press]

    for thread_to_start in threads_to_start:
        t1 = Thread(target=thread_to_start)
        t1.start()
