import sys, time
from src.programs.ball import ball
import src.data.state as state

from src.peripherals.adafruit import AdaFruit
from src.programs.snake import snake
from src.programs.mbta import display_train_arrival_times
from src.programs.strobe import strobe



def main_loop():
    times = []
    loop_num = 0
    while True:
        # try:
        start_time = time.time()

        state.program=2
        if state.program == 0:
            try:
                display_train_arrival_times()
            except:
                pass
            
        # elif state.program == 1:
        #     display_image()

        elif state.program == 1:
            ball()

        elif state.program == 2:
            snake()

        elif state.program == 3:
            strobe()
            
        elif state.program == 0:
            # that was the last program
            state.program = 1

        times.append(time.time() - start_time)
        times = times[-50:]
        loop_num += 1
        print("\nLoop: ", loop_num)
        print(f"Frequency: {round(len(times) / sum(times), 2)} Hz")

    # except Exception as e:
    #     print(e, "waiting 3 seconds and trying again")
    #     time.sleep(3)


if __name__ == "__main__":
    # Main function of the entire program
    from gpiozero import Button
    from signal import pause
    import time

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


    # Initialize hardware periphrals
    if len(sys.argv) > 1 and sys.argv[-1] == "simulate":
        from src.peripherals.simulate import Simulate
        state.display = Simulate()
    else:
        state.display = AdaFruit()

    # run the programs
    main_loop()
