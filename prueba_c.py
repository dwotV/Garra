import time
import serial


ard=serial.Serial("COM3",9600)
time.sleep(1)
while True:
    # while(ard.in_waiting==0):
    #     pass
    dp=str(dp,"utf-8")
    print(dp)
