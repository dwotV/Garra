# Este paquete controla los movimientos del brazo robótico xArm-UNO a través de una librería ya existente: 'xarm'.
import xarm

# Este paquete se utiliza para el cálculo de la posición de los rotores cuando es necesario.
import math

import time

from Garra.sensor import sens

class Garra:

    # Constructor de la clase Garra
    
    # El atributo 'pos' inicializa los valores para cada uno de los servo-motores 
    # en el siguiente formato: [[servo, valor] , [servo2, valor2] ...].
    # Estos valores son para ubicar objetos posicionados en un conjunto de anillos que pertenecen a un tablero circular. 
    # Se utilizan coordenadas polares, donde el anillo supone el radio y un hora (valor entre 1 y 12) el ángulo.
    
    # El atributo 'rob' se utiliza para manipular al robot como un objeto de la clase Garra. 
    # Sin embargo, es inicializado como '0' hasta que se utilice el método 'conecta()'.
    
    def __init__(self):
        self.pos=[
        [[2, 515], [3, 130], [4, 430], [5, 350]],     # Anillo 1
        [[2, 515], [3, 45], [4, 215], [5,225]],       # Anillo 2
        [[2, 515], [3, 55], [4, 125], [5, 175]],      # Anillo 3
        [[2, 515], [3, 140], [4,  125], [5, 155]],    # Anillo 4
        [[2, 515], [3, 215], [4, 125], [5, 0]]        # Anillo 5
        ]
        self.rob=0
        self.sen=sens()
    
    
    # Método para establecer la conexión con el robot mediante un puerto USB
    # Al comprobar que la conexión fue exitosa, el robot se moviliza a su posición inicial 
    def conecta(self):
        try:
            self.rob=xarm.Controller("USB")
            self.rob.setPosition([[1, 355],[2, 905],[3, 265],[4, 340],[5, 535],[6, 500]],duration=2000,wait=True)
        except:
            return False
    
    def conectaSen(self,usb):
        self.sen.conectar(usb)
        
    
    # Método para cerrar la garra
    # Está diseñado para tomar un cubo de 3 cm de largo.
    # Para objetos de diferente escala, se debe modificar el valor '550'
    def agarra(self):
        self.rob.setPosition(1,550,2000,True)
    
    # Método para abrir la garra
    # Colocar 0 en el segundo campo para abrir por completo la garra 
    def suelta(self):
        self.rob.setPosition(1,0,2000,True)
    
    # Método para movilizar la garra dados la hora y el anillo
    # Hora es el parámetro de rotación dado al servo 6
    # Para ubicarse en el anillo correspondiente, llamar al array con la posición de cada servo
    def mover(self, hora:int, anillo:int):
        if(anillo<1 or anillo>5): 
            print("ERROR, El anillo al que se moverá el gancho debe ser un número entero entre 1 y 5")
        elif(hora<1 or hora>10):
            print("ERROR, la hora a la que se moverá el gancho debe ser un número entero entre 1 y 10")
        else:
            hora=math.floor(120+((760/9)*(hora-1)))   # Aqui transformamos el rango de xarm (0-1000) a 10 posiciones que abarcan 180 grados. Modificar el cálculo en caso de necesitar más horas o un ángulo diferente.                     
            self.rob.setPosition(6,hora,2000,True)
            self.rob.setPosition(self.pos[anillo-1],duration=2000,wait=True) 

    # Método para aparentar un saludo
    def saludar(self):
        self.rob.setPosition([[1, 420], [2, 120], [3, 500], [4, 145], [5, 400], [6, 120]],duration=1000,wait=True)
        self.rob.setPosition([[1, 595], [2, 120], [3, 500], [4, 300], [5, 400], [6, 120]],duration=700,wait=True)
        self.rob.setPosition([[1, 495], [2, 120], [3, 500], [4, 0], [5, 400], [6, 120]],duration=700,wait=True)
        self.rob.setPosition([[1, 250], [2, 120], [3, 500], [4, 300], [5, 400], [6, 120]],duration=700,wait=True)
        self.rob.setPosition([[1, 595], [2, 120], [3, 500], [4, 0], [5, 400], [6, 120]],duration=700,wait=True)
        self.rob.setPosition([[1, 395], [2, 120], [3, 500], [4, 145], [5, 400], [6, 120]],duration=1000,wait=True)

    # Método que lleva un cubo de la posición inicial de la garra al sensor de color y lo lee
    # La posición puede cambiar al modificar el plano y movimiento de la garra
    # Op es un parámetro que indica si se regresará el color en formato RGB o 'red', 'green' o 'blue'
    def leeColor(self,op:int=0):
        self.rob.setPosition([[2, 500], [3, 130], [4, 145], [5, 240], [6, 50]],duration=2000,wait=True)
        time.sleep(2.5)
        return self.sen.getColor(op)

    # Método que recibe una posición y hace que la garra recoja el bloque que esté en ella y le aplica el método leeColor()
    def mueveBloque2Color(self,hora:int,anillo:int):
        self.mover(hora,anillo)
        self.agarra()
        self.resetPosition()
        return self.leeColor()
    
    # Método para ir a la posición inicial
    # Facilita los movimientos de la garra y previene la colisión con objetos cercanos.
    def resetPosition(self):
        self.rob.setPosition([[3, 265],[4, 340],[5, 535],[6, 500]],duration=2000,wait=True)
