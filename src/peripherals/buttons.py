from threading import Thread
import time
import src.data.state as state

try:
    import RPi.GPIO as GPIO
except:
    print("Could not import RPi.GPIO")

def button_press_callback(state, max_state, message):
    state += 1
    if state > max_state:
        state = 0
    print(message.format(state+1, max_state+1))
    time.sleep(0.5)
    return state

def program_button_press():
    pin = 19
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        time.sleep(0.01)
        GPIO.wait_for_edge(pin, GPIO.FALLING)
        state.program = button_press_callback(state.program, state.num_programs, "Incrementing to program: {}/{}")

def mode_button_press():
    pin = 25
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        time.sleep(0.01)
        GPIO.wait_for_edge(pin, GPIO.FALLING)
        state.mode = button_press_callback(state.mode, state.num_modes, "Incrementing to mode: {}/{}")

def start_buttons_thread():
    GPIO.setmode(GPIO.BCM)
    threads_to_start = [program_button_press, mode_button_press]

    for thread_to_start in threads_to_start:
        t1 = Thread(target=thread_to_start)
        t1.start()
