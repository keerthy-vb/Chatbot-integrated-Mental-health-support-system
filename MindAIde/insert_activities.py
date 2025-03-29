from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
activities_collection = db["selfcare_suggestions"]

# Clear existing data (optional, to avoid duplicate entries)
activities_collection.delete_many({})

# Data to insert
selfcare_data = [
    {
        "category": "Anxiety",
        "type": "Activity",
        "title": "Deep Breathing Exercises",
        "description": "Practice deep breathing techniques to calm your mind.",
    },
    {
        "category": "Anxiety",
        "type": "Exercise",
        "title": "Yoga for Relaxation",
        "description": "Perform simple yoga poses to reduce anxiety.",
    },
    {
        "category": "Anxiety",
        "type": "YouTube",
        "title": "Guided Meditation for Anxiety",
        "link": "https://www.youtube.com/watch?v=O-6f5wQXSu8",
    },
    {
        "category": "Anxiety",
        "type": "Article",
        "title": "Managing Anxiety: A Guide",
        "link": "https://www.helpguide.org/articles/anxiety/managing-anxiety.htm",
    },
    {
        "category": "Depression",
        "type": "Activity",
        "title": "Journaling",
        "description": "Write about your thoughts and feelings to process emotions.",
    },
    {
        "category": "Depression",
        "type": "Exercise",
        "title": "Morning Walk",
        "description": "Take a 15-minute walk outside to boost mood.",
    },
    {
        "category": "Depression",
        "type": "YouTube",
        "title": "Overcoming Depression: A Motivational Talk",
        "link": "https://www.youtube.com/watch?v=xoYnqvadurg",
    },
    {
        "category": "Depression",
        "type": "Article",
        "title": "Understanding Depression",
        "link": "https://www.psycom.net/depression-definition",
    },
    {
        "category": "Stress",
        "type": "Activity",
        "title": "Listen to Relaxing Music",
        "description": "Put on calming music to reduce stress levels.",
    },
    {
        "category": "Stress",
        "type": "Exercise",
        "title": "Stretching Exercises",
        "description": "Perform simple stretches to relieve muscle tension.",
    },
    {
        "category": "Stress",
        "type": "YouTube",
        "title": "Stress Management Tips",
        "link": "https://www.youtube.com/watch?v=I6402QJp52M",
    },
    {
        "category": "Stress",
        "type": "Article",
        "title": "How to Cope with Stress",
        "link": "https://www.medicalnewstoday.com/articles/145855",
    },
    {
        "category": "Normal",
        "type": "Activity",
        "title": "Spend Time with Family",
        "description": "Engage in activities with loved ones for emotional well-being.",
    },
    {
        "category": "Normal",
        "type": "Exercise",
        "title": "Basic Home Workout",
        "description": "Do a simple home workout routine for overall health.",
    },
    {
        "category": "Normal",
        "type": "YouTube",
        "title": "Daily Healthy Habits",
        "link": "https://www.youtube.com/watch?v=3OGv4Hft7R4",
    },
    {
        "category": "Normal",
        "type": "Article",
        "title": "Healthy Lifestyle Tips",
        "link": "https://www.healthline.com/health/healthy-living",
    },
]

# Insert into the collection
activities_collection.insert_many(selfcare_data)

print("Self-care suggestions inserted successfully!")
