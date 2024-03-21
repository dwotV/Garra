import xarm # importamos xarm para utilizar las funciones básicas de posición de los motores de la garra

#clase Garra que contiene todos los atributos y métodos correspondientes a una garra
class Garra:

    #Constructor de la clase Garra, sus atributos son "pos" y "rob". Para poder trabajar en coordenadas polares "pos" es el arreglo las posiciones de "r" en el tablero circular y "rob" es el robot que vamos a controlar
    def __init__(self):
        self.pos=[
        [[2, 515], [3, 130], [4, 430], [5, 350]], #Anillo 1
        [[2, 515], [3, 45], [4, 215], [5,225]], #Anillo 2
        [[2, 515], [3, 55], [4, 125], [5, 175]], #Anillo 3
        [[2, 515], [3, 140], [4,  125], [5, 155]], #Anillo 4
        [[2, 515], [3, 215], [4, 125], [5, 0]] #Anillo 5
        ]   #Array de las posiciones de todos los motores para las 5 posiciones en r (anillos) pertenecientes al radio del tablero circular
        self.rob=0 #definimos el robot como cero hasta que se use el método "conecta()"
    
    #Método para conectarse con la garra
    def conecta(self):
        self.rob=xarm.Controller("USB") #Se conecta a la garra por el puerto USB y crea un objeto Controller para controlar a la Garra
        self.rob.setPosition([[1, 355],[2, 905],[3, 265],[4, 340],[5, 535],[6, 500]],duration=2000,wait=True) #Se mueve a la posición de inicio y hace un movimiento para indicar que se conectó
    
    #Método para cerrar la garra
    def agarra(self):
        self.rob.setPosition(1,550,2000,True) #Se cambia la posición del Motor que controla la garra (Serv 1) para abrirla
    
    #Método para abrir la garra
    def suelta(self):
        self.rob.setPosition(1,0,2000,True) #Se cambia la posición del Motor que controla la garra (Serv 1) para  cerrarla
    
    #Método para ir a una posición del círculo predefinida. Tiene 2 parámetros: "hora" y "anillo". Para trabajar con coordenadas polares "hora" es el ángulo (theta) en el tablero circular y el anillo es la distancia del origen del tablero circular (r)
    def mover(self, hora:int, anillo:int):
        if(anillo<1 or anillo>5): #Valida que el parámetro de anillo tome una de las 5 posiciones posibles
            print("ERROR, El anillo al que se moverá el gancho debe ser un número entero entre 1 y 5")
        elif(hora<1 or hora>12): #Valida que el parámetro de hora tome una de las 12 posiciones posibles
            print("ERROR, la hora a la que se moverá el gancho debe ser un número entero entre 1 y 12")
            
        else:
            hora=int((1000/12)*hora) #Hace la transformación de nuestras posiciones del ángulo del círculo (theta) a las unidades de la librería "xarm" y lo transforma a entero
            self.rob.setPosition(6,hora,2000,True)  #Se cambia la posición del Motor que controla la rotación (Serv 6) a la hora dada en los parámetros
            self.rob.setPosition(self.pos[anillo-1],duration=2000,wait=True)  #Se cambia la posición de todos los motores por medio del elemento en la posición "anillo" del arreglo de posiciones en "r" (pos)

    #Método para hacer una serie de movimientos que aparentan un saludo
    def saludar(self):
        self.rob.setPosition([[1, 420], [2, 120], [3, 500], [4, 145], [5, 400], [6, 120]],duration=1000,wait=True)
        self.rob.setPosition([[1, 595], [2, 120], [3, 500], [4, 300], [5, 400], [6, 120]],duration=700,wait=True)
        self.rob.setPosition([[1, 495], [2, 120], [3, 500], [4, 0], [5, 400], [6, 120]],duration=700,wait=True)
        self.rob.setPosition([[1, 250], [2, 120], [3, 500], [4, 300], [5, 400], [6, 120]],duration=700,wait=True)
        self.rob.setPosition([[1, 595], [2, 120], [3, 500], [4, 0], [5, 400], [6, 120]],duration=700,wait=True)
        self.rob.setPosition([[1, 395], [2, 120], [3, 500], [4, 145], [5, 400], [6, 120]],duration=1000,wait=True)
    
    #Método para ir a la posición predeterminada, para así facilitar movimiento de objetos y de la garra sin colisionar con un objeto. La garra se mamntendrá en su estado actual (abierto/cerrado)
    def resetPosition(self):
        self.rob.setPosition([[3, 265],[4, 340],[5, 535],[6, 500]],duration=2000,wait=True)
    
    def rps(self):
        self.rob.setPosition([[3, 265],[4, 340],[5, 535],[6, 500]],duration=2000,wait=True)