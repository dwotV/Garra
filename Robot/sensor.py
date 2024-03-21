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
        self.ard.write(b'1')

    #def desTouch(self):
     #   self.ard.write(b'3')
    
    def desDistance(self):
        self.ard.write(b'4')

    def desPresence(self):
        self.ard.write(b'5')

    def getColor(int op=0):
        dt=self.ard.readline()
        dt=dt.dplit('@')
        dt=dt.split(',')
        dt[0]=int(dt[0])
        dt[1]=int(dt[1])
        dt[2]=int(dt[2])
        # Si op==0, regresa si es rojo, verde o azul
        if(op==0):
            if(dt[0]>dt[1] and dt[0]>dt[2]):
                return "red"
            elif(dt[1]>dt[2]):
                return "green"
            else:
                return "blue"
        #Si op!=0, regresa el código rgb
        else:
            return dt
    
    def isColor(self,col:string):
        return getColor()==col

    def isColor(self,col:list):
        dt=getColor(1)
        return dt==col

    def getSound(self):
        dt=self.ard.readline()
        dt=dt.split('@')
        dt=dt[1]
        if(dt=='1'):
            return True
        else:
            return False

    def getTouch(self):
        dt=self.ard.readline()
        dt=dt.split('@')
        dt=dt[2]
        if(dt==1 or dt==2):
            return True
        else:
            return False

    def getShortTouch(self):
        dt=self.ard.readline()
        dt=dt.split('@')
        dt=dt[2]
        if(dt=='1'):
            return True
        else:
            return False
    def getLongTouch(self):
        dt=self.ard.readline()
        dt=dt.split('@')
        dt=dt[2]
        if(dt=='2'):
            return True
        else:
            return False

    def getDistance(self):
        dt=self.ard.readline()
        dt=dt.split('@')
        dt=float(dt[3])
        return dt

    def getPresence(self):
        dt=self.ard.readline()
        dt=dt.split('@')
        dt=dt[4]
        dt=dt.split(",")
        return dt

    #Método until incompleto (no dejar avanzar hasta que se cumpla una condición)
    def until(self,sen,cond):
        while True:
            if(sen=="color" and isColor(cond)):
               return True
            elif(sen=="sonido" and getSound()=='1'):
                return True
            elif(sen=="toque"):
                if(cond=='0' and getTouch()):
                    return True
                elif(cond=='1' and getShortTouch()):
                    return True
                elif(getLongTouch()):
                    return True
