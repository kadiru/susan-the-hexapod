import serial
import time

# Serial connections to each Arduino
serial45 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_24333313930351C05231-if00', 115200, timeout=1)
serial61 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313837351300250-if00', 115200, timeout=1)
serial23 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313637351115182-if00', 115200, timeout=1)

time.sleep(2)  # Give Arduinos time to reset

def send_command(serial_x, command, duration, speed):
    full_command = f"{command},{duration},{speed}"
    print(f"Sending: {full_command}")
    serial_x.write((full_command + '\n').encode('utf-8'))

def seqWaveGait(duration, speed, delay_between_legs):
    wave_sequence = [
        (serial61, 'e2'), (serial23, 'e1'), (serial23, 'e2'),
        (serial45, 'e1'), (serial45, 'e2'), (serial61, 'e1')
    ]
    retract_sequence = [
        (serial61, 'r2'), (serial23, 'r1'), (serial23, 'r2'),
        (serial45, 'r1'), (serial45, 'r2'), (serial61, 'r1')
    ]
    for serial_x, cmd in wave_sequence:
        send_command(serial_x, cmd, duration, speed)
        time.sleep(delay_between_legs / 1000.0)
    time.sleep((duration + 100) / 1000.0)
    for serial_x, cmd in retract_sequence:
        send_command(serial_x, cmd, duration, speed)
        time.sleep(delay_between_legs / 1000.0)
    time.sleep((duration + 100) / 1000.0)

def frontBackSymmetricWaveGait(duration, speed, delay_between_steps):
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
            send_command(serial_x, cmd, duration, speed)
        time.sleep(delay_between_steps / 1000.0)
    for pair in forward_retract:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration, speed)
        time.sleep(delay_between_steps / 1000.0)
    for pair in backward_wave:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration, speed)
        time.sleep(delay_between_steps / 1000.0)
    for pair in backward_retract:
        for serial_x, cmd in pair:
            send_command(serial_x, cmd, duration, speed)
        time.sleep(delay_between_steps / 1000.0)

def extendall(speed):
    duration = 500
    for serial_x, cmd in [(serial45, 'e1'), (serial45, 'e2'), (serial61, 'e1'), (serial61, 'e2'), (serial23, 'e1'), (serial23, 'e2')]:
        send_command(serial_x, cmd, duration, speed)

def retrieveall(speed):
    duration = 500
    for serial_x, cmd in [(serial45, 'r1'), (serial45, 'r2'), (serial61, 'r1'), (serial61, 'r2'), (serial23, 'r1'), (serial23, 'r2')]:
        send_command(serial_x, cmd, duration, speed)

def diagonals(speed):
    duration = 500
    send_command(serial61, 'e1', duration, speed)
    send_command(serial23, 'e2', duration, speed)
    time.sleep(duration / 1000.0)
    send_command(serial61, 'r1', duration, speed)
    send_command(serial23, 'r2', duration, speed)
    time.sleep(duration / 1000.0)
    send_command(serial61, 'e2', duration, speed)
    send_command(serial45, 'e1', duration, speed)
    time.sleep(duration / 1000.0)
    send_command(serial61, 'r2', duration, speed)
    send_command(serial45, 'r1', duration, speed)

def pointLeft(speed):
    duration = 750
    send_command(serial61, 'e2', duration, speed)
    send_command(serial23, 'e1', duration, speed)
    send_command(serial23, 'e2', duration, speed)
    send_command(serial45, 'r1', duration, speed)
    send_command(serial45, 'r2', duration, speed)
    send_command(serial61, 'r1', duration, speed)

def pointRight(speed):
    duration = 750
    send_command(serial45, 'e1', duration, speed)
    send_command(serial45, 'e2', duration, speed)
    send_command(serial61, 'e1', duration, speed)
    send_command(serial61, 'r2', duration, speed)
    send_command(serial23, 'r1', duration, speed)
    send_command(serial23, 'r2', duration, speed)

def shake(speed):
    duration = 150
    for i in range(5):
        for serial_x, cmd in [(serial45, 'e1'), (serial45, 'e2'), (serial61, 'e1'), (serial61, 'e2'), (serial23, 'e1'), (serial23, 'e2')]:
            send_command(serial_x, cmd, duration, speed)
        time.sleep(duration / 1000.0)
        for serial_x, cmd in [(serial45, 'r1'), (serial45, 'r2'), (serial61, 'r1'), (serial61, 'r2'), (serial23, 'r1'), (serial23, 'r2')]:
            send_command(serial_x, cmd, duration, speed)
        time.sleep(duration / 1000.0)

def restingBreath(speed, cycles=10, duration=600):
    for i in range(cycles):
        for serial_x, cmd in [(serial45, 'e1'), (serial45, 'e2'), (serial61, 'e1'), (serial61, 'e2'), (serial23, 'e1'), (serial23, 'e2')]:
            send_command(serial_x, cmd, duration, speed)
        time.sleep(duration / 1000.0)
        for serial_x, cmd in [(serial45, 'r1'), (serial45, 'r2'), (serial61, 'r1'), (serial61, 'r2'), (serial23, 'r1'), (serial23, 'r2')]:
            send_command(serial_x, cmd, duration, speed)
        time.sleep(duration / 1000.0)

def rampUpSpeed():
    for s in [63, 127, 255]:
        print(f"Running at speed {s}")
        seqWaveGait(duration=500, speed=s, delay_between_legs=150)

def rampDownSpeed():
    for s in [255, 127, 63]:
        print(f"Running at speed {s}")
        seqWaveGait(duration=500, speed=s, delay_between_legs=150)

def rampContinuousSpeed():
    for s in range(63, 256, 32):
        print(f"Running at speed {s}")
        seqWaveGait(duration=400, speed=s, delay_between_legs=100)

# Main menu loop
try:
    print("\n--- Select Speed ---")
    print("f → Full speed (255), h → Half speed (127), q → Quarter speed (63)")
    speed_choice = input("Enter speed (f/h/q): ").strip().lower()
    speed = {"f": 255, "h": 127, "q": 63}.get(speed_choice, 127)

    while True:
        print("\n--- Gait Control Menu ---")
        print("1  → Sequential Traveling Wave")
        print("2  → Symmetric Front↔Back Wave")
        print("3  → Extend All")
        print("4  → Retrieve All")
        print("5  → Diagonal Pairs")
        print("6  → Point Left")
        print("7  → Point Right")
        print("8  → Shake!")
        print("9  → Resting Breath")
        print("10 → Ramp Up Speed")
        print("11 → Ramp Down Speed")
        print("12 → Continuous Speed Ramp")
        print("q  → Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            seqWaveGait(duration=500, speed=speed, delay_between_legs=150)
        elif choice == "2":
            frontBackSymmetricWaveGait(duration=500, speed=speed, delay_between_steps=150)
        elif choice == "3":
            extendall(speed)
        elif choice == "4":
            retrieveall(speed)
        elif choice == "5":
            diagonals(speed)
        elif choice == "6":
            pointLeft(speed)
        elif choice == "7":
            pointRight(speed)
        elif choice == "8":
            shake(speed)
        elif choice == "9":
            restingBreath(speed)
        elif choice == "10":
            rampUpSpeed()
        elif choice == "11":
            rampDownSpeed()
        elif choice == "12":
            rampContinuousSpeed()
        elif choice.lower() == "q":
            break
        else:
            print("Invalid input.")

except Exception as e:
    print(f"Error: {e}")

finally:
    serial45.close()
    serial61.close()
    serial23.close()
    print("Serial ports closed.")
