__title__ = "gdplatformer"
__author__ = "NeKitDS, Sapfirenko"
__copyright__ = "Copyright 2020 NeKitDS, Sapfirenko"
__license__ = "MIT"
__version__ = "0.1.0"

import time

from colorama import Fore  # type: ignore  # no typehints
import gd  # type: ignore  # no typehints
from pynput.keyboard import Key, Listener  # type: ignore  # no typehints

import colorama  # type: ignore  # no typehints

colorama.init()

info = f"""(c) {__copyright__}
    Geometry Dash Platformer Mod (GDPM) v{__version__}.
    Created using gd.py (https://github.com/NeKitDS/gd.py)
"""

how_to = """Controls:
    Right       -> Move forward.
    Left        -> Move back.
    Tab         -> Change speed.
    Right Shift -> Enable/Disable NoClip.
    Left Ctrl   -> Get player size.
    Right Ctrl  -> Increment player size by 1.
    Right Alt   -> Decrement player size by 1.
"""

print(info)
time.sleep(1)
print(how_to)

# setup colors for console
colors = [
    Fore.LIGHTYELLOW_EX,
    Fore.LIGHTBLUE_EX,
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTRED_EX,
]
# set default speed to normal speed
default_speed = gd.api.SpeedConstant.NORMAL.value
# create gd.py memory object, without loading it (loaded when running)
memory = gd.memory.get_memory(load=False)
# noclip flag
noclip_enabled = False
# size pricision, can be changed for more precise player size
size_precision = 1
# set speed value to default speed
speed_value = default_speed
# setup speed values
speed_values = [speed.value for speed in gd.api.SpeedConstant]

# try to remove 0.0 speed (SpeedConstant.NULL)
try:
    speed_values.remove(0.0)
except ValueError:
    pass


def signum(number: float) -> int:  # self explanatory, get sign of a number
    if number < 0:
        return -1
    elif number > 0:
        return 1
    else:
        return 0


def reload_memory() -> bool:  # try to reload memory and return reload status
    try:
        memory.reload()
        return True
    except RuntimeError:
        return False


def on_press(key: Key) -> bool:  # handle key press
    global noclip_enabled, speed_value

    size = round(memory.get_size(), size_precision)  # get current size
    # reflect speed value update (if went through speed changer)
    speed_value = round(memory.get_speed_value(), 1) or speed_value

    if key == Key.ctrl_l:  # if left ctrl was pressed -> print size
        print(f"Player size: {size}")

    elif key == Key.ctrl_r:  # if right ctrl was pressed
        # increment size
        memory.set_size(size + 1)
        print(f"Player size incremented by 1 ({size} -> {size + 1})")

    elif key == Key.alt_r:  # if right alt was pressed
        if size < 1:  # if size is too low -> send warning
            print(f"Player size is less than 1: {size}")
        else:  # otherwise, decrement size
            memory.set_size(size - 1)
            print(f"Player size decremented by 1 ({size} -> {size - 1})")

    elif key == Key.shift_r:  # if right shift was pressed
        # disable noclip if enabled, enable noclip if disabled
        if noclip_enabled:
            memory.disable_noclip()
            print("NoClip is now disabled.")
            noclip_enabled = False

        else:
            memory.enable_noclip()
            print("NoClip is now enabled.")
            noclip_enabled = True

    elif key == Key.tab:  # if tab was pressed
        try:
            speed_index = speed_values.index(
                abs(speed_value)
            )  # get current speed index
        except ValueError:  # just in case
            speed_index = 0

        speed_index = (speed_index + 1) % len(
            speed_values
        )  # get next value (jump back if last)

        speed_value = signum(speed_value) * speed_values[speed_index]
        color = colors[speed_index]  # pick color according to the speed

        if (
            memory.get_speed_value()
        ):  # if player is moving, we can update speed on the fly
            memory.set_speed_value(speed_value)  # set speed value

        print(
            color
            + f"Speed changed to #{speed_index} ({abs(speed_value)})"
            + Fore.RESET
        )

    elif key == Key.right:  # if right arrow was pressed
        speed_value = abs(speed_value)  # make speed value positive
        memory.set_speed_value(speed_value)  # set speed value

    elif key == Key.left:  # if left arrow was pressed
        speed_value = -abs(speed_value)  # make speed value negative
        memory.set_speed_value(speed_value)  # set speed value

    else:  # other key
        pass  # do nothing

    return reload_memory()  # reload memory to check if GD is closed


def on_release(key) -> bool:
    if key in {Key.left, Key.right}:  # if left/right arrow was released
        memory.set_speed_value(0)  # set speed to 0

    else:  # other key
        pass  # do nothing

    return reload_memory()  # reload memory to check if GD is closed


with Listener(on_press=on_press, on_release=on_release) as listener:
    print("Waiting for Geometry Dash...")

    while not reload_memory():  # wait until GD is opened
        time.sleep(1)

    # join the listener into main thread, waiting for it to stop
    listener.join()

    print("Geometry Dash is closed.")
