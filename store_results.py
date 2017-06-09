from pymongo import MongoClient
import logging

logging.basicConfig(filename="mongo.log", filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = MongoClient('10.6.128.9', 8081)
client.email.authenticate('emailUser', '', mechanism='SCRAM-SHA-1')

'''
db = client.email

post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"]}

emails = db.emails

post_id = emails.insert_one(post).inserted_id
logger.info("Added object with id: %s to database.", post_id)

print post_id
'''

def insert_email():
    next
