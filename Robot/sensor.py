import time
import serial

class sens:
    ard=0

    def __init__():
        pass

    def conectar(self,puerto:str):
        try:
            self.ard=serial.Serial(puerto,9600)
        except:
            return False
    
    def leer(self):
        time.sleep(1)
        while True:
            while(self.ard.in_waiting==0):
                pass
            dp=self.ard.readline()
            print(dp)
    
    def desColor(self):
        try:
            self.ard.write(b'1')
            return True
        except:
            return False

    def desTouch(self):
        try:
            self.ard.write(b'3')
        except:
            return False

    def desDistance(self):
        try:
            self.ard.write(b'4')
        except:
            return False

    def desPresence(self):
        try:
            self.ard.write(b'5')
        except:
            return False

    def getColor(self, op:int=0) ->bool | list:
        rawd=self.ard.readline() # Reading Raw data 
        rawd=str(rawd,"utf-8")
        rawd=rawd.split('@') 
        dt=rawd[0].split(',') # Split into RGB List
        dt[0]=int(dt[0]) #R
        dt[1]=int(dt[1]) #G
        dt[2]=int(dt[2]) #B
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
            return dt # Return RGB List 
    
    def isColor(self, col:str) ->bool :
        return self.getColor()==col

    def isColor(self,col:list)  ->bool :
        dt=self.getColor(1)
        return dt==col

    def getSound(self)  ->bool :
        rawd=self.ard.readline() # Reading Raw data 
        rawd=str(rawd,"utf-8")
        rawd=rawd.split('@') 
        dt=rawd[1] # Sonido registrado
        if(dt=='1'):
            return True
        else:
            return False
        
    def isSound(self) ->bool :
        return self.getSound()

    def getTouch(self)  ->bool :
        rawd=self.ard.readline() # Reading Raw data 
        rawd=str(rawd,"utf-8")
        rawd=rawd.split('@') 
        dt=rawd[2]
        if(dt==1 or dt==2):
            return True
        else:
            return False
        
    def isTouch(self)  ->bool :
        return self.getTouch()

    def getShortTouch(self)  ->bool :
        rawd=self.ard.readline() # Reading Raw data 
        rawd=str(rawd,"utf-8")
        rawd=rawd.split('@') 
        dt=rawd[2]
        if(dt=='1'): 
            return True
        else:
            return False
        
    def isShortTouch(self)  ->bool :
        return self.getShortTouch()

    def getLongTouch(self)  ->bool :
        rawd=self.ard.readline() # Reading Raw data 
        rawd=str(rawd,"utf-8")
        rawd=rawd.split('@') 
        dt=rawd[2]
        if(dt=='2'):
            return True
        else:
            return False
        
    def isLongTouch(self)  ->bool :
        return self.getLongTouch()

    def getDistance(self)  ->float :
        rawd=self.ard.readline() # Reading Raw data 
        rawd=str(rawd,"utf-8")
        rawd=rawd.split('@') 
        dt=float(rawd[3])
        return dt
    
    def isDistance(self, infLimit:int|float, supLimit:int|float)  ->bool :
        if(self.getDistance() >= infLimit and self.getDistance() <= supLimit):
            return True
        else:
            return False

    def getPresence(self)  ->list[int] :
        rawd=self.ard.readline() # Reading Raw data 
        rawd=str(rawd,"utf-8")
        rawd=rawd.split('@') 
        dt=rawd[4]
        dt=dt.split(",")
        dt[1]= int(dt[1]) # Sensor 1
        dt[2]= int(dt[2]) # Sensor 2
        dt[3]= int(dt[3]) # Sensor 3
        return dt
    
    def getPresence(self, sensorid:int)  ->int | bool :
        if(sensorid<1 or sensorid>3):
            return False
        else:
            rawd=self.ard.readline() # Reading Raw data 
            rawd=str(rawd,"utf-8")
            rawd=rawd.split('@') 
            dt=rawd[4]
            dt=dt.split(",")
            dt = int(dt[sensorid])
            return dt
    
    def isPresence(self, sensorid:int)  ->bool :
        if(sensorid<1 or sensorid>3):
            return False
        else:
            if(self.getPresence(sensorid)!=0):
                return True
            else:
                return False

    #Método until incompleto (no dejar avanzar hasta que se cumpla una condición)
    def until(self, sen:str, cond:any)  ->bool :
        while True:
            if(sen=="color" and self.isColor(cond)):
               return True
            elif(sen=="sonido" and self.getSound()=='1'):
                return True
            elif(sen=="toque"):
                if(cond=='0' and self.getTouch()):
                    return True
                elif(cond=='1' and self.getShortTouch()):
                    return True
                elif(self.getLongTouch()):
                    return True
