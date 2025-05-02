import serial
import time

# Serial connections to each Arduino
serial45 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_24333313930351C05231-if00', 115200, timeout=1)
serial61 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313837351300250-if00', 115200, timeout=1)
serial23 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313637351115182-if00', 115200, timeout=1)

time.sleep(2)  # Give Arduinos time to reset

# Default behavior parameters
current_duration = 500
current_speed = 127
current_fade_in = 50
current_fade_out = 50

# Global parameters for behavior execution
current_params = {
    "duration": 500,
    "speed": 255,
    "fade_in": 100,
    "fade_out": 100
}

def send_command(serial_x, command, duration, speed, fade_in=50, fade_out=50):
    full_command = f"{command},{duration},{speed},{fade_in},{fade_out}"
    print(f"Sending: {full_command}")
    serial_x.write((full_command + '\n').encode('utf-8'))

def seqWaveGait(duration, speed, delay_between_legs, fade_in, fade_out):
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

def frontBackSymmetricWaveGait(duration, speed, delay_between_steps, fade_in, fade_out):
    forward_wave = [
        [(serial61, 'e2'), (serial61, 'e1')],
        [(serial23, 'e1'), (serial45, 'e2')],
        [(serial23, 'e2'), (serial45, 'e1')]
    ]
    forward_retract = [
        [(serial61, 'r2'), (serial61, 'r1')],
        [(serial23, 'r1'), (serial45, 'r2')],
        [(serial23, 'r2'), (serial45, 'r1')]
    ]
    backward_wave = list(reversed(forward_wave))
    backward_retract = list(reversed(forward_retract))
    for pair in forward_wave:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(delay_between_steps / 1000.0)
    for pair in forward_retract:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(delay_between_steps / 1000.0)
    for pair in backward_wave:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(delay_between_steps / 1000.0)
    for pair in backward_retract:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(delay_between_steps / 1000.0)

def extendall(speed, duration, fade_in, fade_out):
    for serial_x, cmd in [(serial45, 'e1'), (serial45, 'e2'), (serial61, 'e1'), (serial61, 'e2'), (serial23, 'e1'), (serial23, 'e2')]:
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)

def retrieveall(speed, duration, fade_in, fade_out):
    for serial_x, cmd in [(serial45, 'r1'), (serial45, 'r2'), (serial61, 'r1'), (serial61, 'r2'), (serial23, 'r1'), (serial23, 'r2')]:
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)

def diagonals(speed, duration, fade_in, fade_out):
    send_command(serial61, 'e1', duration, speed, fade_in, fade_out)
    send_command(serial23, 'e2', duration, speed, fade_in, fade_out)
    time.sleep(duration / 1000.0)
    send_command(serial61, 'r1', duration, speed, fade_in, fade_out)
    send_command(serial23, 'r2', duration, speed, fade_in, fade_out)
    time.sleep(duration / 1000.0)
    send_command(serial61, 'e2', duration, speed, fade_in, fade_out)
    send_command(serial45, 'e1', duration, speed, fade_in, fade_out)
    time.sleep(duration / 1000.0)
    send_command(serial61, 'r2', duration, speed, fade_in, fade_out)
    send_command(serial45, 'r1', duration, speed, fade_in, fade_out)

def pointLeft(speed, duration, fade_in, fade_out):
    send_command(serial61, 'e2', duration, speed, fade_in, fade_out)
    send_command(serial23, 'e1', duration, speed, fade_in, fade_out)
    send_command(serial23, 'e2', duration, speed, fade_in, fade_out)
    send_command(serial45, 'r1', duration, speed, fade_in, fade_out)
    send_command(serial45, 'r2', duration, speed, fade_in, fade_out)
    send_command(serial61, 'r1', duration, speed, fade_in, fade_out)

