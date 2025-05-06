import serial
import time
import math
import keyboard
import curses

# Serial connections to each Arduino
serial45 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_24333313930351C05231-if00', 115200, timeout=1)
serial61 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313837351300250-if00', 115200, timeout=1)
serial23 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313637351115182-if00', 115200, timeout=1)

time.sleep(2)  # Give Arduinos time to reset

def send_command(serial_x, command, duration, speed, fade_in=50, fade_out=50):
    full_command = f"{command},{duration},{speed},{fade_in},{fade_out}"
    print(f"Sending: {full_command}")
    serial_x.write((full_command + '\n').encode('utf-8'))

def retractAllCompletely(duration, speed, fade_in, fade_out):
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

def pointLeftSequential(duration, speed, fade_in, fade_out):
    pair_sequence = [
        ((serial61, 'e2'), (serial61, 'r1')),  # Left front extend, right rear retract
        ((serial23, 'e1'), (serial45, 'r1')),  # Left middle extend, right front retract
        ((serial23, 'e2'), (serial45, 'r2')),  # Left rear extend, right middle retract
    ]

    delay_between_pairs = duration / len(pair_sequence) / 1000.0  # Equal spacing

    for (serial_left, cmd_left), (serial_right, cmd_right) in pair_sequence:
        send_command(serial_left, cmd_left, duration, speed, fade_in, fade_out)
        send_command(serial_right, cmd_right, duration, speed, fade_in, fade_out)
        time.sleep(delay_between_pairs)

def pointRightSequential(duration, speed, fade_in, fade_out):
    pair_sequence = [
        ((serial61, 'e1'), (serial61, 'r2')),  # Right front extend, left rear retract
        ((serial45, 'e2'), (serial23, 'r1')),  # Right middle extend, left front retract
        ((serial45, 'e1'), (serial23, 'r2')),  # Right rear extend, left middle retract
    ]

    delay_between_pairs = duration / len(pair_sequence) / 1000.0  # Equal spacing

    for (serial_right, cmd_right), (serial_left, cmd_left) in pair_sequence:
        send_command(serial_right, cmd_right, duration, speed, fade_in, fade_out)
        send_command(serial_left, cmd_left, duration, speed, fade_in, fade_out)
        time.sleep(delay_between_pairs)

def pointLeft(duration, speed, fade_in, fade_out):
    send_command(serial61, 'e2', duration, speed, fade_in, fade_out)
    send_command(serial23, 'e1', duration, speed, fade_in, fade_out)
    send_command(serial23, 'e2', duration, speed, fade_in, fade_out)
    send_command(serial45, 'r1', duration, speed, fade_in, fade_out)
    send_command(serial45, 'r2', duration, speed, fade_in, fade_out)
    send_command(serial61, 'r1', duration, speed, fade_in, fade_out)
    time.sleep(duration/1000.0)

def pointRight(duration, speed, fade_in, fade_out):
    send_command(serial45, 'e1', duration, speed, fade_in, fade_out)
    send_command(serial45, 'e2', duration, speed, fade_in, fade_out)
    send_command(serial61, 'e1', duration, speed, fade_in, fade_out)
    send_command(serial61, 'r2', duration, speed, fade_in, fade_out)
    send_command(serial23, 'r1', duration, speed, fade_in, fade_out)
    send_command(serial23, 'r2', duration, speed, fade_in, fade_out)
    time.sleep(duration/1000.0)

def retractRightSequential(duration, speed, fade_in, fade_out):
    right_retract_sequence = [
        (serial61, 'r1'),  # Right front
        (serial45, 'r2'),  # Right middle
        (serial45, 'r1'),  # Right rear
    ]

    delay_between_legs = duration / len(right_retract_sequence) / 1000.0  # Convert to seconds

    for serial_x, cmd in right_retract_sequence:
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(delay_between_legs)

def retractLeftSequential(duration, speed, fade_in, fade_out):
    left_retract_sequence = [
        (serial23, 'r2'),  # Left rear
        (serial23, 'r1'),  # Left middle
        (serial61, 'r2'),  # Left front
    ]

    delay_between_legs = duration / len(left_retract_sequence) / 1000.0  # Convert to seconds

    for serial_x, cmd in left_retract_sequence:
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(delay_between_legs)

