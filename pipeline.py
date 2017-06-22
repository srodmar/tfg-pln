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
from lang_detect import detect_classify
from pyfreeling import Analyzer
from test_pyfreeling import extract_lemmas
from store_results import insert_email

# Detectar idioma correo -> lanzar Stanford para ese idioma -> Procesar con StanfordCoreNLP
# Problema: hay que cerrar y volver a lanzar Stanford con cada cambio de idioma
# Solución: dividir los correos por idioma y lanzar una instancia del
# servidor por cada idioma


def clean_symbols(word_array):
    aux_array = list(word_array)
    logger.info('WORD ARRAY: %s', word_array)
    symbols = ('[', '>>', '\\', '?', '+', '-', ':', '_', '"', '.', ',', ';', 'http', '#', 'image')
    for word in word_array:
        logger.info('ANALIZANDO: %s', word)
        if word.startswith(symbols) or word[:1].isdigit() or len(word) <= 1 or '/' in word:
            #print 'PALABRA QUE NO MOLA', word
            logger.info('PALABRA QUE NO MOLA: %s', word)
            aux_array.remove(word)

    #print 'ARRAY QUE DEBERÍA MOLAR', aux_array
    logger.info('ARRAY QUE DEBERIA MOLAR: %s', aux_array)
    return aux_array


def clean_text(text, lang='english'):
    try:
        stopw = stopwords.words(lang)
    except IOError:
        print 'No hay stopw para: ' + lang
        stopw = []
    exclude = set(string.punctuation)
    exclude.update(['¿'.decode('UTF-8'), '¡'.decode('UTF-8'), '~', '‘'.decode('UTF-8'),
                    '’'.decode('UTF-8'), '–'.decode('UTF-8')])
    # print exclude
    logger.info('TEXTO ANTES DE LIMPIAR: %s', text)
    text = text.decode('utf-8')
    # Se crea un array con todas las palabras del texto que no sean stopwords
    # y luego se uno dicho array separando cada item por un espacio (" ")
    stop_free = " ".join([i for i in text.lower().split() if i not in stopw])
    # Se recorren todos los caracteres del string y se incluyen solo los que no
    # son símbolos de puntuación
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    symbols_free = clean_symbols(punc_free.split())
    return [word.encode('utf-8') for word in symbols_free]
    # return punc_free.encode('utf-8')


def clean_text_array(text, lang='english'):
    try:
        stopw = stopwords.words(lang)
    except IOError:
        print 'No hay stopw para: ' + lang
        stopw = []
    exclude = set(string.punctuation)
    exclude.update(['¿'.decode('UTF-8'), '¡'.decode('UTF-8'), '~', '‘'.decode('UTF-8'),
                    '’'.decode('UTF-8'), '–'.decode('UTF-8')])
    # print exclude
    logger.info('TEXTO ANTES DE LIMPIAR: %s', text)
    text = [word.encode('utf-8') for word in text]
    # Se crea un array con todas las palabras del texto que no sean stopwords
    # y luego se uno dicho array separando cada item por un espacio (" ")
    stop_free = [word for word in text if word not in stopw]
    # Se recorren todos los caracteres del string y se incluyen solo los que no
    # son símbolos de puntuación
    punc_free = [ch for ch in stop_free if ch not in exclude]
    # return punc_free.encode('utf-8')
    symbols_free = clean_symbols(punc_free)
    return [word.decode('utf-8') for word in symbols_free]


def get_topic(topic_list):
    print 'Lista de tópicos: ', topic_list
    max_topic_id = -1
    max_prob = -1
    for topic in topic_list:
        if topic[1] > max_prob:
            max_prob = topic[1]
            max_topic_id = topic[0]
    print 'topic: ', max_topic_id, ' prob: ', max_prob
    return max_topic_id

def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half], a_list[half:]

def get_lemmas_topics():
    store_dir = 'storage/body_texts/classified'
    idiomas = {'af': 'afrikaans', 'ca': 'catalan', 'en': 'english', 'es': 'spanish', 'fr': 'french',
               'gl': 'galician', 'it': 'italian', 'pt': 'portuguese',
               'ru': 'russian', 'de': 'german', 'nl': 'dutch', 'sl': 'slovene', 'cy': 'welsh'}
    #port = 8081
    idiomas_freeling = ['as', 'ca', 'en', 'es', 'fr', 'gl', 'it', 'pt', 'ru']
    analyzer = {}

    lang_id = 1
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
        if lang not in idiomas:
            print 'LANG RARO', lang
            continue
        texts_dir = store_dir + '/' + lang
        lang_lemmas = {}
        file_list = os.listdir(texts_dir)
        for file in file_list:
            print('FILE EN PROBLEMAS: ' + file)
            with open(texts_dir + '/' + file, 'r') as current_file:
                text = current_file.read()
            # print 'IDIOMA: ' + lang + ' TEXT: ' + text
            '''if lang in idiomas:
                ctext = clean_text(text, idiomas[lang])
            else:
                ctext = clean_text(text)
            print ctext'''
            if analyzer:
                lemmas = extract_lemmas(analyzer, text)
                lemmas = clean_text_array(lemmas, idiomas[lang])
            else:
                lemmas = clean_text(text, idiomas[lang])
            # logger.info(lemmas)
            print 'CLEAN LEMMAS:', lemmas
            # Agrego cada array de lemmas al diccionario, con su mail id como clave
            lang_lemmas[file[-20:-4]] = (lemmas, file[:-21], text)

        lemmas_list = [(i, tup[0]) for i, tup in lang_lemmas.viewitems()]
        dictionary = gensim.corpora.Dictionary([tup[1] for tup in lemmas_list])

        lemmasA, lemmasB = split_list(lemmas_list)

        email_term_matrix = [dictionary.doc2bow(item[1]) for item in lemmasA]
        lda = gensim.models.ldamodel.LdaModel(
            email_term_matrix, num_topics=10, id2word=dictionary, passes=1)

        # print lda.show_topics(num_topics=10, num_words=5)
        for tup in lemmasB:
            mail_id = tup[0]
            mail_topic_id = get_topic(lda.get_document_topics(dictionary.doc2bow(tup[1])))
            insert_email(mail_id, lang_lemmas[mail_id][1], lang_lemmas[mail_id][2],
                         lda.show_topic(mail_topic_id, topn=5), str(lang_id) + str(mail_topic_id))
            # print 'Mail: %s - Topic: %s' % (id, lda.show_topic(mail_topic,
            # topn=5))

        lang_id += 1


if __name__ == '__main__':
    logging.basicConfig(filename="sample.log", filemode='w', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)

    # Se lanza la recogida de correos electrónicos
    #collect_mails()

    # Se analizan los correos y se muestran los idiomas detectados
    #detect_classify()

    # Se consiguen los lemmas de cada palabra de los correos y se extraen tópicos
    get_lemmas_topics()
