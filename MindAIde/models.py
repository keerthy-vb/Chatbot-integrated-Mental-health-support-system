from mongoengine import Document, StringField, IntField, connect

# Connect to MongoDB
connect('mental_health_db')

# Define a User model (MongoDB collection)
class User(Document):
    name = StringField(required=True)
    age = IntField(required=True)
