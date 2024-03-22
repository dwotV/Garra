# Garra

**Descripción:**
Este proyecto permite programar con Python un brazo robótico (xArm-UNO).
También permite una manipulación primaria del módulo de sensores externos que está incluido en la compra del robot.

  1. Sensor de presencia
  2. Sensor de color
  3. Sensor ultrasónico (o de distancia)
  4. Sensor de tacto
  5. Sensor de sonido 
     
Al ser un lenguaje de alto nivel, se utilizó Python para el diseño de la interfaz (las funciones).Esto supone una excelente opción para quienes desean empezar a desarrollar lógica de programación de forma intuitiva y visualizarla en Hardware.

Puesto que tanto el Hardware como el Software están en constante evolución, es probable que se requiera modificar el código en el futuro para que sea congruente con las versiones contemporáneas de Arduino.

## Tabla de contenidos
1. [Requisitos](#requisitos)
   * Dependencias de Software
   * Instalación de librerías
2. [Protocolo](#protocolo)
   * Métodos de la clase
       * Garra
       * Sensor
3. [Instrucciones](#instrucciones)
4. Ejemplo de uso
   
## Requisitos
<a name="requisitos"></a>

### Dependencias de Software

Para el funcionamiento del código, se requiere la instalación del siguiente software:
_Al desarrollar el proyecto se utilizó Python 3.11 y Arduino 2.3.2_

- [Python](https://www.python.org/).
- [Pip](https://pypi.org/project/pip/).
- [Arduino](https://www.arduino.cc/en/software).

Se sugiere utilizar algún editor de texto para visualizar el código, pero no es indispensable.
-[Visual Studio Code](https://code.visualstudio.com/download).

### Instalación de librerias 
Los comandos deben ser ejecutados exactamente en el orden especificado.
#### Controlar el brazo (xArm-UNO)
Las siguientes librerías se utilizan para controlar el brazo robótico:
##### Instalación (Windows)
```
> pip install --upgrade setuptools
> pip install hidapi
> pip install xarm
```
##### Instalación (Linux, MacOS y Raspberry Pi)
- https://github.com/ccourson/xArmServoController/tree/main/Python#installation-linux-macos-and-raspberry-pi

#### Utilizar los sensores
La instalación de las siguientes librerías solo es necesaria si se desea utilizar la placa de sensores incluida con el brazo:

```
> pip install pyserial
> pip install time
```
## Protocolo
<a name="protocolo"></a>
### Garra

La clase Garra posee los atributos posición y robot.
'Pos' es un array bidimensional que guarda dos enteros en el formato [[sn, v],[sn, v] … ], donde sn es el número del servo motor y v el valor que controla su movimiento.

| Nombre de la función | Descripción | Parámetros | Ejemplo de uso |
| -------------------- | ----------- | ---------- | -------------- |
| conecta() | Conectar con el robot vía USB | N/A | conecta() |
| agarra() | Cierra la garra para tomar un objeto de 3 cm de radio| N/A | agarra()|
| suelta() | Abre la garra por completo | N/A | suelta() |
| mover() | Moviliza la garra en un ángulo y radio específicos | mover(hora, anillo) | mover(2, 5) |
| saludar() | Simula un saludo a través de movimientos del brazo | N/A | saludar()|
| leeColor() | Moviliza un objeto de la posición inicial de la garra al sensor de color para leerlo, con opción de desplegarlo como RGB (op = 0) o 'red' (op = 1) |  leeColor(op) | leeColor(1)|
| mueveBloque2Color | Recibe una posición, recoje el bloque en dicha posición y lee su color | mueveBloque2Color(hora, anillo) | mueveBloque2Color(8, 3)|
| resetPosition() | Moviliza la garra a la posición inicial | N/A | resetPosition() |


### Sensor
La clase sensor posee el atributo 'ard', haciendo referencia a Arduino.
Color: (R,G,B)
Sonido: (Bool)
Touch: (int) - 0= culquier toque, 1= toque corto, 2= toque largo
Distancia: (float)
Presencia: (lista[str])
| Nombre de la función | Descripción | Parámetros | Ejemplo de uso |
| -------------------- | ----------- | ---------- | -------------- |
| conectar() | Conecta la placa Arduino al puerto indicado (str) | conectar(puerto) | conectar('COM3')|
| leerSens() | Hace una lectura de todos los sensores y retorna una lista con las entradas en el siguiente orden: color, sonido, touch, distancia, presencia | leerSens(list[])| leerSens(list[list[1,2,3], True, 1, 3.54, list[0,0,0])|
| desColor() | Muestra la información del sensor de color en el display | (N/A) | desColor()|
|desDistance()|Muestra la información del sensor de distancia en el display | (N/A) | desDistance()|
|desPresence()|Muestra la información del sensor de presencia en el display | (N/A) | desPresence()|
|getColor() | Devuelve la lectura del color con opción de desplegarlo como RGB (op = 0) o 'red' (op = 1) | getColor(op) | getColor(0)|
|isColor() | Compara si se cumple la condición del color en la lectura | isColor(color) | isColor('red') o isColor([9,32,15]) |
| getSound() | Devuelve la lectura del sensor de sonido (si se detectó o no) | N/A | getSound() |
| getTouch() | Devuelve la lectura del sensor de touch (0= cualquiera, 1= corto, 2= largo) | N/A | getTouch() |
|isTouch()| Si se detecta un touch, valida que se detecte un sonido| N/A| isTouch()|
|isShortTouch()| Si se detecta un touch corto, valida que el sonido sea corto| N/A| isShortTouch()|
|isLongTouch()| Si se detecta un touch largo, valida que el sonido sea largo| N/A| isLongTouch()|
|getDistance()|Devuelve la distancia detectada por el sensor de distancia| N/A | getDistance()|
|isDistance()| Devuelve si el objeto se encuentra o no dentro de un rango de distancia | isDistance(infLimit, supLimit) | isDistance(3,8)|
|getPresence()| Devuelve una lista que indica el estado de presencia o no ['0', '0', '0'] índice 0 = izquierda; índice 1= centro; índice 2= derecha| (N/A)| getPresence()|
| isPresence() | Devuelve un booleano que indica si la presencia coincide con la que le indicas | isPresence(id_sensor) | isPresence([1, 0, 0]) |
| until() | Espera hasta que se cumpla una condición con los sensores para regresar True | until (sensor, condición) | until("color", "red") |

## Instrucciones
<a name= "instrucciones"></a>
1. Instalar todas las dependencias de software
2. Descargar la librería "Garra"
3. Instalar el Robot
4. Conectar el Robot
5. Programar utilizando los métodos y funciones necesarias
6. Ejecutar el código

## Ejemplo de uso
<a name= "ejemplo"></a>
```
import Garra
import time

rb=Garra()
rb.conecta()
rb.mover(1,1)
rb.agarra()
rb.resetPosition()
rb.mover(1,1)
rb.suelta()
rb.resetPosition()
for i in range(5):
    for j in range(10):
        rb.mover(j+1,i+1)
        rb.agarra()
        rb.resetPosition()
        if ((j+2)>10):
            continue
        else:
            rb.mover(j+2,i+1)
            rb.suelta()
            rb.resetPosition()
    rb.mover(10,i+1)
    rb.agarra()
    rb.resetPosition()
    if ((i+2)>5):
        continue
    else:
        rb.mover(1,i+2)
        rb.suelta()
        rb.resetPosition()

```


