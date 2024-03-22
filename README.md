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
1. Requisitos
   * Dependencias de Software
   * Instalación de librerías  
3. Instrucciones
4. Ejemplo de uso
   
## Requisitos

## Dependencias de Software

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
