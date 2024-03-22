import time
import serial

class sens:
    ard=0

    # Constructor de clase sens
    def __init__():
        pass

    # Método para conectar la placa Arduino al Puerto indicado, en caso de una conexión fallida devuelve False
    def conectar(self,puerto:str):
        try:
            self.ard=serial.Serial(puerto,9600)
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
        time.sleep(1)
        rawd=self.ard.readline() # Reading Raw data 
        rawd=str(rawd,"utf-8")
        rawd=rawd.split('@')
        rawd[0]=rawd[0].split(",")
        for i in range(3):
            rawd[0][i]=int(rawd[0][i])
        rawd[1]=bool(int(rawd[1]))
        rawd[2]=int(rawd[2])
        rawd[3]=float(rawd[3])
        rawd[4]=rawd[4].split(",")
        return rawd

    #Método para mostrar la información del sensor de Color en el display integrado al modulo de sensores xarm. 
    def desColor(self)  ->bool :
        try:
            self.ard.write(b'1')
            return True
        except:
            return False

    '''
    #Método para mostrar la información del sensor Touch en el display integrado al modulo de sensores xarm. 
    def desTouch(self)  ->bool :
        try:
            self.ard.write(b'3')
        except:
            return False
    '''

    #Método para mostrar la información del sensor de Distancia en el display integrado al modulo de sensores xarm. 
    def desDistance(self)  ->bool :
        try:
            self.ard.write(b'4')
            return True
        except:
            return False

    #Método para mostrar la información de los sensores de Presencia en el display integrado al modulo de sensores xarm. 
    def desPresence(self)  ->bool :
        try:
            self.ard.write(b'5')
            return True
        except:
            return False

    
    # Método para devolver la lectura del sensor de detección de Color
    # Se devuelve un color predefinido donde color = {'red', 'green', 'blue'}
    # o se devuelve una lista con el código de color RGB en la forma [R,G,B]
    
    def getColor(self, op:int=0) ->str | list:
        dt=self.leerSens() # Split into RGB List
        dt=dt[0] #RGB
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

    # Método para devolver el resultado de la comparación entre una condición deseada predefinida donde col ∈ {'red', 'green', 'blue'}
    # para el sensor de Color del sensor y la lectura actual del sensor.
    
    def isColor(self, col:str) ->bool :
        return self.getColor()==col

    
    # Método para devolver el resultado de la comparación entre una condición deseada donde col es una lista con un código RGB
    # para el sensor de Color del sensor y la lectura actual del sensor.
    
    def isColor(self,col:list)  ->bool :
        dt=self.getColor(1)
        return dt==col

    
    # Método para devolver la lectura del sensor de detección de Sonido
    # Se devuelve un bool donde se indica la existencia de algún sonido
    
    def getSound(self)  ->bool :
        dt=self.leerSens() # Split into RGB List
        dt=dt[1] #Sound 
        return dt

    
    # Método para devolver la lectura del sensor de detección de Touch
    # Se devuelve un bool donde se indica la existencia de algún tipo de Touch donde:
    #     0 -> Cualquier touch
    #     1 -> Touch corto
    #     2 -> Touch largo

    def getTouch(self)  ->int :
        dt=self.leerSens() # Leer existencia de cualquier tipo de touch
        dt=dt[2] #Touch
        return dt


    # Método para devolver la lectura del sensor de detección de Touch tipo 0
    # Se devuelve un bool donde se indica la existencia de algún sonido cualquiera
        
    def isTouch(self)  ->bool :
        dt=self.getTouch()
        if(dt!=0):
            return True
        else:
            return False


    # Método para devolver la lectura del sensor de detección de Touch tipo 1
    # Se devuelve un bool donde se indica la existencia de algún sonido corto

    def isShortTouch(self)  ->bool :
        dt=self.getTouch()
        if(dt==1):
            return True
        else:
            return False


    # Método para devolver la lectura del sensor de detección de Touch tipo 1
    # Se devuelve un bool donde se indica la existencia de algún sonido largo

    def isLongTouch(self)  ->bool :
        dt=self.getTouch()
        if(dt==2):
            return True
        else:
            return False


    # Método para devolver la lectura del sensor de detección de Distancia
    # Se devuelve un float donde se indica la distancia detectada con respecto al objeto físico colocado en el campo de detección del sensor
    
    def getDistance(self)  ->float :
        dt=self.leerSens() # Lectura de Sensores
        dt=dt[3] #Distance
        return dt


    # Método para devolver la lectura del sensor de Distancia 
    # Se devuelve un bool donde se indica si el objeto detectado se encuentra dentro de un rango establecido mediante [limiteInferior, limiteSuperior]
    # o unicamente un valor particular para comparar.
    
    def isDistance(self, infLimit:int|float, supLimit:int|float=-1)  ->bool :
        if(supLimit==-1):
            supLimit=infLimit
        dt= self.getDistance()
        if(dt >= infLimit and dt <= supLimit):
            return True
        else:
            return False


    # Método para devolver la lectura de los tres sensores de presencia
    # Se devuelve una lista[str] donde se indica el estado de presencia de cada sensor, donde:
    # ['0','0','0'] representa presencia nula en los tres sensores
    # La distribución de sensores es la siguiente:
    #      indice 0 -> Sensor Izquierda 
    #      indice 1 -> Sensor Centro 
    #      indice 2 -> Sensor Derecha (Sensor más cercano a la tarjeta Arduino del Módulo físico)     
    
    def getPresence(self)  ->list[str] :
        dt=self.leerSens() # Lectura de Sensores
        dt=dt[4] #Presence
        return dt


    # Método para devolver la lectura de un sensor de Presencia 
    # Se devuelve un str donde se indica la presencia de un objeto en el sensor con el id indicado en "sensorid", donde:
    #      '0' -> Sin presencia de objeto
    #      '1' -> Presencia de objeto

    def getPresence(self, sensorid:int)  -> str | bool :
        if(sensorid<1 or sensorid>3):
            return False
        else:
            dt=self.getPresence() # Lectura de Sensores
            return dt[sensorid-1]


    # Método para devolver la lectura de un sensor de Presencia 
    # Se devuelve un bool donde se indica la presencia de un objeto en el sensor con el id indicado en "sensorid"

    def isPresence(self, sensorid:int)  ->bool :
        if(sensorid<1 or sensorid>3):
            return False
        else:
            dt=self.getPresence()
            return dt[sensorid-1]=='1'

    # La lista es unna lista de strings para que reciba tres datos cualquiera, si no son 0 o 1, se considera que el valor de presencia puede ser cualquiera,
    # si el dato es 0 o 1, se necesita que el dato del sensor presencia sea exactamente igual para regresar verdadero
    # Ejemplo: ['x','x','x'], sin importar que da True
    # Ejemplo: ['1','0','x'] requiere que presencia en 0 sea '1', en 1 sea '0' y en 3 puede ser cualquiera
    def isPresence(self, lst:list[str])  ->bool :
        if(len(lst)!=3):
            return False
        else:
            dt=self.getPresence()
            for i in range(3):
                if(lst[i]=='1' and dt[i]!='1'):
                    return False
                elif(lst[i]=='0' and dt[i]!='0'):
                    return False
            return True

    #Método until incompleto (no dejar avanzar hasta que se cumpla una condición)
    def until(self, sen: {'color', "sound", "touch", "distance", "presence"} , cond:any="")  ->bool :
        while True:
            #Until color
            if(sen=="color"): #cond debe ser 'red', 'green', 'blue' o una lista de código RGB y utiliza como criterio isColor()
               if((type(cond)==list and len(cond)==3) or (cond=='red' or cond=='green' or cond=='blue')):
                   if(self.isColor(cond)):
                       return True
               else:
                   return False
            #Until sonido
            elif(sen=="sound" and self.getSound()): #cond no es utilizado ya que regresa si hubo o no sonido, acorde al método getSound()
                return True
            #Until toque
            elif(sen=="touch"):
                if(cond==0 and self.isTouch()): #cond==0 significa que revisa cualquier toque con isTouch()
                    return True
                elif(cond==1 and self.isShortTouch()): #cond==1 significa que revisa un toque corto con isShortTouch()
                    return True
                elif(self.isLongTouch()): #otro cond significa que revisa un toque largo con isLongTouch
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