def extendAllCompletely(duration, speed, fade_in, fade_out):
    extend_commands = [
        (serial61, 'e1'),  # Right rear
        (serial61, 'e2'),  # Left front
        (serial23, 'e1'),  # Left middle
        (serial23, 'e2'),  # Left rear
        (serial45, 'e1'),  # Right front
        (serial45, 'e2'),  # Right middle
    ]

    for serial_x, cmd in extend_commands:
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)

def prepPointLeftRightLeft(duration, speed, fade_in, fade_out):
    extendAllCompletely(duration, speed, fade_in, fade_out)

def pointLeftRightLeft(duration, speed, fade_in, fade_out):
    print("Pointing Left...")
    pointLeft(duration, speed, fade_in, fade_out)

    #time.sleep(duration/1000.0)  # small pause between transitions

    print("Pointing Right...")
    pointRight(duration, speed, fade_in, fade_out)

    #time.sleep(duration/1000.0)  # small pause between transitions

    print("Pointing Left again...")
    pointLeft(duration, speed, fade_in, fade_out)
    
    print("\nFinal full retract of all legs...")
    retractAllCompletely(duration=1000, speed=255, fade_in=fade_in, fade_out=fade_out)

def seqWave(duration, speed, delay_between_legs, fade_in, fade_out):
    wave_sequence = [
        (serial61, 'e2'), (serial23, 'e1'), (serial23, 'e2'),
        (serial45, 'e1'), (serial45, 'e2'), (serial61, 'e1')
    ]
    retract_sequence = [
        (serial61, 'r2'), (serial23, 'r1'), (serial23, 'r2'),
        (serial45, 'r1'), (serial45, 'r2'), (serial61, 'r1')
    ]
    for serial_x, cmd in wave_sequence:
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(delay_between_legs / 1000.0)
    time.sleep((duration + 100) / 1000.0)
    for serial_x, cmd in retract_sequence:
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(delay_between_legs / 1000.0)
    time.sleep((duration + 100) / 1000.0)

def seqWaveFrontToBackSymmetricalSides(duration, speed, delay_between_pairs, fade_in, fade_out):
    wave_pairs = [
        # (Left leg, Right leg)
        [(serial45, 'e1'), (serial23, 'e2')],  # 4 + 3
        [(serial45, 'e2'), (serial23, 'e1')],  # 5 + 2
        [(serial61, 'e1'), (serial61, 'e2')],  # 6 + 1
    ]

    retract_pairs = [
        [(serial45, 'r1'), (serial23, 'r2')],
        [(serial45, 'r2'), (serial23, 'r1')],
        [(serial61, 'r1'), (serial61, 'r2')],
    ]

    for pair in wave_pairs:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(delay_between_pairs / 1000.0)

    #time.sleep((duration + 100) / 1000.0)

    for pair in retract_pairs:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(delay_between_pairs / 1000.0)

    time.sleep((duration + 100) / 1000.0)

def seqWaveFrontToBackSymmetricalSides_looped(cycles, base_duration, speed, fade_in, fade_out):
    wave_pairs = [
        [(serial45, 'e1'), (serial23, 'e2')],  # 4 + 3 (front)
        [(serial45, 'e2'), (serial23, 'e1')],  # 5 + 2 (middle)
        [(serial61, 'e1'), (serial61, 'e2')],  # 6 + 1 (rear)
    ]

    retract_pairs = [
        [(serial45, 'r1'), (serial23, 'r2')],
        [(serial45, 'r2'), (serial23, 'r1')],
        [(serial61, 'r1'), (serial61, 'r2')],
    ]

    total_pairs = len(wave_pairs)

    for cycle in range(cycles):
        print(f"\nCycle {cycle + 1} of {cycles} — Extending Wave")

        # First 3 cycles: fast extension, slower retraction
        if cycle < 3:
            extend_duration = base_duration // 2
            retract_duration = base_duration
            extend_speed = min(255, speed * 2.5)
        else:
            extend_duration = base_duration
            retract_duration = base_duration
            extend_speed = speed

        delay_between_pairs_ext = extend_duration / total_pairs / 1000.0
        delay_between_pairs_ret = retract_duration / total_pairs / 1000.0

        # Extension phase
        for i in range(total_pairs):
            pair = wave_pairs[i]
            for serial_x, cmd in pair:
                send_command(serial_x, cmd, extend_duration, extend_speed, fade_in, fade_out)
            time.sleep(delay_between_pairs_ext)

        print(f"Cycle {cycle + 1} of {cycles} — Retracting Wave")
        for i in range(total_pairs):
            pair = retract_pairs[i]
            for serial_x, cmd in pair:
                send_command(serial_x, cmd, retract_duration, speed, fade_in, fade_out)
            time.sleep(delay_between_pairs_ret)

    print("\nFinal full retract of all legs...")
    retractAllCompletely(duration=1000, speed=255, fade_in=fade_in, fade_out=fade_out)

