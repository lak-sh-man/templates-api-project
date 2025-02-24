from flask_pymongo import PyMongo

def init_db(app):
    mongodb_client = PyMongo(app)
    return mongodb_client.db  

# STRUCTURE

## users collection
"""
[
    {
        "_id": "lakshman1122000@gmail.com",
        "first_name": "lakshman",
        "last_name": "N",
        "password": "123"
    },
    {
        "_id": "sriram1122000@gmail.com",
        "first_name": "sriram",
        "last_name": "N",
        "password": "123"
    }
]
"""

## templates collection
"""
[
    {
        "_id": "lakshman1122000@gmail.com",
        "templates": {
            "90231c15875f433ab6aa0ba57d0bc127": {
                "template_name": "Welcome Gmail",
                "subject": "Welcome to Our Service!",
                "body": "Thank you for signing up!"
            },
            "a9f2e04d85bf4bc6b38d8f8c9c8a1283": {
                "template_name": "Promo Offer",
                "subject": "Exclusive Discount for You!",
                "body": "Get 20% off on your next purchase."
            }
        }
    },
    {
        "_id": "sriram1122000@gmail.com",
        "templates": {
            "b3a7c2d5e81241f28b9d59eb67b3f782": {
                "template_name": "New User Welcome",
                "subject": "Hi Sriram, Welcome!",
                "body": "Glad to have you!"
            }
        }
    }
]
"""