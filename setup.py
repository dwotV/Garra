from setuptools import setup, find_packages

version = '1.0.0'
description = 'Un paquete de python para la garra xArm Uno.'
long_description = 'Un paquete de python para poder utilizar de manera sencilla el modelo de garra xArm Uno de la maraca Hiwonder.'

#Configrurado
setup(
    name='Garra-main',
    version=version,
    author='Andrea Bahena Valdés, José de Jesús Becerra González, Miguel Ángel Pérez Ávila, Santiago Albarrán Organista, Deal Chávez Ferreyra',
    author_email='<daelcferreyra@gmail.com>',
    description=description,
    long_description=long_description,
    packages=find_packages(),
    install_requires=['xarm, setuptools, hidapi, time, pyserial, serial'],

    keywords=['garra', 'xArm Uno', 'Hiwonder', 'Python', 'Python3'],    
    classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
    ]
)
