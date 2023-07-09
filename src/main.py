import sys, time
from src.peripherals.buttons import start_buttons_thread
from src.programs.display_image import display_image
from src.programs.ball import ball
import src.data.state as state

from threading import Thread
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
        state.program = 1

        if state.program == 0:
            display_train_arrival_times()

        # elif state.program == 1:
        #     display_image()

        elif state.program == 1:
            ball()

        elif state.program == 2:
            snake()

        elif state.program == 3:
            strobe()

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

    # Initialize hardware periphrals
    if len(sys.argv) > 1 and sys.argv[-1] == "simulate":
        from src.peripherals.simulate import Simulate
        state.display = Simulate()
    else:
        buttons_thread = Thread(target=start_buttons_thread)
        buttons_thread.start()
        state.display = AdaFruit()

    # run the programs
    main_loop()
