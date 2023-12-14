import serial
import time

ser = serial.Serial('COM3', 9600, timeout=0.050)

while True:
    while ser.in_waiting > 0:
        print(ser.readline())
        time.sleep(0.0)
