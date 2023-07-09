from threading import Thread
import time
import src.data.state as state

try:
    import RPi.GPIO as GPIO
except:
    print("Could not import RPi.GPIO")

PRESS_GAP = 0.75

from gpiozero import Button

def program_button_press():
    button = Button(19)

    while True:
        if button.is_pressed:
            state.program += 1
            if state.program >= state.num_programs:
                state.program = 0

            print(f"Incrementing to program: {state.program+1} / {state.num_programs}")
            while button.is_pressed:
                time.sleep(0.01)
            time.sleep(0.1)


# def mode_button_press():
#     pin = 25

#     GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#     last_press = time.time()

#     while True:

#         if time.time() - last_press < PRESS_GAP:
#             continue

#         button_pressed = not GPIO.input(pin)

#         if not button_pressed:
#             continue

#         last_press = time.time()
    
#         state.mode += 1
#         if state.mode >= state.num_modes:
#             state.mode = 0

#         print(f"Incrementing to mode: {state.mode+1} / {state.num_modes}")


def start_buttons_thread():
    # GPIO.setmode(GPIO.BCM)
    threads_to_start = [program_button_press, program_button_press]

    for thread_to_start in threads_to_start:
        t1 = Thread(target=thread_to_start)
        t1.start()