def pointRight(speed, duration, fade_in, fade_out):
    send_command(serial45, 'e1', duration, speed, fade_in, fade_out)
    send_command(serial45, 'e2', duration, speed, fade_in, fade_out)
    send_command(serial61, 'e1', duration, speed, fade_in, fade_out)
    send_command(serial61, 'r2', duration, speed, fade_in, fade_out)
    send_command(serial23, 'r1', duration, speed, fade_in, fade_out)
    send_command(serial23, 'r2', duration, speed, fade_in, fade_out)

def shake(speed, duration, fade_in, fade_out):
    for i in range(5):
        for serial_x, cmd in [(serial45, 'e1'), (serial45, 'e2'), (serial61, 'e1'), (serial61, 'e2'), (serial23, 'e1'), (serial23, 'e2')]:
            send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(duration / 1000.0)
        for serial_x, cmd in [(serial45, 'r1'), (serial45, 'r2'), (serial61, 'r1'), (serial61, 'r2'), (serial23, 'r1'), (serial23, 'r2')]:
            send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(duration / 1000.0)

def restingBreath(speed, duration, fade_in, fade_out, cycles=10):
    for i in range(cycles):
        for serial_x, cmd in [(serial45, 'e1'), (serial45, 'e2'), (serial61, 'e1'), (serial61, 'e2'), (serial23, 'e1'), (serial23, 'e2')]:
            send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(duration / 1000.0)
        for serial_x, cmd in [(serial45, 'r1'), (serial45, 'r2'), (serial61, 'r1'), (serial61, 'r2'), (serial23, 'r1'), (serial23, 'r2')]:
            send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(duration / 1000.0)

def execute_behavior_by_id(behavior_id, duration, speed, fade_in, fade_out):
    if behavior_id == "1":
        seqWaveGait(duration, speed, 150, fade_in, fade_out)
    elif behavior_id == "2":
        frontBackSymmetricWaveGait(duration, speed, 150, fade_in, fade_out)
    elif behavior_id == "3":
        extendall(speed, duration, fade_in, fade_out)
    elif behavior_id == "4":
        retrieveall(speed, duration, fade_in, fade_out)
    elif behavior_id == "5":
        diagonals(speed, duration, fade_in, fade_out)
    elif behavior_id == "6":
        pointLeft(speed, duration, fade_in, fade_out)
    elif behavior_id == "7":
        pointRight(speed, duration, fade_in, fade_out)
    elif behavior_id == "8":
        shake(speed, duration, fade_in, fade_out)
    elif behavior_id == "9":
        restingBreath(speed, duration, fade_in, fade_out)
    elif behavior_id == "10":
        four_count_leg_sequence(speed, duration, fade_in, fade_out)
    elif behavior_id == "11":
        wave_456321(speed, duration, fade_in, fade_out)
    elif behavior_id == "12":
        wave_123654(speed, duration, fade_in, fade_out)
    elif behavior_id == "13":
        open_close_1_and_4_twice(speed, duration, fade_in, fade_out)
    elif behavior_id == "14":
        four_count_with_wave(speed, duration, fade_in, fade_out)
    elif behavior_id == "15":
        complexEightCount(speed, duration, fade_in, fade_out)
    else:
        print("Invalid behavior ID")

def four_count_leg_sequence(speed, duration, fade_in, fade_out, cycles=1):
    """Moves the legs in a 4-count rhythm: 3 → 4 → (2+5) → (1+6)"""
    for _ in range(cycles):
        # 1st count: Leg 3
        send_command(serial23, 'e2', duration, speed, fade_in, fade_out)
        time.sleep(duration / 1000.0)
        send_command(serial23, 'r2', duration, speed, fade_in, fade_out)
        time.sleep(duration / 1000.0)

        # 2nd count: Leg 4
        send_command(serial45, 'e1', duration, speed, fade_in, fade_out)
        time.sleep(duration / 1000.0)
        send_command(serial45, 'r1', duration, speed, fade_in, fade_out)
        time.sleep(duration / 1000.0)

        # 3rd count: Legs 2 & 5
        send_command(serial23, 'e1', duration, speed, fade_in, fade_out)
        send_command(serial45, 'e2', duration, speed, fade_in, fade_out)
        time.sleep(duration / 1000.0)
        send_command(serial23, 'r1', duration, speed, fade_in, fade_out)
        send_command(serial45, 'r2', duration, speed, fade_in, fade_out)
        time.sleep(duration / 1000.0)

        # 4th count: Legs 1 & 6
        send_command(serial61, 'e1', duration, speed, fade_in, fade_out)
        send_command(serial61, 'e2', duration, speed, fade_in, fade_out)
        time.sleep(duration / 1000.0)
        send_command(serial61, 'r1', duration, speed, fade_in, fade_out)
        send_command(serial61, 'r2', duration, speed, fade_in, fade_out)
        time.sleep(duration / 1000.0)

