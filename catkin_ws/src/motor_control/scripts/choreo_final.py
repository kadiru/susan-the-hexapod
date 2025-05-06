import serial
import time
import math

# Serial connections to each Arduino
serial45 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_24333313930351C05231-if00', 115200, timeout=1)
serial61 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313837351300250-if00', 115200, timeout=1)
serial23 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313637351115182-if00', 115200, timeout=1)

time.sleep(2)  # Give Arduinos time to reset

# Default behavior parameters
current_duration = 750
current_speed = 192
current_fade_in = 50
current_fade_out = 50

def send_command(serial_x, command, duration, speed, fade_in=50, fade_out=50):
    full_command = f"{command},{duration},{speed},{fade_in},{fade_out}"
    print(f"Sending: {full_command}")
    serial_x.write((full_command + '\n').encode('utf-8'))

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

def seqWaveFrontToBackSymmetricalSides_looped(cycles, cycle_duration, duration, speed, fade_in, fade_out):
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

    steps_per_cycle = 20
    total_pairs = len(wave_pairs)
    step_time = cycle_duration / steps_per_cycle / 1000.0  # seconds

    for i in range(cycles):
        print(f"\n--- Sinusoidal Cycle {i + 1} of {cycles} ---")
        for step in range(steps_per_cycle):
            phase = (2 * math.pi * step) / steps_per_cycle

            for idx, pair in enumerate(wave_pairs):
                # Phase shift across pairs (120° apart)
                phase_shift = (2 * math.pi * idx) / total_pairs
                sin_val = (math.sin(phase + phase_shift) + 1) / 2  # [0,1]
                act_time = int(duration * sin_val)

                # Use same act_time for both legs in pair
                for serial_x, cmd in pair:
                    send_command(serial_x, cmd, act_time, speed, fade_in, fade_out)

            time.sleep(step_time)

        # Optional: Retract phase (mirrored)
        for step in range(steps_per_cycle):
            phase = (2 * math.pi * step) / steps_per_cycle

            for idx, pair in enumerate(retract_pairs):
                phase_shift = (2 * math.pi * idx) / total_pairs
                sin_val = (math.sin(phase + phase_shift) + 1) / 2
                act_time = int(duration * sin_val)

                for serial_x, cmd in pair:
                    send_command(serial_x, cmd, act_time, speed, fade_in, fade_out)

            time.sleep(step_time)

def execute_behavior_by_id(behavior_id, duration, speed, fade_in, fade_out):
    if behavior_id == "1":
        seqWave(duration, speed, 150, fade_in, fade_out)
    elif behavior_id == "2":
        seqWaveFrontToBackSymmetricalSides(duration, speed, 150, fade_in, fade_out)
    elif behavior_id == "3":
        seqWaveFrontToBackSymmetricalSides_looped(10,2000,duration,speed,fade_in,fade_out)
    else:
        print("Invalid behavior ID")
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
        print("1  → Sequential Wave")
        print("2  → Sequential Wave Front to Back Symmetrical Sides")
        print("3  → Sequential Wave Front to Back Symmetrical Sides with 25 cycles")
        
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

except Exception as e:
    print(f"Error: {e}")

finally:
    serial45.close()
    serial61.close()
    serial23.close()
    print("Serial ports closed.")

