# -*- coding: utf-8 -*-
###############################################################################
#  Fco. Javier Rodriguez Navarro 
#
#  Esclavo.py: Clase que tendra los datos de los esclavos conectados, uno por
#              cada esclavo, desde ella se realizan los envios y recepción de 
#              información
#
#  Historico:
#     - 12/5/2019 1.0 Version inicio para curso CHEE.
#
###############################################################################
import sys
import socket
import logging
import pickle
import datetime
import time
import base64

class Esclavo():
    def __init__(self, socketcliente,nombre, Clave):
        self.socketcliente = socketcliente   # Socket por el que se realiza la conexión
        self.nombre = nombre   # Nombre del Hilo
        self.Clave = Clave

        datos = self.recibe()
        logging.info("Se solicita conexión: %s",datos)
        param=datos[2:]
        parametros={}        
        parametros = pickle.loads(param)    

        self.hostname = parametros.get('H1')
        self.arquitectura = parametros.get('H2')
        # Actualizamos el nombre del hilo con la arquitectura y Host.
        self.nombre = self.nombre + " "+self.arquitectura+" ("+ self.hostname+")"
        logging.info("Conexta: %s",self.nombre)
       
        #Genera la nueva clave
        since = datetime.datetime(2019, 5, 2, 2, 5, 19) 
        mytime = datetime.datetime.now() 
        diff_seconds = (mytime-since).total_seconds()
        nclave = str(diff_seconds-2019)+"RATCP8: "+str(diff_seconds+2019)
        self.envia(nclave)  #Envia la clave 
        self.Clave = nclave

################################################################################
#   METODOS de la clase
################################################################################
    def getNombre(self):
        return self.nombre

################################################################################
#   envia(mensaje) Envia mensaje.
#   recibe(tamano) Recibe datos, tamaño si es mas de 1024.
################################################################################     
    def envia(self, mensaje):

        #Realizamos la encriptación y el Base64
        mensaje = self.encripta(mensaje)
        totalenviado =0
        longitud = len(mensaje)

        # Pasamos la longitud   
        datos = str(longitud).zfill(24) #Relleno 0 hasta 24 bytes
        logging.info("Envia longitud --> %s",datos)
        while totalenviado < 24:
            enviado = self.socketcliente.send(datos[totalenviado:])
            if enviado == 0:
                logging.error("Conexión ROTA")
            totalenviado = totalenviado + enviado

        # Pasamos los datos
        logging.info("Envia --> %s <-- %s >--",mensaje[:15],mensaje[-15:])
        totalenviado = 0  
        while totalenviado < longitud:
            enviado = self.socketcliente.send(mensaje[totalenviado:])
            if enviado == 0:
                logging.error("Conexión ROTA")
            totalenviado = totalenviado + enviado

    def recibe(self):
        buf = b''
        tamano = 0
        # Recogemos la longitud del mensaje a recibir.
        while len(buf) < 24:
            recibido = self.socketcliente.recv(24-len(buf))
            buf = buf + recibido
  
        tamano = int(buf[:24])
        logging.info("Se esperan %d datos",tamano)
          
        # Recogemos el mensaje
        buf = b''
        while len(buf) < tamano:
            recibido = self.socketcliente.recv(tamano-len(buf))
            buf = buf + recibido
                    
        logging.info("FIN recepción %d-->%s<-->%s",len(buf),buf[:15],buf[-15:])

        return self.desencripta(buf)
      

################################################################################
#   encripta(mensaje) Encripta mensaje y lo retorna encriptado.
#   desencripta(mensaje) Desencripta mensaje y lo retorna limpio.
################################################################################
    def encripta(self,mensaje):
        mensaje = base64.encodestring(mensaje)
        return mensaje
    def desencripta(self,mensaje):
        mensaje = base64.decodestring(mensaje + '=' * (-len(mensaje) % 4))
        return mensaje 

