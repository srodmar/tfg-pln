from langdetect import detect, detect_langs
from chardet.universaldetector import UniversalDetector
#from chardet import detect as detectc
import codecs
import os

#l = detect("War doesn't show who's right, just who's left.")
#print(l)

detector = UniversalDetector()
results = []
store_dir = 'storage/body_texts'
for file in os.listdir(store_dir):
    if file.endswith(".txt"):
        with open(store_dir + '/' + file, 'r') as myfile:
            data = ''
            for line in myfile.readlines():
                data += line
                detector.feed(line)
                #if detector.done: break
            detector.close()
            #data = myfile.read().replace('\n', '')
            #print(detector.result)
        #char = detectc(data)
        #print 'ENC: ' + str(detector.result['encoding'])
        #if cont == 7:
        #    print 'HOLA: ' + data[2192] + ' - ' + data[0]
        #print data
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
print stats
