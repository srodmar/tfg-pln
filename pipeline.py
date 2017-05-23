# encoding: utf-8
import os
import shlex
import subprocess
import time

from gmail import main as collect_mails
from lang_detect import detect_classify
from pycorenlp import StanfordCoreNLP

# Se lanza la recogida de correos electrónicos
# collect_mails()

# Se analizan los correos y se muestran los idiomas detectados
# detect_classify()

# Detectar idioma correo -> lanzar Stanford para ese idioma -> Procesar con StanfordCoreNLP
# Problema: hay que cerrar y volver a lanzar Stanford con cada cambio de idioma
# Solución: dividir los correos por idioma y lanzar una instancia del
# servidor por cada idioma

# lista de idiomas que soporta StanfordCoreNLP
idiomas = {'ar': 'arabic', 'zh': 'chinese',
           'fr': 'french', 'de': 'german', 'es': 'spanish'}
store_dir = 'storage/body_texts/classified'
port = 9000
current_dir = os.getcwd()
processes = []


def call(command):
    args = shlex.split(command)
    return subprocess.Popen(args)


def kill(processes):
    for p in processes:
        p.terminate()

server_ports = {}
for file in os.listdir(store_dir):
    if file in idiomas:
        os.chdir('stanford-corenlp-full-2016-10-31')
        command = 'java -Xmx2048m -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -serverProperties StanfordCoreNLP-' + \
            idiomas[file] + '.properties -port ' + \
            str(port) + ' -timeout 15000'
        processes.append(call(command))
        server_ports[file] = port
        port += 1
        os.chdir(current_dir)
    elif file == 'en':
        os.chdir('stanford-corenlp-full-2016-10-31')
        command = 'java -mx2048m -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port ' + \
            str(port) + ' -timeout 15000'
        processes.append(call(command))
        server_ports[file] = port
        port += 1
        os.chdir(current_dir)

time.sleep(20)

for lan in server_ports:
    nlp = StanfordCoreNLP('http://localhost:' + str(server_ports[lan]))
    text = ('Hola, mi nombre es Manolo y esta es la historia de mi vida')
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse',
        'outputFormat': 'json'
    })
    #print(output)
    print(output['sentences'][0]['parse'])
print('A MATAR')
kill(processes)
