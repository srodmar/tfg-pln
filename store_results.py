from pymongo import MongoClient
import logging

logging.basicConfig(filename="mongo.log", filemode='w', level=logging.DEBUG)

client = MongoClient('10.6.128.9', 8081)
client.emails.authenticate('emailUser', 'emailcito99', mechanism='SCRAM-SHA-1')

db = client.emails

post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"]}

email = db.email

post_id = email.insert_one(post).inserted_id

print post_id