def wave_456321(duration, speed, fade_in, fade_out):
    sequence = [
        (serial45, 'e1'),  # 4
        (serial45, 'e2'),  # 5
        (serial61, 'e1'),  # 6
        (serial61, 'e2'),  # 3
        (serial23, 'e1'),  # 2
        (serial23, 'e2'),  # 1
    ]
    for serial_x, cmd in sequence:
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(0.15)  # Delay between steps

    # Optional: retract in same order or reversed
    for serial_x, cmd in sequence:
        r_cmd = cmd.replace('e', 'r')
        send_command(serial_x, r_cmd, duration, speed, fade_in, fade_out)
        time.sleep(0.15)

def wave_123654(duration, speed, fade_in, fade_out):
    sequence = [
        (serial23, 'e2'),  # 1
        (serial23, 'e1'),  # 2
        (serial61, 'e2'),  # 3
        (serial61, 'e1'),  # 6
        (serial45, 'e2'),  # 5
        (serial45, 'e1'),  # 4
    ]
    for serial_x, cmd in sequence:
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(0.15)  # Delay between steps

    # Optional: retract in same order
    for serial_x, cmd in sequence:
        r_cmd = cmd.replace('e', 'r')
        send_command(serial_x, r_cmd, duration, speed, fade_in, fade_out)
        time.sleep(0.15)

def open_close_1_and_4_twice(duration, speed, fade_in, fade_out):
    sequence = [
        # First open
        (serial23, 'e2'),  # 1
        (serial45, 'e1'),  # 4
        # First close
        (serial23, 'r2'),
        (serial45, 'r1'),
        # Second open
        (serial23, 'e2'),
        (serial45, 'e1'),
        # Second close
        (serial23, 'r2'),
        (serial45, 'r1'),
    ]
    for serial_x, cmd in sequence:
        send_command(
            serial_x,
            cmd,
            current_params['duration'],
            current_params['speed'],
            current_params['fade_in'],
            current_params['fade_out']
        )
        time.sleep(current_params['duration'] / 1000.0)

def four_count_with_wave(duration, speed, fade_in, fade_out):
    pair_sequence = [
        [(serial23, 'e2'), (serial61, 'e1')],  # 1 & 6
        [(serial23, 'e1'), (serial45, 'e1')],  # 3 & 4
        [(serial61, 'e2'), (serial45, 'e2')]   # 2 & 5
    ]
    wave_sequence = [
        (serial23, 'e2'),  # 1
        (serial61, 'e2'),  # 2
        (serial23, 'e1'),  # 3
        (serial45, 'e1'),  # 4
        (serial45, 'e2'),  # 5
        (serial61, 'e1')   # 6
    ]

    # Count 1–3: Pairs move together
    for pair in pair_sequence:
        for serial_x, cmd in pair:
            send_command(
                serial_x, cmd,
                current_params['duration'],
                current_params['speed'],
                current_params['fade_in'],
                current_params['fade_out']
            )
        time.sleep(current_params['duration'] / 1000.0)

    # Count 4: Traveling wave 1 → 6
    for serial_x, cmd in wave_sequence:
        send_command(
            serial_x, cmd,
            current_params['duration'],
            current_params['speed'],
            current_params['fade_in'],
            current_params['fade_out']
        )
        time.sleep(current_params['duration'] / 1000.0)

