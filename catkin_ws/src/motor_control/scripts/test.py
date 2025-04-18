import serial
import time

# Set up the serial connection
serial45 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_24333313930351C05231-if00', 115200, timeout=1);#arduino_1
serial61 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313837351300250-if00', 115200, timeout=1);#arduino_2
serial23 = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_85937313637351115182-if00', 115200, timeout=1);#arduino_3

def send_command(serial_x, command):
    print(f"Sending: {command}")
    serial_x.write((command + '\n').encode('utf-8'))
    time.sleep(1)  # wait a bit for actuator to move

# Give the Arduino some time to reset after opening the port
time.sleep(2)

try:
    # Test actuator 4
    send_command(serial45, 'e1,500')  # Extend actuator 4 for 500 ms
    time.sleep(1)
    send_command(serial45, 'r1,500')  # Retract actuator 5 for 500 ms

    # Test actuator 5 (assuming it exists in your Arduino code)
    send_command(serial45, 'e2,500')  # Extend actuator 4 for 500 ms
    time.sleep(1)
    send_command(serial45, 'r2,500')  # Retract actuator 5 for 500 ms	
	
    # Test actuator 6
    send_command(serial61, 'e1,500')  # Extend actuator 6 for 500 ms
    time.sleep(1)
    send_command(serial61, 'r1,500')  # Retract actuator 6 for 500 ms

    # Test actuator 1 (assuming it exists in your Arduino code)
    send_command(serial61, 'e2,500')  # Extend actuator 1 for 500 ms
    time.sleep(1)
    send_command(serial61, 'r2,500')  # Retract actuator 1 for 500 ms
    
    # Test actuator 2
    send_command(serial23, 'e1,500')  # Extend actuator 2 for 500 ms
    time.sleep(1)
    send_command(serial23, 'r1,500')  # Retract actuator 2 for 500 ms

    # Test actuator 3 (assuming it exists in your Arduino code)
    send_command(serial23, 'e2,500')  # Extend actuator 3 for 500 ms
    time.sleep(1)
    send_command(serial23, 'r2,500')  # Retract actuator 3 for 500 ms

except Exception as e:
    print(f"Error: {e}")

finally:
    serial45.close()
    print("Test complete. Serial45 closed.")
    serial61.close()
    print("Test complete. Serial45 closed.")
    serial23.close()
    print("Test complete. Serial45 closed.")
