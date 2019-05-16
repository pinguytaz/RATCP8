# RATCP8 (Construcción de un RAT en Python)
[![license](https://www.pinguytaz.net/IMG_GITHUB/gplv3-with-text-84x42.png)](https://github.com/pinguytaz/RATCP8/blob/master/LICENSE)
[![license](https://www.pinguytaz.net/IMG_GITHUB/python-logo.png)](https://www.python.org/)


__AVISO LEGAL Y RENUNCIA DE RESPONSABILIDADES__
RATCP8 es un proyecto de código abierto con el unico fin de educación e investigación para desarrolladores de seguridad, y que pueda ayudar a crear contramedidas para las amenzas actuales.

El autor __NO asume ninguna responsabilidad__ por la forma en que elija utilizar cualquiera de los ejecutables/código fuente de cualquier archivo provistos. El autor y cualquier persona afiliada no serán responsables de ninguna pérdida o daño en relación con el uso de CUALQUIER archivo incluido en RATCP8. Al utilizar RATCP8 o cualquier contenido incluido, usted ACEPTA USARLO BAJO SU PROPIO RIESGO. Una vez más, RATCP8 y TODOS los archivos incluidos son SOLAMENTE para fines de EDUCACIÓN y/o INVESTIGACIÓN. RATCP8 SOLO está destinada a ser utilizada en sus propios laboratorios de pruebas, o con el consentimiento explícito del propietario de la propiedad que se este probando.


##Acerca de RATCP8
Es un RAT generado en Python, cuya finalidad es educativa generando para eso dos modulos:
    *S_RAT.py* es el modulo que se ejecuta en la maquina que deseamos tomar el control, esclavo, pero que sera este el modulo que inicie la comunicacion con el maestro indicando que ya esta disponible (Conexión inversa).
             Se realiza un fork para que despues de ejecutarse quede en memoria como si de un demonio se tratase, esta parte de código es necesaria cambiarla para compatibilizarla con Windows.
             Esta primera versión solo es ejecutable en Linux.
    *M_RAT.py* es el modulo que se ejecuta en nuestra maquina y es la que toma el control de las maquinas esclavo. Para esta version se han desarrollado dos simples funciones pero se iran añadiendo funciones segun deseemos profundiczar en la investigación del lenguaje python y ejecución remota para gestión de seguridad y administración remota de equipos.
             La ejecución de los comandos y desconexiones a los esclavos se realiza mediante un interfaz grafico.

RATCP8 tiene las varias caracteristicas tipicas de los RATs (Herramientas de control remoto) y BOTs (Varios equipos controlados por un unico maestro) para realizar el estudio de como trabajan estos sistemas y de esa forma poder denfendernos ante ellos.
    1.- Sistema maestro capaz de recibir distintas conexiones de sus esclavos y de forma independiente trabajar sobre ellos mediante un simple protocolo de comunicación.
    2.- Protocolo de comunicación encriptado, en este caso la encriptación es muy basica ya que se trata de un simple Base64 pero esta preparado para añadir cualquier sistema de cifrado (ya que pasamos contraseña en el protocolo) y que se realizar en versiones más adelante de forma que nos permita estudiar y realizar detectores de trafico anomalo aunque este este encriptado para protegernos ante ellos.
    3.- Ejecución en memoria evitando dejar rastros en el disco del sistema atacado.
    4.- Ejecución de codigo generado remotamente, de forma que un analisis inicial de la memoria no detecta codigo malicioso en principio.


Funciones de RATCP8
    1.- Captura remota de la pantalla del esclavo.
    2.- Ejecución de una ventana avisando que ha sido hackeado, esta se realiza dinamicamente desde el maestro con el envio del codigo del archivo Hack.cod. Este es el principio para generar una funcion que lance codigo remoto sin necesidad de generar un nuevo esclavo.

__Estructura del código__
*S_RAT* codigo del esclavo en un unico fichero para facilitar el convertirlo en ELF o EXE.

*M_RAT* código del maestro con sus diferentes ficheros, y dos directorios:
      1) \Codigos en este directorio estaran los ficheros de ejecución remota en esta primera version "Hack.cod"
      2) \Descargas Donde se descargaran las capturas de pantalla obtenidas.

__Website__: https://www.pinguytaz.net
