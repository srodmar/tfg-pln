import xmltodict
import pprint

from lxml import etree
pp = pprint.PrettyPrinter(indent=4)

def extract_lemmas(analyzer, text):
    xml = analyzer.run(text)
    print xml
    obj = xmltodict.parse(etree.tostring(xml))
    lemmas = []
    if obj['sentences']:
        if isinstance(obj['sentences']['sentence'], list):
            for sentence in obj['sentences']['sentence']:
                if isinstance(sentence['token'], list):
                    for token in sentence['token']:
                        if token['@tag'].startswith(('NP', 'NNP')):
                            continue
                        lemmas.append(token['@lemma'])
                else:
                    token = sentence['token']
                    if token['@tag'].startswith(('NP', 'NNP')):
                        continue
                    lemmas.append(token['@lemma'])
        else:
            if isinstance(obj['sentences']['sentence']['token'], list):
                for token in obj['sentences']['sentence']['token']:
                    if token['@tag'].startswith(('NP', 'NNP')):
                        continue
                    lemmas.append(token['@lemma'])
            else:
                token = obj['sentences']['sentence']['token']
                if token['@tag'].startswith(('NP', 'NNP')):
                    pass
                else:
                    lemmas.append(token['@lemma'])
    return lemmas

def extract_lemmas_sentences(analyzer, text):
    xml = analyzer.run(text)
    obj = xmltodict.parse(etree.tostring(xml))
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
