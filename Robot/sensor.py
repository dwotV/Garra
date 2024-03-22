import time
import serial

class sens:
    ard=0

    def __init__(self):
        pass

    def conectar(self,puerto:str):
        try:
            self.ard=serial.Serial(puerto,9600)
            time.sleep(4)
            self.ard.readline()
            self.ard.readline()
            return True
        except:
            return False

    # Lectura de TODOS sensores en un solo instante regresando una lista con las entradas recuperadas.
    # ind=0  ->  Lista de código RGB (R,G,B)
    # ind=1  ->  Bool sobre exitencia de un sonido
    # ind=2  ->  int que indica el tipo de touch registrado donde:
    #            0 = Cualquier toque
    #            1 = Toque corto
    #            2 = Toque largo}
    # ind=3  ->  float que indica la distancia del objeto registrada por el sensor  
    # ind=4  ->  Lista[str] que indica si se detecta presencia en el sensor N | 0<N<4
    def leerSens(self)  ->list[list[int], bool, int, float, list[str]] :
        rawd=""
        while(rawd==""):
            self.ard.write(b'1')
            rawd=self.ard.readline() # Reading Raw data 
            rawd=str(rawd,"utf-8")
        rawd=rawd[:-2]
        rawd=rawd.split('@')
        rawd[0]=rawd[0].split(",")
        for i in range(3):
            rawd[0][i]=int(rawd[0][i])
        rawd[1]=bool(int(rawd[1]))
        rawd[2]=int(rawd[2])
        rawd[3]=float(rawd[3])
        rawd[4]=rawd[4].split(",")
        return rawd
    
    def desColor(self)  ->bool :
        try:
            self.ard.write(b'11')
            self.ard.readline()
            return True
        except:
            return False

    '''
    def desTouch(self)  ->bool :
        try:
            self.ard.write(b'3')
        except:
            return False
    '''
    
    def desDistance(self)  ->bool :
        try:
            self.ard.write(b'14')
            self.ard.readline()
            return True
        except:
            return False

    def desPresence(self)  ->bool :
        try:
            self.ard.write(b'15')
            self.ard.readline()
            return True
        except:
            return False

    def getColor(self, op:int=0) ->str | list:
        dt=self.leerSens() # Split into RGB List
        dt=dt[0] #RGB
       # self.desColor()
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
    
    def isColor(self, col:str|list) ->bool :
        if(type(col)==str):
            return self.getColor()==col
        else:
            dt=self.getColor(1)
            return dt==col

    def getSound(self)  ->bool :
        dt=self.leerSens() # Split into RGB List
        dt=dt[1] #Sound 
        return dt

    def getTouch(self)  ->int :
        dt=self.leerSens() # Leer existencia de cualquier tipo de touch
        dt=dt[2] #Touch
        return dt
        
    def isTouch(self)  ->bool :
        dt=self.getTouch()
        if(dt!=0):
            return True
        else:
            return False

    def isShortTouch(self)  ->bool :
        dt=self.getTouch()
        if(dt==1):
            return True
        else:
            return False

    def isLongTouch(self)  ->bool :
        dt=self.getTouch()
        if(dt==2):
            return True
        else:
            return False

    def getDistance(self)  ->float :
        dt=self.leerSens() # Lectura de Sensores
        dt=dt[3] #Distance
        return dt
    
    def isDistance(self, infLimit:int|float, supLimit:int|float=-1):
        if(supLimit==-1):
            supLimit=infLimit
        dt= self.getDistance()
        if(dt >= infLimit and dt <= supLimit):
            return True
        else:
            return False

    def getPresence(self,sensorid:int=0)  ->list[int] :
        if(sensorid==0):
            dt=self.leerSens() # Lectura de Sensores
            dt=dt[4] #Presence
            return dt
        else:
            if(sensorid<1 or sensorid>3):
                return False
            else:
                dt=self.getPresence() # Lectura de Sensores
                return dt[sensorid-1]        
    
    def isPresence(self, sensorid:int |list[str])  ->bool :
        if(type(sensorid)!=list):
            if(sensorid<1 or sensorid>3):
                return False
            else:
                dt=self.getPresence()
                return dt[sensorid-1]=='1'
        # La lista es unna lista de strings para que reciba tres datos cualquiera, si no son 0 o 1, se considera que el valor de presencia puede ser cualquiera,
        # si el dato es 0 o 1, se necesita que el dato del sensor presencia sea exactamente igual para regresar verdadero
        # Ejemplo: ['x','x','x'], sin importar que da True
        # Ejemplo: ['1','0','x'] requiere que presencia en 0 sea '1', en 1 sea '0' y en 3 puede ser cualquiera
        else:
            if(len(sensorid)!=3):
                return False
            else:
                dt=self.getPresence()
                for i in range(3):
                    if(sensorid[i]=='1' and dt[i]!='1'):
                        return False
                    elif(sensorid[i]=='0' and dt[i]!='0'):
                        return False
                return True

        

    #Método until incompleto (no dejar avanzar hasta que se cumpla una condición)
    def until(self, sen: str , cond:any="")  ->bool :
        while True:
            #Until color
            if(sen=="color"): #cond debe ser 'red', 'green', 'blue' o una lista de código RGB y utiliza como criterio isColor()
               if((type(cond)==list and len(cond)==3) or (cond=='red' or cond=='green' or cond=='blue')):
                   if(self.isColor(cond)):
                       return True
               else:
                   return False
            #Until sonido
            elif(sen=="sound"): #cond no es utilizado ya que regresa si hubo o no sonido, acorde al método getSound()
                if(self.getSound()):
                    return True
            #Until toque
            elif(sen=="touch"):
                if(cond==0 and self.isTouch()): #cond==0 significa que revisa cualquier toque con isTouch()
                    return True
                elif(cond==1 and self.isShortTouch()): #cond==1 significa que revisa un toque corto con isShortTouch()
                    return True
                elif(self.isLongTouch()): #otro cond significa que revisa un toque largo con isLongTouch()
                    return True
            #Until distancia
            elif(sen=="distance"):
                if(type(cond)!=list): #si cond no es una lista, llama isDistance() con un sólo parámetro
                    if(self.isDistance(cond)):
                        return True
                elif(len(cond)==2): #si cond es una lista de dos posiciones, llama isDistance() con dos parámetros
                    if(self.isDistance(cond[0],cond[1])):
                        return True
            #Until presencia
            elif(sen=="presence" and (type(cond)==int or type(cond)==list)): #cond debe ser entero o lista para poder ser enviado a isPresence()
                if(self.isPresence(cond)):
                    return True
            #Default
            else:
                return False #si no se cumple nada, devuelve False
                    
                
                    
