from langdetect import detect, detect_langs

l = detect("War doesn't show who's right, just who's left.")
print(l)

cont = 1
while cont <= 100:
    file = 'inmail.' + str(cont)
    with open(file, 'r') as myfile:
        data=myfile.read().replace('\n', '')
    cont = cont + 1
