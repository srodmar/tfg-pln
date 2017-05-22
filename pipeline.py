# encoding: utf-8
from gmail import main
from lang_detect import detect_all

# Se lanza la recogida de correos electrónicos
main()

# Se analizan los correos y se muestran los idiomas detectados
print detect_all()

# Detectar idioma correo -> lanzar Stanford para ese idioma -> Procesar con StanfordCoreNLP
# Problema: hay que cerrar y volver a lanzar Stanford con cada cambio de idioma
