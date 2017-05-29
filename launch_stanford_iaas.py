pp = pprint.PrettyPrinter(indent=4)
# lista de idiomas que soporta StanfordCoreNLP
idiomas = {'ar': 'arabic', 'zh': 'chinese',
           'fr': 'french', 'de': 'german', 'es': 'spanish'}
store_dir = 'storage/body_texts/classified'
port = 8081

server_ports = {}
for dir in os.listdir(store_dir):
    if dir in idiomas:
        launch_corenlp(idiomas[dir], str(port))
        server_ports[dir] = port
        port += 1
    elif dir == 'en':
        launch_corenlp(None, str(port))
        server_ports[dir] = port
        port += 1

for lang in server_ports:
    print('Lanzo peticiones al servidor ' + lang + ', en el puerto: ' + str(server_ports[lang]))
    nlp = StanfordCoreNLP('http://alu0100699968.iaas.ull.es:8082')# + str(server_ports[lang]))
    text = ('The quick brown fox jumped over the lazy dog of John.')
    texts_dir = store_dir + '/' + lang
    for file in os.listdir(texts_dir):
        #with open(texts_dir + '/' + file, 'r') as current_file:
        #    text = current_file.read()
        print('READ FILE: ' + file + ' Tipo: ' + str(type(text)))
        #text = text.decode('utf-8')
        #text = text.encode('utf-8')
        output = nlp.annotate(text, properties={
            'annotators': 'tokenize,ssplit,pos,ner',
            'outputFormat': 'json'
        })
        pp.pprint(output)