def complexEightCount(duration, speed, fade_in, fade_out):
    step_delay = duration / 1000.0

    # Count 1: Leg 4
    send_command(serial45, 'e2', duration, speed, fade_in, fade_out)
    time.sleep(step_delay)

    # Count 2: Leg 3
    send_command(serial23, 'e1', duration, speed, fade_in, fade_out)
    time.sleep(step_delay)

    # Count 3: Leg 4
    send_command(serial45, 'e2', duration, speed, fade_in, fade_out)
    time.sleep(step_delay)

    # Count 4: Leg 3
    send_command(serial23, 'e1', duration, speed, fade_in, fade_out)
    time.sleep(step_delay)

    # Count 5: Legs 2 & 5 together
    send_command(serial23, 'e2', duration, speed, fade_in, fade_out)
    send_command(serial61, 'e1', duration, speed, fade_in, fade_out)
    time.sleep(step_delay)

    # Counts 6–8: Wave 4→5→6→3→2→1
    wave_sequence = [
        (serial45, 'e2'),  # 4
        (serial23, 'e2'),  # 5
        (serial61, 'e2'),  # 6
        (serial23, 'e1'),  # 3
        (serial61, 'e1'),  # 2
        (serial45, 'e1')   # 1
    ]
    for serial_x, cmd in wave_sequence:
        send_command(serial_x, cmd, duration, speed, fade_in, fade_out)
        time.sleep(step_delay / 2)  # tighter wave flow


# CLI menu
try:
    print("\nReady to receive behavior commands.")
    print("Send: behavior_id[,duration,speed,fade_in,fade_out]")
    print(" - duration: 100–750 ms")
    print(" - speed   : 0–255")
    print(" - fade_in : 20–200 ms")
    print(" - fade_out: 20–200 ms")
    print("You can also send just the behavior ID to repeat it with the last used parameters.\n")

    while True:
        print("--- Gait Control Menu ---")
        print("1  → Sequential Traveling Wave")
        print("2  → Symmetric Front↔Back Wave")
        print("3  → Extend All")
        print("4  → Retrieve All")
        print("5  → Diagonal Pairs")
        print("6  → Point Left")
        print("7  → Point Right")
        print("8  → Shake!")
        print("9  → Resting Breath")
        print("q  → Quit")
        print("10 → 4-Count Leg Sequence: 3, 4, 2&5, 1&6")
        print("11 → Wave 4→5→6→3→2→1")
        print("12 → Wave 1→2→3→6→5→4 (Mirrored)")
        print("13 → Legs 1 and 4 Open-Close Twice")
        print("14 → 4-Count + Wave Sequence")
        print("15 → 8-Count Combo: 4-3-4-3-2&5 + Wave(4→1)")
        print("Enter behavior ID or: ID,duration,speed,fade_in,fade_out")

        user_input = input(">>> ").strip()
        if user_input.lower() == "q":
            break

        parts = user_input.split(' ')
        if len(parts) == 1:
            behavior_id = parts[0]
            execute_behavior_by_id(behavior_id, current_duration, current_speed, current_fade_in, current_fade_out)

        elif len(parts) == 5:
            behavior_id = parts[0]
            current_duration = int(parts[1])
            current_speed = int(parts[2])
            current_fade_in = int(parts[3])
            current_fade_out = int(parts[4])
            # Update global parameters
            current_params["duration"] = current_duration
            current_params["speed"] = current_speed
            current_params["fade_in"] = current_fade_in
            current_params["fade_out"] = current_fade_out
            execute_behavior_by_id(behavior_id, current_duration, current_speed, current_fade_in, current_fade_out)

        else:
            print("Invalid input format. Use: ID[,duration,speed,fade_in,fade_out]")

except Exception as e:
    print(f"Error: {e}")

finally:
    serial45.close()
    serial61.close()
    serial23.close()
    print("Serial ports closed.")
