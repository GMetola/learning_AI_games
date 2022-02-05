import pyautogui
import datetime
import time
import numpy as np
from pynput import keyboard

key_pressed = None

def on_press(key):
    global key_listened
    if key == keyboard.Key.esc:
        key_pressed = key
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['1', '2', 'left', 'right']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)
        key_pressed = k

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread

amplitude = 27
now = datetime.datetime.now()
start = time.time()
i = 0
while key_pressed is None:
    killing_zone_x = np.random.randint(1720,1720+amplitude)
    killing_zone_y = np.random.randint(825,825+amplitude)
    pyautogui.doubleClick(killing_zone_x,killing_zone_y)
    time.sleep(0.000001)
    if i%50 == 0:
        pyautogui.leftClick(1772,599)
        print("New level?")
        print("Clicks per second: ", i*2/time.perf_counter())
    i += 1
    


listener.join()  # remove if main thread is polling self.keys
print("Program ended, seconds running: ", time.perf_counter())
