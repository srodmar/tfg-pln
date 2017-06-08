from langdetect import detect, detect_langs
from chardet.universaldetector import UniversalDetector
from pyfreeling import Analyzer
from lxml import etree
import codecs
import os
import xmltodict

store_dir = 'storage/body_texts'

def detect_all():
    detector = UniversalDetector()
    results = []
    for file in os.listdir(store_dir):
        if file.endswith(".txt"):
            with open(store_dir + '/' + file, 'r') as myfile:
                data = ''
                for line in myfile.readlines():
                    data += line
                    detector.feed(line)
                    #if detector.done: break
                detector.close()
            # Si se pudo detectar el encoding del fichero
            if detector.result['encoding']:
                print(detect_langs(data.decode(detector.result['encoding'])))
                dlang = detect(data.decode(detector.result['encoding']))
                if dlang == 'fr':
                    print data
                results.append({'mail': file, 'lang': dlang})
            else:
                results.append({'mail': file, 'lang': 'error'})

    stats = {}
    for result in results:
        lang = result['lang']
        if lang in stats:
            stats[lang] = stats[lang] + 1
        else:
            stats[lang] = 1
        if lang != u'en':
            print str(lang) + ' - ' + str(result['mail'])
    return stats

def detect_classify():
    detector = UniversalDetector()
    for file in os.listdir(store_dir):
        if file.endswith(".txt"):
            with open(store_dir + '/' + file, 'r') as myfile:
                data = ''
                for line in myfile.readlines():
                    data += line
                    detector.feed(line)
                    #if detector.done: break
                detector.close()
            # Si se pudo detectar el encoding del fichero
            if detector.result['encoding']:
                dlang = detect(data.decode(detector.result['encoding']))
                move_dir = '/classified/' + str(dlang)
            else:
                move_dir = '/classified/errors'

            if not os.path.exists(store_dir + move_dir):
                os.makedirs(store_dir + move_dir)
            os.rename(store_dir + '/' + file, store_dir + move_dir + '/' + file)

def detect_classify_fl():
    detector = UniversalDetector()
    for file in os.listdir(store_dir):
        if file.endswith(".txt"):
            with open(store_dir + '/' + file, 'r') as myfile:
                data = ''
                for line in myfile.readlines():
                    data += line
                    detector.feed(line)
                    #if detector.done: break
                detector.close()
            # Si se pudo detectar el encoding del fichero
            if detector.result['encoding']:
                analyzer = Analyzer(config='ident.cfg', outlv='ident')
                dlang = analyzer.run(data)
                obj = xmltodict.parse(etree.tostring(dlang))
                print file + ' - lan: ' + obj['sentences']
                move_dir = '/classified/fl_' + str(obj['sentences'][:2])
            else:
                move_dir = '/classified/errors'

            if not os.path.exists(store_dir + move_dir):
                os.makedirs(store_dir + move_dir)
            os.rename(store_dir + '/' + file, store_dir + move_dir + '/' + file)

if __name__ == '__main__':
    detect_classify()
