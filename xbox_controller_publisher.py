#!/usr/bin/env python3
"""
Xbox Controller Publisher for ROS3

This script reads inputs from an Xbox controller via USB and publishes them to a ROS3 topic.
"""

import sys
import os
import time

# Add the ros3 Python module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ros3', 'lang', 'python'))
import ros3 as rose

from evdev import InputDevice, categorize, ecodes

# Button and axis mappings for Xbox controller (update these based on debug output)
BUTTON_MAP = {
    # Example mappings, update based on debug output
    304: "A",          # BTN_SOUTH
    305: "B",          # BTN_EAST
    307: "X",          # BTN_NORTH
    308: "Y",          # BTN_WEST
    310: "LB",         # BTN_TL
    311: "RB",         # BTN_TR
    314: "Back",       # BTN_SELECT
    315: "Start",      # BTN_START
    316: "Power",      # BTN_MODE
    317: "Left_Thumb", # BTN_THUMBL
    318: "Right_Thumb" # BTN_THUMBR
}

AXIS_MAP = {
    # Example mappings, update based on debug output
    0: "left_x",      # ABS_X
    1: "left_y",      # ABS_Y
    2: "lt",          # ABS_Z (Left Trigger)
    3: "right_x",     # ABS_RX
    4: "right_y",     # ABS_RY
    5: "rt",          # ABS_RZ (Right Trigger)
    16: "cross_x",    # ABS_HAT0X (D-pad left/right)
    17: "cross_y"     # ABS_HAT0Y (D-pad up/down)
}

def read_xbox_controller(device_path):
    try:
        gamepad = InputDevice(device_path)
        result = {
            "device": device_path,
            "buttons": {name: 0 for name in BUTTON_MAP.values()},
            "axes": {name: 0.0 for name in AXIS_MAP.values()}
        }
        try:
            for event in gamepad.read_loop():
                if event.type == ecodes.EV_KEY:
                    button_name = BUTTON_MAP.get(event.code, None)
                    if button_name:
                        result["buttons"][button_name] = event.value
                        print(f"Button: {button_name} = {event.value}")  # Debug print
                    else:
                        print(f"Unknown button code: {event.code}")  # Debug print
                elif event.type == ecodes.EV_ABS:
                    axis_name = AXIS_MAP.get(event.code, None)
                    if axis_name:
                        max_val = 32767 if event.code in (0, 1, 3, 4) else 255
                        normalized = event.value / max_val
                        if event.code in (16, 17):
                            normalized = event.value
                        result["axes"][axis_name] = normalized
                        print(f"Axis: {axis_name} = {normalized}")  # Debug print
                yield result
        except Exception as e:
            print(f"Error reading from {device_path}: {e}")
        finally:
            gamepad.close()
    except Exception as e:
        print(f"Error opening {device_path}: {e}")

def main():
    # Initialize the ROS3 node
    node = rose.Node("xbox_controller_publisher")

    # Create a publisher for the Xbox controller topic
    publisher = node.publisher("/xbox/controller", message_size=1024, rate=60)

    # Use the correct event device for your controller
    device_path = "/dev/input/event15"

    print("Xbox Controller Publisher Started")
    print(f"Attempting to read from {device_path}")

    # Initialize previous state
    previous_state = None

    # Main loop
    for inputs in read_xbox_controller(device_path):
        if inputs:
            if previous_state is None or inputs != previous_state:
                publisher.publish(inputs)
                print(f"Published: {inputs}")
                previous_state = inputs
        if not node.ok():
            break

    # Shutdown the node
    node.shutdown()

if __name__ == "__main__":
    main()