def execute_behavior_by_id(behavior_id, duration, speed, fade_in, fade_out):
    if behavior_id == "0":
        retractAllCompletely(1200, 255, 200, 200)   
    if behavior_id == "1":
        seqWave(duration, speed, 150, fade_in, fade_out)
    elif behavior_id == "2":
        seqWaveFrontToBackSymmetricalSides(duration, speed, 150, fade_in, fade_out)
    elif behavior_id == "3":
        seqWaveFrontToBackSymmetricalSides_looped(20,duration,100,fade_in,fade_out)
    elif behavior_id == "4":
        pointLeftSequential(duration, 255, fade_in, fade_out)
    elif behavior_id == "5":
        pointRightSequential(duration, 255, fade_in, fade_out)
    elif behavior_id == "6":
        retractRightSequential(duration, 255, fade_in, fade_out)
    elif behavior_id == "7":
        retractLeftSequential(duration, 255, fade_in, fade_out)
    elif behavior_id == "8":
        extendAllCompletely(1200, 255, 200, 200)
    elif behavior_id == "9":
        prepPointLeftRightLeft(1500, 90, 40, 40)
    elif behavior_id == "10":
        pointLeftRightLeft(400, 255, 100, 100)
    else:
        print("Invalid behavior ID")

# Behavior list
behaviors = [
    lambda: pointLeft(500, 127, 50, 50),
    lambda: pointRight(500, 127, 50, 50),
    lambda: pointLeft(500, 127, 50, 50)
]

current_index = 0
paused = False

def play_behavior(index):
    if 0 <= index < len(behaviors):
        print(f"\nPlaying behavior {index + 1}/{len(behaviors)}")
        behaviors[index]()

import curses
import time

def behavior_playback_control(stdscr):
    # List of behaviors to cycle through
    behaviors = [
        "Sequential Wave",
        "Sequential Wave Front to Back Symmetrical Sides",
        "Point Left Sequential",
        "Point Right Sequential",
        "Retract Left Sequential",
        "Retract Right Sequential"
    ]

    # Initialize the current behavior index and state
    behavior_index = 0
    playing = True

    # Setup for the terminal
    stdscr.clear()
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input mode

    while True:
        # Display the current behavior
        stdscr.clear()
        stdscr.addstr(0, 0, f"Current Behavior: {behaviors[behavior_index]}")
        stdscr.addstr(1, 0, "Press right arrow to play next behavior")
        stdscr.addstr(2, 0, "Press left arrow to play previous behavior")
        stdscr.addstr(3, 0, "Press 'space' to pause/resume current behavior")
        stdscr.addstr(4, 0, "Press 'q' to quit playback")
        
        if not playing:
            stdscr.addstr(5, 0, "Playback is paused... Press 'space' to resume.")
        else:
            stdscr.addstr(5, 0, "Playback is running... Press 'space' to pause.")

        # Refresh the screen to update the text
        stdscr.refresh()

        # Wait for a key press (non-blocking)
        key = stdscr.getch()

        if key == curses.KEY_RIGHT:  # Right arrow key
            behavior_index = (behavior_index + 1) % len(behaviors)
        elif key == curses.KEY_LEFT:  # Left arrow key
            behavior_index = (behavior_index - 1) % len(behaviors)
        elif key == ord(' '):  # Space key to pause/resume
            playing = not playing
            status = "paused" if not playing else "playing"
            stdscr.addstr(0, 0, f"Behavior is {status}. Press 'space' to toggle.")
            stdscr.refresh()
            continue
        elif key == ord('q'):  # 'q' to quit
            break

        # Optional: Add a small delay to avoid overloading the CPU with constant screen refresh
        time.sleep(0.1)


