# Garra

**Descripción:**
Este proyecto permite programar con Python un brazo robótico (xArm-UNO).
También permite una manipulación primaria del módulo de sensores externos.

  1. Sensor de presencia
  2. Sensor de color
  3. Sensor ultrasónico (o de distancia)
  4. Sensor de tacto
  5. Sensor de sonido 
     
Es una excelente opción para quienes desean empezar a desarrollar lógica de programación de forma intuitiva y visualizarla en Hardware.

# ¿Cómo funciona?
# Requisistos


## Dependencias de Software
- [Python](https://www.python.org/).
- [Pip](https://pypi.org/project/pip/).
- [Arduino](https://www.arduino.cc/en/software).

### Instalación de librerias necesarias

#### Controlar el brazo (xArm-UNO)
##### Instalación (Windows)
```
> pip install --upgrade setuptools
> pip install hidapi
> pip install xarm
```
##### Instalación (Linux, MacOS y Raspberry Pi)
- https://github.com/ccourson/xArmServoController/tree/main/Python#installation-linux-macos-and-raspberry-pi

#### Utilizar los sensores
```
> pip install pyserial
> pip install time
```
