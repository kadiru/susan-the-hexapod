import serial
import time
import math
import keyboard
import curses
import threading

from functools import partial

# Serial connections to each Arduino
serial45 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_24333313930351C05231-if00', 115200, timeout=1)
serial61 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313837351300250-if00', 115200, timeout=1)
serial23 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313637351115182-if00', 115200, timeout=1)

time.sleep(2)  # Give Arduinos time to reset

def send_command(serial_x, command, duration, speed, fade_in=50, fade_out=50):
    full_command = f"{command},{duration},{speed},{fade_in},{fade_out}"
    print(f"Sending: {full_command}")
    serial_x.write((full_command + '\n').encode('utf-8'))

def retractAll(duration, speed, fade_in, fade_out, stop_event):
    """
    Retracts all six legs in a specific sequence unless interrupted by stop_event.

    Args:
        duration (int): Duration in milliseconds for each movement.
        speed (int): Speed value (0–255).
        fade_in (int): Fade-in value (0–255).
        fade_out (int): Fade-out value (0–255).
        stop_event (threading.Event): Event to allow mid-cycle interrupt.
    """
    retract_commands = [
        (serial45, 'r1'),  # Leg 4
        (serial45, 'r2'),  # Leg 5
        (serial61, 'r1'),  # Leg 6
        (serial23, 'r2'),  # Leg 3
        (serial23, 'r1'),  # Leg 2
        (serial61, 'r2'),  # Leg 1
    ]

    print("Retracting all legs completely...")

    for serial_x, cmd in retract_commands:
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)

    # Final wait after all commands, also interruptible
    final_wait = duration / 1000.0
    waited = 0
    check_interval = 0.02
    while waited < final_wait:
        if stop_event.is_set():
            print("Retract operation interrupted during final wait.")
            for serial_x, cmd in retract_commands: # stop all actuators
                send_command(serial_x, cmd, 0, speed, 0, 0)
            return
        time.sleep(check_interval)
        waited += check_interval

def extendLeftSync(duration, speed, fade_in, fade_out, stop_event):
    commands = [
        (serial61, 'e2'),  # Leg 1 extend
        (serial23, 'e1'),  # Leg 2 extend
        (serial23, 'e2'),  # Leg 3 extend
        (serial45, 'r1'),  # Leg 4 retract
        (serial45, 'r2'),  # Leg 5 retract
        (serial61, 'r1'),  # Leg 6 retract
    ]

    print("Extending Left Side...")

    for serial_x, cmd in commands:
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)

    # Interruptible sleep
    total_sleep = duration / 1000.0
    sleep_step = 0.02
    elapsed = 0
    while elapsed < total_sleep:
        if stop_event.is_set():
            print("extendLeftSync sleep interrupted.")
            return
        time.sleep(sleep_step)
        elapsed += sleep_step
    
def extendRightSync(duration, speed, fade_in, fade_out, stop_event):
    commands = [
        (serial45, 'e1'),  # Leg 4 extend
        (serial45, 'e2'),  # Leg 5 extend
        (serial61, 'e1'),  # Leg 6 extend
        (serial23, 'r1'),  # Leg 2 retract
        (serial23, 'r2'),  # Leg 3 retract
        (serial61, 'r2'),  # Leg 1 retract
    ]

    print("Extending Right Side...")

    for serial_x, cmd in commands:
        if stop_event.is_set():
            print("extendRightSync operation interrupted.")
            return
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)

    # Interruptible sleep
    total_sleep = duration / 1000.0
    sleep_step = 0.02
    elapsed = 0
    while elapsed < total_sleep:
        if stop_event.is_set():
            print("extendRightSync sleep interrupted.")
            return
        time.sleep(sleep_step)
        elapsed += sleep_step

def extendLeftRightLeft(duration, speed, fade_in, fade_out, stop_event):
    print("extending Left...")
    extendLeftSync(duration, speed, fade_in, fade_out, stop_event)
    if stop_event.is_set():
        print("Interrupted after first left extension.")
        return

    print("extending Right...")
    extendRightSync(duration, speed, fade_in, fade_out, stop_event)
    if stop_event.is_set():
        print("Interrupted after right extension.")
        return

    print("extending Left again...")
    extendLeftSync(duration, speed, fade_in, fade_out, stop_event)
    if stop_event.is_set():
        print("Interrupted after second left extension.")
        return

    print("\nFinal full retract of all legs...")
    retractAll(duration=1000, speed=255, fade_in=fade_in, fade_out=fade_out, stop_event=stop_event)

# Optionally, export a list or dict of behaviors for auto-registration
ALL_BEHAVIORS = {
    "retractAll": partial(retractAll, duration=1500, speed=100, fade_in=0, fade_out=0),
    "extendLeftSync": partial(extendLeftSync, duration=1500, speed=100, fade_in=0, fade_out=0),
    "extendRightSync": partial(extendRightSync, duration=1500, speed=100, fade_in=0, fade_out=0),
    "extendLeftRightLeft": partial(extendLeftRightLeft, duration=800, speed=255, fade_in=100, fade_out=100)
}
