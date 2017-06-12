from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import logging

#logging.basicConfig(filename="mongo.log", filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = MongoClient('10.6.128.9', 8081)
client.email.authenticate('emailUser', '', mechanism='SCRAM-SHA-1')


db = client.email
emails = db.emails
'''
post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"]}



post_id = emails.insert_one(post).inserted_id
logger.info("Added object with id: %s to database.", post_id)

print post_id
'''


def insert_email(mail_id, mail_text, mail_topic):
    email = {"mail_id": mail_id,
             "text": mail_text,
             "topic": mail_topic}

    try:
        email_id = emails.insert_one(email).inserted_id
        logger.info("Added object with id: %s to database.", email_id)
    except DuplicateKeyError:
        emails.update_one({
            'mail_id': mail_id
        }, {
            '$set': {
                'text': mail_text,
                'topic': mail_topic
            }
        }, upsert=False)
