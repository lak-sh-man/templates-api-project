from flask_pymongo import PyMongo

def init_db(app):
    try:
        mongodb_client = PyMongo(app)
        db_instance = mongodb_client.db  # Get the database instance
        
        if db_instance is None:
            print("❌ MongoDB connection failed: Database instance is None")
        else:
            print("✅ MongoDB connected successfully!")

        return db_instance  # Ensure this returns the database

    except Exception as e:
        print(f"⚠️ Exception during MongoDB connection: {e}")
        return None
 

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