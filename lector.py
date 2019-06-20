from pygame import mixer # Load the required library
from gpiozero import OutputDevice
from datetime import datetime
import time, serial, sys, logging
import serial

#Configuraciones
codigo_ganador = '98761234'
relay_pin = 23
logging.basicConfig(level = logging.INFO, filename = "/home/pi/lector/lector.log")

#configurando gpi
relay = OutputDevice(relay_pin,active_high=False, initial_value=True)
logging.info("Configurando pines")
time.sleep(1)
#iniciando mixer
mixer.init()
logging.info( str(datetime.now()) + ": Iniciando mixer y configurando")
mixer.music.load('/home/pi/lector/init.mp3')
mixer.music.play()
relay.on()
logging.info("activando rele")
time.sleep(4)
relay.off()
ultimo_leido = ""
logging.info(str(datetime.now()) + ": Listo para leer")

while True:
    try:  
        ser = open('/dev/tty1','rb')
        #ser = serial.Serial('/dev/tty1',9600)
        #codigo_leido = ser.read(256)
        codigo_leido = ser.read(8)
        logging.info( str(datetime.now()) + " - Leido por serial: " + str(codigo_leido))
        if codigo_leido!= "" :
            if codigo_ganador in str(codigo_leido) :
            #gana
                mixer.music.load('/home/pi/lector/1.mp3')
                mixer.music.play()
                relay.on()
                time.sleep(3)
                mixer.music.stop()
                relay.off()
            else: 
                #pierde
                mixer.music.load('/home/pi/lector/2.mp3')
                mixer.music.play()
                time.sleep(3)
                mixer.music.stop()
            ultimo_leido = codigo_leido
        else:
            ultimo_leido = ""
    except Exception as error:
        logging.info(( str(datetime.now()) + "ERROR: ",error) )
