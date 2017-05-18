from pycorenlp import StanfordCoreNLP
import pprint

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    nlp = StanfordCoreNLP('http://localhost:9000')
    text = (
        'Pusheen and Smitha walked along the beach. Pusheen wanted to surf,'
        'but fell off the surfboard.')
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse,sentiment',
        'outputFormat': 'json'
    })
    #print(output)
    print(output['sentences'][0]['parse'])
    if 'sentiment' in output:
        print(output['sentiment'])
    output = nlp.tokensregex(text, pattern='/Pusheen|Smitha/', filter=False)
    pp.pprint(output)
    output = nlp.semgrex(text, pattern='{tag: VBD}', filter=False)
    pp.pprint(output)
