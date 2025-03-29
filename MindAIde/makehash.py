from werkzeug.security import generate_password_hash
from pymongo import MongoClient

# ✅ Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
users_collection = db["users"]

# ✅ Update all users to use hashed passwords
for user in users_collection.find():
    plain_password = user["password"]  # Get the current plain text password
    hashed_password = generate_password_hash(plain_password)  # Hash it

    # ✅ Update the password in MongoDB
    users_collection.update_one({"_id": user["_id"]}, {"$set": {"password": hashed_password}})

print("✅ All passwords have been securely hashed!")
