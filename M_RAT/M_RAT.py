#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Fco. Javier Rodriguez Navarro 
#
#  M_RAT.py: Programa Maestro que controla en remoto a un ordenador que
#             tenga S_RAT ejecutandose.
#
#  Historico:
#     - 12/5/2019 1.0 Version inicio para curso CHEE.
#
###############################################################################
import sys
import logging
import os

import VN_Principal

#import datetime
#from Crypto.Cipher import ARC4
#import pickle

#Configurar Variables 
PORT = 8484
Clave = "ElCursoCHEEPractica8"

logging.basicConfig(level=logging.DEBUG) # Poner CRITICAL en prod.

def main(argv):
  
    # Creamos la ventana principal.
    vn_principal = VN_Principal.VN_Principal(PORT,Clave)
   
    sys.exit(0)
  

################# Lanzamiento de la funcion principal ##########################
if __name__ == "__main__":
    main(sys.argv)
