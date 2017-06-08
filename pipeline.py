# encoding: utf-8
import os
import shlex
import subprocess
import time
import pprint
import gensim
import string
import logging
from nltk.corpus import stopwords

from gmail import main as collect_mails
from lang_detect import detect_classify, detect_classify_fl
from pyfreeling import Analyzer
from test_pyfreeling import extract_lemmas

# Se lanza la recogida de correos electrónicos
collect_mails()

# Se analizan los correos y se muestran los idiomas detectados
detect_classify()

# Detectar idioma correo -> lanzar Stanford para ese idioma -> Procesar con StanfordCoreNLP
# Problema: hay que cerrar y volver a lanzar Stanford con cada cambio de idioma
# Solución: dividir los correos por idioma y lanzar una instancia del
# servidor por cada idioma

logging.basicConfig(filename="sample.log", filemode='w', level=logging.DEBUG)


def clean_text(text):
    stopw = stopwords.words('spanish')
    exclude = set(string.punctuation)
    exclude.update(['¿'.decode('UTF-8'), '¡'.decode('UTF-8'), '~'])
    print exclude
    text = text.decode('utf-8')
    # Se crea un array con todas las palabras del texto que no sean stopwords
    # y luego se uno dicho array separando cada item por un espacio (" ")
    stop_free = " ".join([i for i in text.lower().split() if i not in stopw])
    # Se recorren todos los caracteres del string y se incluyen solo los que no
    # son símbolos de puntuación
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    return punc_free.encode('utf-8')

spanish_stopwords = stopwords.words('spanish')

store_dir = 'storage/body_texts/classified'
idiomas = {'ca': 'catalan', 'cs': '', 'en': 'english', 'es': 'spanish',
           'fr': 'french', 'gl': 'galician', 'it': 'italian', 'pt': 'portuguese', 'ru': 'russian'}
#port = 8081

analyzer = {}
for dir in os.listdir(store_dir):
    if dir in idiomas:
        print 'funciona el dir: ' + str(dir)
        analyzer[dir] = Analyzer(config=dir + '.cfg', lang=dir)
print analyzer
for lang in analyzer:
    print 'ANALIZANDO ' + lang
    # if lang == 'es':
    texts_dir = store_dir + '/' + lang
    lang_lemmas = []
    file_list = os.listdir(texts_dir)
    for file in file_list:
        print('FILE EN PROBLEMAS: ' + file)
        with open(texts_dir + '/' + file, 'r') as current_file:
            text = current_file.read()
        # print 'IDIOMA: ' + lang + ' TEXT: ' + text
        ctext = clean_text(text)
        lemmas = extract_lemmas(analyzer[lang], ctext)
        logging.info(lemmas)
        # print lemmas
        lang_lemmas.append(lemmas)
    dictionary = gensim.corpora.Dictionary(lang_lemmas)
    email_term_matrix = [dictionary.doc2bow(email) for email in lang_lemmas]
    lda = gensim.models.ldamodel.LdaModel(
        email_term_matrix, num_topics=10, id2word=dictionary, passes=20)
    #print lda.show_topics(num_topics=10, num_words=5)
    print lda.get_document_topics(dictionary.doc2bow(lang_lemmas[0]))
    # print 'MODEEEEEL: '
    # print model
