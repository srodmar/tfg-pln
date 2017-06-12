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
from store_results import insert_email

# Se lanza la recogida de correos electrónicos
# collect_mails()

# Se analizan los correos y se muestran los idiomas detectados
# detect_classify()

# Detectar idioma correo -> lanzar Stanford para ese idioma -> Procesar con StanfordCoreNLP
# Problema: hay que cerrar y volver a lanzar Stanford con cada cambio de idioma
# Solución: dividir los correos por idioma y lanzar una instancia del
# servidor por cada idioma

logging.basicConfig(filename="sample.log", filemode='w', level=logging.DEBUG)


def clean_text(text, lang='english'):
    try:
        stopw = stopwords.words(lang)
    except IOError:
        print 'No hay stopw para: ' + lang
        stopw = []
    exclude = set(string.punctuation)
    exclude.update(['¿'.decode('UTF-8'), '¡'.decode('UTF-8'), '~'])
    # print exclude
    text = text.decode('utf-8')
    # Se crea un array con todas las palabras del texto que no sean stopwords
    # y luego se uno dicho array separando cada item por un espacio (" ")
    stop_free = " ".join([i for i in text.lower().split() if i not in stopw])
    # Se recorren todos los caracteres del string y se incluyen solo los que no
    # son símbolos de puntuación
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    return punc_free.encode('utf-8')


def get_topic(topic_list):
    max_topic_id = -1
    max_prob = -1
    for topic in topic_list:
        if topic[1] > max_prob:
            max_prob = topic[1]
            max_topic_id = topic[0]
    return max_topic_id

store_dir = 'storage/body_texts/classified'
idiomas = {'ca': 'catalan', 'en': 'english', 'es': 'spanish', 'fr': 'french',
           'gl': 'galician', 'it': 'italian', 'pt': 'portuguese',
           'ru': 'russian', 'de': 'german', 'nl': 'dutch', 'sl': 'slovene'}
#port = 8081
idiomas_freeling = ['as', 'ca', 'cy', 'en', 'es', 'fr', 'gl', 'it', 'pt', 'ru']
analyzer = {}

for lang in os.listdir(store_dir):
    if lang in idiomas_freeling:
        print 'funciona el dir: ' + str(lang)
        analyzer = Analyzer(config=lang + '.cfg')
    else:
        analyzer = None
# print analyzer
# for lang in analyzer:
    # print 'ANALIZANDO ' + lang
    # if lang == 'es':
    texts_dir = store_dir + '/' + lang
    lang_lemmas = {}
    file_list = os.listdir(texts_dir)
    for file in file_list:
        print('FILE EN PROBLEMAS: ' + file)
        with open(texts_dir + '/' + file, 'r') as current_file:
            text = current_file.read()
        # print 'IDIOMA: ' + lang + ' TEXT: ' + text
        if lang in idiomas:
            ctext = clean_text(text, idiomas[lang])
        else:
            ctext = clean_text(text)
        if analyzer:
            lemmas = extract_lemmas(analyzer, ctext)
        else:
            lemmas = ctext.split()
        logging.info(lemmas)
        # Agrego cada array de lemmas al diccionario, con su mail id como clave
        lang_lemmas[file[10:-4]] = (lemmas, text)
    dictionary = gensim.corpora.Dictionary(
        [tuple[0] for id, tuple in lang_lemmas.viewitems()])
    email_term_matrix = [dictionary.doc2bow(
        tuple[0]) for id, tuple in lang_lemmas.viewitems()]
    lda = gensim.models.ldamodel.LdaModel(
        email_term_matrix, num_topics=10, id2word=dictionary, passes=20)
    # print lda.show_topics(num_topics=10, num_words=5)
    for mail_id in lang_lemmas:
        mail_topic = get_topic(lda.get_document_topics(
            dictionary.doc2bow(lang_lemmas[mail_id][0])))
        insert_email(mail_id, lang_lemmas[mail_id][
                     1], lda.show_topic(mail_topic, topn=5))
        # print 'Mail: %s - Topic: %s' % (id, lda.show_topic(mail_topic, topn=5))
