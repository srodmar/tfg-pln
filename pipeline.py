# encoding: utf-8
import os
import shlex
import subprocess
import time
import pprint
import gensim
from nltk.corpus import stopwords

from gmail import main as collect_mails
from lang_detect import detect_classify
from pyfreeling import Analyzer
from test_pyfreeling import extract_lemmas

# Se lanza la recogida de correos electrónicos
# collect_mails()

# Se analizan los correos y se muestran los idiomas detectados
# detect_classify()

# Detectar idioma correo -> lanzar Stanford para ese idioma -> Procesar con StanfordCoreNLP
# Problema: hay que cerrar y volver a lanzar Stanford con cada cambio de idioma
# Solución: dividir los correos por idioma y lanzar una instancia del
# servidor por cada idioma

spanish_stopwords = stopwords.words('spanish')

store_dir = 'storage/body_texts/classified'
idiomas = ['as', 'ca', 'cs', 'de', 'en', 'es',
           'fr', 'gl', 'it', 'no', 'pt', 'ru', 'sl']
#port = 8081

analyzer = {}
for dir in os.listdir(store_dir):
    if dir in idiomas:
        analyzer[dir] = Analyzer(config = dir + '.cfg', lang=dir)

for lang in analyzer:
    if lang == 'es':
        texts_dir = store_dir + '/' + lang
        for file in os.listdir(texts_dir):
            print('FILE EN PROBLEMAS: ' + file)
            with open(texts_dir + '/' + file, 'r') as current_file:
                text = current_file.read()
            print 'IDIOMA: ' + lang + ' TEXT: ' + text
            lemmas = extract_lemmas(analyzer[lang], text)
            print lemmas
            if lang == 'es':
                for word in lemmas:
                    if word in spanish_stopwords:
                        lemmas.remove(word)
                print lemmas
                dictionary = gensim.corpora.Dictionary([lemmas])
                lda = gensim.models.ldamodel.LdaModel(lemmas, num_topics=3, id2word = dictionary, passes=50)
                print lda.show_topics(num_topics=3)
                print 'MODEEEEEL: '
                print model
