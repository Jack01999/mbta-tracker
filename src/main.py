import sys, time
import traceback

from src.programs.ball import ball
import src.data.state as state

from src.peripherals.adafruit import AdaFruit
from src.programs.display_image import display_image
from src.programs.mbta import display_train_arrival_times
from src.programs.snake import snake

try:
    from gpiozero import Button
except:
    pass

def main_loop():
    times = []
    loop_num = 0
    while True:
        
        start_time = time.time()
        
        try:
            if state.program == 0:
                display_train_arrival_times()
            elif state.program == 1:
                display_image()
            elif state.program == 1:
                ball()
            elif state.program == 2:
                snake()
            elif state.program == 4:
                # that was the last program
                state.program = 1

        except Exception as e:
            traceback.print_exc()
            print(f"{e}, waiting a second and trying again.")
            time.sleep(1)

        times.append(time.time()- start_time)
        times = times[-50:]
        loop_num += 1
        print("\nLoop: ", loop_num)
        print("program: ", state.program)
        print("mode: ", state.mode)
        print(f"Frequency: {round(len(times) / sum(times), 2)} Hz")


if __name__ == "__main__":
    # Main function of the entire program

    # run the buttons
    button_1_pressed_time = 0
    button_2_pressed_time = 0

    def increment_program():
        global button_1_pressed_time
        current_time = time.time()

        if current_time - button_1_pressed_time > 0.5:
            state.program += 1
            print(f"Program {state.program}")
            button_1_pressed_time = current_time

    def increment_mode():
        global button_2_pressed_time
        current_time = time.time()

        if current_time - button_2_pressed_time > 0.5:
            state.mode += 1
            print(f"Mode  {state.mode}")

            if state.mode > 5:
                state.mode = 0
            button_2_pressed_time = current_time

    button_1 = Button(19)
    button_1.when_pressed = increment_program

    button_2 = Button(25)
    button_2.when_pressed = increment_mode

    # select the dipslay
    if len(sys.argv) > 1 and sys.argv[-1] == "simulate":
        from src.peripherals.simulate import Simulate
        state.display = Simulate()
    else:
        state.display = AdaFruit()

    # run the programs
    main_loop()
