import xmltodict
import pprint
import pdb

from pyfreeling import Analyzer
from lxml import etree

pp = pprint.PrettyPrinter(indent=4)

analyzer = Analyzer(config='en.cfg')
xml = analyzer.run('Hello World, This is me.', 'noflush')
print(etree.tostring(xml))
obj = xmltodict.parse(etree.tostring(xml))

#pp.pprint(obj['sentences']['sentence'])
#pdb.set_trace()

if isinstance(obj['sentences']['sentence'], list):
    for sentence in obj['sentences']['sentence']:
        for token in sentence['token']:
            print token['@lemma']
else:
    for token in obj['sentences']['sentence']['token']:
        print token['@lemma']

'''analyzer = Analyzer(config='es.cfg', lang='es')

output = analyzer.run('Hola mundo', 'noflush')
print(etree.tostring(output))'''
