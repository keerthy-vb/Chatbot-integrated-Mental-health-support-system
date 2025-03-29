from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]

# Insert sample therapist
db.therapists.insert_one({
    "name": "Dr. Jane Smith",
    "specialization": "Clinical Psychologist",
    "qualifications": "PhD in Clinical Psychology",
    "contact": "jane.smith@email.com",
    "verified": True
})

print("Sample therapist added!")
