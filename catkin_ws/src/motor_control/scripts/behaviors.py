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

def sleep_interruptibly(total_duration, stop_event, interval=0.02):
    elapsed = 0
    while elapsed < total_duration:
        if stop_event.is_set():
            break
        time.sleep(interval)
        elapsed += interval

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

def waveFrontToBackSync(cycles, each_leg_duration, speed, fade_in, fade_out, stop_event):
    extend_pairs = [
        [(serial61, 'e1'), (serial61, 'e2')],  # 6 + 1 (front)
        [(serial45, 'e2'), (serial23, 'e1')],  # 5 + 2 (middle)
        [(serial45, 'e1'), (serial23, 'e2')],  # 4 + 3 (rear)
    ]

    retract_pairs = [
        [(serial61, 'r1'), (serial61, 'r2')],
        [(serial45, 'r2'), (serial23, 'r1')],
        [(serial45, 'r1'), (serial23, 'r2')],
    ]

    total_pairs = len(extend_pairs)

    for cycle in range(cycles):
        if stop_event.is_set():
            print("Wave behavior interrupted before cycle.")
            return

        print(f"\nCycle {cycle + 1} of {cycles} — Extending Wave")

        if cycle < 3:
            extend_duration = each_leg_duration // 2
            retract_duration = each_leg_duration
            extend_speed = min(255, int(speed * 2.5))
        else:
            extend_duration = each_leg_duration
            retract_duration = each_leg_duration
            extend_speed = speed

        delay_between_pairs_ext = extend_duration / total_pairs / 1000.0
        delay_between_pairs_ret = retract_duration / total_pairs / 1000.0

        # Extension phase
        for i in range(total_pairs):
            if stop_event.is_set():
                print("Wave behavior interrupted during extension.")
                return
            for serial_x, cmd in extend_pairs[i]:
                send_command(serial_x, cmd, extend_duration, extend_speed, fade_in, fade_out)
            sleep_interruptibly(delay_between_pairs_ext, stop_event)

        print(f"Cycle {cycle + 1} of {cycles} — Retracting Wave")

        # Retraction phase
        for i in range(total_pairs):
            if stop_event.is_set():
                print("Wave behavior interrupted during retraction.")
                return
            for serial_x, cmd in retract_pairs[i]:
                send_command(serial_x, cmd, retract_duration, speed, fade_in, fade_out)
            sleep_interruptibly(delay_between_pairs_ret, stop_event)

    print("\nFinal full retract of all legs...")
    retractAll(duration=1500, speed=100, fade_in=fade_in, fade_out=fade_out, stop_event=stop_event)

# Optionally, export a list or dict of behaviors for auto-registration
ALL_BEHAVIORS = {
    "waveFrontToBackSync": partial(waveFrontToBackSync, cycles= 20, each_leg_duration=750, speed=100, fade_in=100, fade_out=100),
    "extendRightSync": partial(extendRightSync, duration=1500, speed=125, fade_in=0, fade_out=0),
    "extendLeftSync": partial(extendLeftSync, duration=1500, speed=125, fade_in=0, fade_out=0),
    "retractAll": partial(retractAll, duration=1500, speed=100, fade_in=0, fade_out=0),
    "extendLeftRightLeft": partial(extendLeftRightLeft, duration=800, speed=255, fade_in=100, fade_out=100)
}

__all__ = ['ALL_BEHAVIORS', 'retractAll']
