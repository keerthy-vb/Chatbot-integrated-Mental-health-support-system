from mongoengine import connect

connect('mental_health_db', host='127.0.0.1', port=27017)

print("Connected to MongoDB successfully!")
