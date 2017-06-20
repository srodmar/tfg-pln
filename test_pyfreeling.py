import xmltodict
import pprint

#from pyfreeling import Analyzer
from lxml import etree
pp = pprint.PrettyPrinter(indent=4)
'''


analyzer = Analyzer(config='en.cfg')
xml = analyzer.run('Hello World, This is me.', 'noflush')
print(etree.tostring(xml))
obj = xmltodict.parse(etree.tostring(xml))

#pp.pprint(obj['sentences']['sentence'])

if isinstance(obj['sentences']['sentence'], list):
    for sentence in obj['sentences']['sentence']:
        for token in sentence['token']:
            print token['@lemma']
else:
    for token in obj['sentences']['sentence']['token']:
        print token['@lemma']

analyzer = Analyzer(config='es.cfg', lang='es')

output = analyzer.run('Hola mundo', 'noflush')
print(etree.tostring(output))
'''
def extract_lemmas(analyzer, text):
    xml = analyzer.run(text)
    print xml
    obj = xmltodict.parse(etree.tostring(xml))
    #print obj
    lemmas = []
    if obj['sentences']:
        if isinstance(obj['sentences']['sentence'], list):
            for sentence in obj['sentences']['sentence']:
                #print 'LA FRASE:'
                #pp.pprint(sentence['token'])
                if isinstance(sentence['token'], list):
                    for token in sentence['token']:
                        #print 'TOKEN list:'
                        #pp.pprint(token)
                        if token['@tag'].startswith(('NP', 'NNP')):
                            #print 'ESTEEE NOOOOOOOOOO:', token['@lemma']
                            continue
                        lemmas.append(token['@lemma'])
                else:
                    token = sentence['token']
                    if token['@tag'].startswith(('NP', 'NNP')):
                        #print 'ESTEEE NOOOOOOOOOO:', token['@lemma']
                        continue
                    lemmas.append(token['@lemma'])
        else:
            if isinstance(obj['sentences']['sentence']['token'], list):
                for token in obj['sentences']['sentence']['token']:
                    #print 'TOKEN no list:', token
                    if token['@tag'].startswith(('NP', 'NNP')):
                        #print 'ESTEEE NOOOOOOOOOO:', token['@lemma']
                        continue
                    lemmas.append(token['@lemma'])
            else:
                token = obj['sentences']['sentence']['token']
                if token['@tag'].startswith(('NP', 'NNP')):
                    #print 'ESTEEE NOOOOOOOOOO:', token['@lemma']
                    pass
                else:
                    lemmas.append(token['@lemma'])
    #print 'LEMMMAAAS', lemmas
    return lemmas

def extract_lemmas_sentences(analyzer, text):
    xml = analyzer.run(text)
    obj = xmltodict.parse(etree.tostring(xml))
    #print obj
    lemmas = []
    if obj['sentences']:
        if isinstance(obj['sentences']['sentence'], list):
            for sentence in obj['sentences']['sentence']:
                lemmas_in_sentence = []
                for token in sentence['token']:
                    lemmas_in_sentence.append(token['@lemma'])
                lemmas.append(lemmas_in_sentence)
        else:
            lemmas_in_sentence = []
            for token in obj['sentences']['sentence']['token']:
                lemmas_in_sentence.append(token['@lemma'])
            lemmas.append(lemmas_in_sentence)

    return lemmas
