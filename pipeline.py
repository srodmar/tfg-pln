# encoding: utf-8
import os
import shlex
import subprocess
import time
import pprint

from gmail import main as collect_mails
from lang_detect import detect_classify
from pycorenlp import StanfordCoreNLP
from ssh_iaas import launch_corenlp
from pyfreeling import Analyzer

# Se lanza la recogida de correos electrónicos
# collect_mails()

# Se analizan los correos y se muestran los idiomas detectados
# detect_classify()

# Detectar idioma correo -> lanzar Stanford para ese idioma -> Procesar con StanfordCoreNLP
# Problema: hay que cerrar y volver a lanzar Stanford con cada cambio de idioma
# Solución: dividir los correos por idioma y lanzar una instancia del
# servidor por cada idioma

store_dir = 'storage/body_texts/classified'
port = 8081

server_ports = {}
for dir in os.listdir(store_dir):
    if dir in idiomas:
        launch_corenlp(idiomas[dir], str(port))
        server_ports[dir] = port
        port += 1
    elif dir == 'en':
        launch_corenlp(None, str(port))
        server_ports[dir] = port
        port += 1
