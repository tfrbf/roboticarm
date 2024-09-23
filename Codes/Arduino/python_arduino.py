import serial
import time



# Replace 'com12' with the correct COM port for your Arduino
ArduinoSerial = serial.Serial('com13', 9600)
time.sleep(2)

print(ArduinoSerial.readline())
print("Enter 1 to turn ON LED and 0 to turn OFF LED")

while True:
    var = input()  # Use input() instead of raw_input()
    print("You entered:", var)

    if var == '1':
        ArduinoSerial.write(b'1')  # Convert to bytes
        print("LED turned ON")
        time.sleep(1)

    elif var == '0':
        ArduinoSerial.write(b'0')  # Convert to bytes
        print("LED turned OFF")
        time.sleep(1)
