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
        print("Enter behavior ID or: ID,duration,speed,fade_in,fade_out")

        user_input = input(">>> ").strip()
        if user_input.lower() == "q":
            break

        parts = user_input.split(',')
        if len(parts) == 1:
            behavior_id = parts[0]
            execute_behavior_by_id(behavior_id, current_duration, current_speed, current_fade_in, current_fade_out)

        elif len(parts) == 5:
            behavior_id = parts[0]
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
