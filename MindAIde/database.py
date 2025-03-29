#for selfcare activity module
from pymongo import MongoClient

def get_db():
    """Connect to MongoDB and return the database."""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["mental_health_db"]
    return db
