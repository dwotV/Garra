import time
import serial

class sens:
    ard=0

    def __init__():
        pass

    def conectar(self,puerto):
        self.ard=serial.Serial(puerto,9600)
    
    def leer(self):
        time.sleep(1)
        while True:
            while(self.ard.in_waiting==0):
                pass
            dp=self.ard.readline()
            print(dp)
    
    def desColor(self):
        self.ard.write(1)

    def desTouch(self):
        self.ard.write(2)
    
    def desDistance(self):
        self.ard.write(3)

