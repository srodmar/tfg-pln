## Requirements
- Google API (https://developers.google.com/api-client-library/python/start/installation)
- langdetect (https://pypi.python.org/pypi/langdetect)
- Freeling 4.0 (http://nlp.lsi.upc.edu/freeling/node/1)
- pyfreeling (https://github.com/malev/pyfreeling)
- NLTK (http://www.nltk.org/install.html)
- pymongo (https://api.mongodb.com/python/current/) Only if you want to store the results

## Running the tool
To run the tool just type 'python pipeline.py'

The first thing the tool does is ask for a GMail account and password in order to retrieve mails from it. 
You can avoid this if you comment the method call 'collect_mails()' from pipeline.py, but you will have to place the text files to process in the following directory: 'storage/body_texts'.
