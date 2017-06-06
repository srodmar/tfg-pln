import xmltodict
import pprint

#from pyfreeling import Analyzer
from lxml import etree

'''
pp = pprint.PrettyPrinter(indent=4)

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
                for token in sentence['token']:
                    lemmas.append(token['@lemma'])
        else:
            for token in obj['sentences']['sentence']['token']:
                lemmas.append(token['@lemma'])

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
