import serial
import time

# Set up the serial connection
serl61 = serial.Serial(
    '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313837351300250-if00',
    115200,
    timeout=1
)

def send_command(command):
    print(f"Sending: {command}")
    serl61.write((command + '\n').encode('utf-8'))
    time.sleep(1)  # wait a bit for actuator to move

# Give the Arduino some time to reset after opening the port
time.sleep(2)

try:
    # Test actuator 1
    send_command('e1,500')  # Extend actuator 1 for 500 ms
    time.sleep(1)
    send_command('r1,500')  # Retract actuator 1 for 500 ms

    # Test actuator 6 (assuming it exists in your Arduino code)
    send_command('e2,500')  # Extend actuator 6 for 500 ms
    time.sleep(1)
    send_command('r2,500')  # Retract actuator 6 for 500 ms

except Exception as e:
    print(f"Error: {e}")

finally:
    serl61.close()
    print("Test complete. Serial port closed.")
