pp = pprint.PrettyPrinter(indent=4)
# lista de idiomas que soporta StanfordCoreNLP
idiomas = {'ar': 'arabic', 'zh': 'chinese',
           'fr': 'french', 'de': 'german', 'es': 'spanish'}
store_dir = 'storage/body_texts/classified'
port = 9000
current_dir = os.getcwd()
processes = []


def call(command):
    args = shlex.split(command)
    return subprocess.Popen(args)


def kill(p):
    if isinstance(p, list):
        for proc in p:
            proc.terminate()
    else:
        p.terminate()


server_ports = {}
for dir in os.listdir(store_dir):
    os.chdir('stanford-corenlp-full-2016-10-31')
    if dir in idiomas:
        command = 'java -Xmx2048m -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -serverProperties StanfordCoreNLP-' + \
            idiomas[dir] + '.properties -port ' + \
            str(port) + ' -timeout 15000'
        p = call(command)
        server_ports[dir] = port
        port += 1
    elif dir == 'en':
        command = 'java -mx2048m -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port ' + \
            str(port) + ' -timeout 15000'
        p = call(command)
        server_ports[dir] = port
        port += 1
    else:
        p = None

    os.chdir(current_dir)
    time.sleep(15)

#for lan in server_ports:
    if p:
        print('Lanzo peticiones al servidor en el puerto: ' + str(server_ports[dir]))
        nlp = StanfordCoreNLP('http://localhost:' + str(server_ports[dir]))
        #text = ('Hola, mi nombre es Manolo y esta es la historia de mi vida')
        texts_dir = store_dir + '/' + dir
        for file in os.listdir(texts_dir):
            with open(texts_dir + '/' + file, 'r') as current_file:
                text = current_file.read()
            print('READ FILE: ' + file + ' Tipo: ' + str(type(text)))
            text = text.decode('utf-8')
            text = text.encode('utf-8')
            output = nlp.annotate(text, properties={
                'annotators': 'tokenize,ssplit,pos,depparse,parse',
                'outputFormat': 'json'
            })
            pp.pprint(output)
        #print(output['sentences'][0]['parse'])
        print('A MATAR')
        kill(p)
