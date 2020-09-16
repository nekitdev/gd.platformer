__title__ = "gdplatformer"
__author__ = "NeKitDS, Sapfirenko"
__copyright__ = "Copyright 2020 NeKitDS, Sapfirenko"
__license__ = "MIT"
__version__ = "0.1.4"

import math
import time
import threading  # used for listening to events not related to keyboard
from typing import Union

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
    Left Shift  -> Lock/Unlock rotation on jump.
    Right Shift -> Enable/Disable NoClip.
    Left Ctrl   -> Get player size.
    Right Ctrl  -> Increment player size by 1.
    Right Alt   -> Decrement player size by 1.
"""

# process name, can be changed for different executable names, I guess
PROCESS_NAME = "GeometryDash"  # no need for ".exe"
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
memory = gd.memory.get_memory(PROCESS_NAME, load=False)
# noclip flag
noclip_enabled = False
# player rotation flag
rotation_unlocked = False
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


def reload_memory() -> bool:  # try to reload memory and return reload status
    try:
        memory.reload()
        return True
    except RuntimeError:
        return False


def listen_for_gd_closed(listener: Listener) -> bool:
    should_close = False

    while True:
        if reload_memory():
            should_close = False

        else:
            if should_close:
                break

            should_close = True

        time.sleep(0.1)

    listener.stop()


def on_press(key: Union[str, Key]) -> bool:  # handle key press
    global noclip_enabled, rotation_unlocked, speed_value

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

    elif key == Key.shift_l:  # if left shift was pressed
        # lock rotation if unlocked, unlock rotation if locked
        if rotation_unlocked:
            memory.player_lock_jump_rotation()
            print("Rotation is now locked.")
            rotation_unlocked = False
        else:
            memory.player_unlock_jump_rotation()
            print("Rotation is now unlocked.")
            rotation_unlocked = True

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

        speed_value = math.copysign(speed_values[speed_index], speed_value)
        color = colors[speed_index]  # pick color according to the speed

        if (
            memory.get_speed_value()
        ):  # if player is moving, we can update speed on the fly
            memory.set_speed_value(speed_value)  # set speed value

        print(
            color + f"Speed changed to #{speed_index} ({abs(speed_value)})" + Fore.RESET
        )

    elif key == Key.right:  # if right arrow was pressed
        speed_value = abs(speed_value)  # make speed value positive
        memory.set_speed_value(speed_value)  # set speed value

    elif key == Key.left:  # if left arrow was pressed
        speed_value = -abs(speed_value)  # make speed value negative
        memory.set_speed_value(speed_value)  # set speed value

    else:  # other key
        pass  # do nothing


def on_release(key: Union[str, Key]) -> bool:
    if key in {Key.left, Key.right}:  # if left/right arrow was released
        memory.set_speed_value(0)  # set speed to 0

    else:  # other key
        pass  # do nothing


def main() -> None:
    print(info)  # show simple info
    print(how_to)  # show tutorial on what the keys do

    with Listener(on_press=on_press, on_release=on_release) as listener:
        # create memory reloading thread
        memory_reload_thread = threading.Thread(
            target=listen_for_gd_closed,
            args=(listener,),
            name="MemoryReloadThread",
            daemon=True,
        )

        print("Waiting for Geometry Dash...")

        while not reload_memory():  # wait until GD is opened
            time.sleep(1)

        print("Found Geometry Dash.")

        # start memory reloading thread
        memory_reload_thread.start()

        # lock player rotation on jump
        memory.player_lock_jump_rotation()
        print("Rotation is now locked.")

        # patch crash on dashing backwards (by cos8o)
        memory.write_bytes(gd.memory.Buffer[0xE9, 0xA7, 0x00], 0x1EEB92)
        print("Patched crash on dashing backwards.")

        # join the listener into main thread, waiting for it to stop
        listener.join()
        memory_reload_thread.join()

        print("Geometry Dash is closed.")


if __name__ == "__main__":
    main()