'''
def behavior_playback_control():
      
    # List of behaviors to cycle through
    behaviors = [
        pointLeftSequential,
        pointRightSequential,
        # Add more behavior functions here
    ]
    
    current_behavior_index = 0]kl

    print("\nBehavior Playback Control:")
    print(" - Press right arrow to play next behavior")
    print(" - Press left arrow to play previous behavior")
    print(" - Press 'space' to pause/resume current behavior")
    print(" - Press 'q' to quit playback")

    while True:
        # Listen for key presses
        if keyboard.is_pressed('right'):
            # Play next behavior
            print(f"Playing behavior: {behaviors[current_behavior_index].__name__}")
            behaviors[current_behavior_index](500, 127, 50, 50)  # Adjust parameters as needed
            current_behavior_index = (current_behavior_index + 1) % len(behaviors)
            time.sleep(0.5)
        
        elif keyboard.is_pressed('left'):
            # Play previous behavior
            current_behavior_index = (current_behavior_index - 1) % len(behaviors)
            print(f"Playing behavior: {behaviors[current_behavior_index].__name__}")
            behaviors[current_behavior_index](500, 127, 50, 50)  # Adjust parameters as needed
            time.sleep(0.5)

        elif keyboard.is_pressed('space'):
            # Pause/resume current behavior
            print("Toggling pause/resume")
            # Add pause logic here if needed
        elif keyboard.is_pressed('q'):
            print("Exiting behavior playback")
            break
        time.sleep(0.1)  # Add a short delay to prevent high CPU usage
            '''

# Function for manual control
def manual_control():
    
    # Default behavior parameters
    current_duration = 750
    current_speed = 192
    current_fade_in = 50
    current_fade_out = 50

    # CLI menu
        
    print("\nReady to receive behavior commands.")
    print("Send: behavior_id[,duration,speed,fade_in,fade_out]")
    print(" - duration: 100–750 ms")
    print(" - speed   : 0–255")
    print(" - fade_in : 20–200 ms")
    print(" - fade_out: 20–200 ms")
    print("You can also send just the behavior ID to repeat it with the last used parameters.\n")

    while True:
        print("--- Gait Control Menu ---")
        print("0  → Retract All Completely")
        print("1  → Sequential Wave")
        print("2  → Sequential Wave Front to Back Symmetrical Sides")
        print("3  → Sequential Wave Front to Back Symmetrical Sides with 25 cycles")
        print("4  → Point Left Sequential")
        print("5  → Point Right Sequential")
        print("6  → Retract Right Sequential")
        print("7  → Retract Left Sequential")
        print("8  → Extend All Completely")
        print("9  → prep for Point Left Right Left")
        print("10  → Point Left Right Left")
        
        user_input = input(">>> ").strip()
        if user_input.lower() == "q":
            break

        parts = user_input.split(' ')
        if len(parts) == 1:
            behavior_id = parts[0]
            execute_behavior_by_id(behavior_id, current_duration, current_speed, current_fade_in, current_fade_out)

        elif len(parts) == 5:
            behavior_id = parts[0]
            
            # Update global parameters
            current_duration = int(parts[1])
            current_speed = int(parts[2])
            current_fade_in = int(parts[3])
            current_fade_out = int(parts[4])
            
            execute_behavior_by_id(behavior_id, current_duration, current_speed, current_fade_in, current_fade_out)

        else:
            print("Invalid input format. Use: ID[,duration,speed,fade_in,fade_out]")

# Main logic
def main():
    print("Welcome to Susan's world! Choose an option:")
    print("1 - Manual control (Choose behaviors by entering their ids)")
    print("2 - Player control (Press arrows to cycle behaviors)")

    user_choice = input("Please choose '1' or '2': ")
    
    try:
        if user_choice == '1':
            manual_control()
        elif user_choice == '2':
            #behavior_playback_control()
            # Start behavior playback control with curses
            curses.wrapper(behavior_playback_control)
        else:
            print("Invalid choice. Exiting.")
            return
    
    except Exception as e:
        print(f"Error: {e}")

    finally:
        serial45.close()
        serial61.close()
        serial23.close()
        print("Serial ports closed.")


if __name__ == "__main__":
    main()
