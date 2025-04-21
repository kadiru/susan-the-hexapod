import serial
import time

# Set up the serial connection
serial45 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_24333313930351C05231-if00', 115200, timeout=1);#arduino_1
serial61 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313837351300250-if00', 115200, timeout=1);#arduino_2
serial23 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313637351115182-if00', 115200, timeout=1);#arduino_3

# Give Arduino time to reset
time.sleep(2)

# Define actuators per board
actuators = {
    'serial45': [(serial45, 'e1'), (serial45, 'r1'), (serial45, 'e2'), (serial45, 'r2')],
    'serial61': [(serial61, 'e1'), (serial61, 'r1'), (serial61, 'e2'), (serial61, 'r2')],
    'serial23': [(serial23, 'e1'), (serial23, 'r1'), (serial23, 'e2'), (serial23, 'r2')],
}

def send_command(serial_x, command, duration):
    full_command = f"{command},{duration}"
    print(f"Sending: {full_command}")
    serial_x.write((full_command + '\n').encode('utf-8'))
    #time.sleep((duration + 200) / 1000.0)  # add small buffer after actuation

def seqWaveGait(duration, delay_between_legs):

    # Define wave order: 1 → 2 → 3 → 4 → 5 → 6
    wave_sequence = [
        (serial61, 'e2'),  # leg 1
        (serial23, 'e1'),  # leg 2
        (serial23, 'e2'),  # leg 3
        (serial45, 'e1'),  # leg 4
        (serial45, 'e2'),  # leg 5
        (serial61, 'e1')   # leg 6
    ]

    retract_sequence = [
        (serial61, 'r2'),  # leg 1
        (serial23, 'r1'),  # leg 2
        (serial23, 'r2'),  # leg 3
        (serial45, 'r1'),  # leg 4
        (serial45, 'r2'),  # leg 5
        (serial61, 'r1')   # leg 6
    ]

    print("\n--- Traveling Wave Gait: Extend Phase ---")
    for serial_x, cmd in wave_sequence:
        send_command(serial_x, cmd, duration)
        time.sleep(delay_between_legs / 1000.0)

    time.sleep((duration + 100) / 1000.0)

    print("--- Traveling Wave Gait: Retract Phase ---")
    for serial_x, cmd in retract_sequence:
        send_command(serial_x, cmd, duration)
        time.sleep(delay_between_legs / 1000.0)

    time.sleep((duration + 100) / 1000.0)

def frontBackSymmetricWaveGait(duration, delay_between_steps):

    # Each tuple: [(serial, command), (serial, command)]
    forward_wave = [
        [(serial61, 'e2'), (serial61, 'e1')],  # Legs 1 & 6
        [(serial23, 'e1'), (serial45, 'e2')],  # Legs 2 & 5
        [(serial23, 'e2'), (serial45, 'e1')]   # Legs 3 & 4
    ]

    forward_retract = [
        [(serial61, 'r2'), (serial61, 'r1')],
        [(serial23, 'r1'), (serial45, 'r2')],
        [(serial23, 'r2'), (serial45, 'r1')]
    ]

    # Reverse for backward wave
    backward_wave = list(reversed(forward_wave))
    backward_retract = list(reversed(forward_retract))

    print("\n--- Symmetric Wave: Front to Back ---")
    for pair in forward_wave:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration)
        time.sleep(delay_between_steps / 1000.0)

    time.sleep((duration + 100) / 1000.0)

    for pair in forward_retract:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration)
        time.sleep(delay_between_steps / 1000.0)

    time.sleep((duration + 100) / 1000.0)

    print("--- Symmetric Wave: Back to Front ---")
    for pair in backward_wave:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration)
        time.sleep(delay_between_steps / 1000.0)

    time.sleep((duration + 100) / 1000.0)

    for pair in backward_retract:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration)
        time.sleep(delay_between_steps / 1000.0)

    time.sleep((duration + 100) / 1000.0)

def test():
    # Duration loop values in ms
    durations = [250, 500, 750]

    for duration in durations:
        print(f"\n--- Actuating with duration: {duration} ms ---")
        for board_name, command_list in actuators.items():
            for serial_x, command in command_list:
                send_command(serial_x, command, duration)
        print("--- Cycle complete ---")
        time.sleep(1)  # wait before next duration cycle

def extendall():
    duration = 500
    send_command(serial45, 'e1', duration)
    send_command(serial45, 'e2', duration)
    send_command(serial61, 'e1', duration)
    send_command(serial61, 'e2', duration)
    send_command(serial23, 'e1', duration)
    send_command(serial23, 'e2', duration)

def diagonals():
    duration = 500
    send_command(serial61, 'e1', duration)
    send_command(serial23, 'e2', duration)
    time.sleep(duration/1000.0)  # wait before next duration cycle
    send_command(serial61, 'r1', duration)
    send_command(serial23, 'r2', duration)
    time.sleep(duration/1000.0)  # wait before next duration cycle
    send_command(serial61, 'e2', duration)
    send_command(serial45, 'e1', duration)
    time.sleep(duration/1000.0)  # wait before next duration cycle
    send_command(serial61, 'r2', duration)
    send_command(serial45, 'r1', duration)

def retrieveall():
    duration = 500
    send_command(serial45, 'r1', duration)
    send_command(serial45, 'r2', duration)
    send_command(serial61, 'r1', duration)
    send_command(serial61, 'r2', duration)
    send_command(serial23, 'r1', duration)
    send_command(serial23, 'r2', duration)	

try:
    while True:
        print("\n--- Gait Control Menu ---")
        print("1 → Sequential Traveling Wave (seqWaveGait)")
        print("2 → Symmetric Front↔Back Wave (frontBackSymmetricWaveGait)")
        print("3 → Extend All")
        print("4 → Retrieve All")
        print("5 → Diagonal Pairs")
        print("q → Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            seqWaveGait()
        elif choice == "2":
            frontBackSymmetricWaveGait()
        elif choice == "3":
            extendall()
        elif choice == "4":
            retrieveall()
        elif choice == "5":
            diagonals()
        elif choice.lower() == "q":
            print("Exiting gait controller.")
            break
        else:
            print("Invalid input. Try again.")

except Exception as e:
    print(f"Error: {e}")

finally:
    serial45.close()
    print("Serial45 closed.")
    serial61.close()
    print("Serial61 closed.")
    serial23.close()
    print("Serial23 closed.")


except Exception as e:
    print(f"Error: {e}")

finally:
    serial45.close()
    print("Test complete. Serial45 closed.")
    serial61.close()
    print("Test complete. Serial45 closed.")
    serial23.close()
    print("Test complete. Serial45 closed.")
