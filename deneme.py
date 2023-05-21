import threading
import time

flag = 0

def event_handler():
    global flag
    # Code to handle the event
    # Set the flag when the event occurs
    flag = True

    # Start a timer to clear the flag after 0.2 seconds
    timer = threading.Timer(0.2, clear_flag, args=(flag,))
    timer.start()

def clear_flag(flag1):
    global flag
    # Code to clear the flag
    print("timer timout")
    flag = False

# Example usage
for _ in range(5):  # Simulate multiple event occurrences
    event_handler()

    # Wait for a while (0.2 seconds or more) to simulate the elapsed time
    time.sleep(0.1)

    # Check the flag value after the elapsed time
    if flag:
        print("Flag is set.")
    else:
        print("Flag is cleared.")
