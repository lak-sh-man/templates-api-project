from flask_pymongo import PyMongo

def init_db(app):
    mongodb_client = PyMongo(app)
    return mongodb_client.db  
