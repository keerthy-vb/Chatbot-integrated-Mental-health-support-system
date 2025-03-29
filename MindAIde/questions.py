from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Change if using a different host
db = client["mental_health_db"]  # Your database name
collection = db["quiz_questions"]  # Your collection name

# Sample questions to insert
questions = [
    {
        "question_text": "How often do you feel overwhelmed with responsibilities?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Stress"
    },
    {
        "question_text": "Do you struggle to concentrate on tasks?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Stress"
    },
    {
        "question_text": "Do you feel anxious about social situations?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Anxiety"
    },
    {
        "question_text": "Do you experience frequent mood swings?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Depression"
    },
    {
        "question_text": "Do you have difficulty sleeping or experience restless sleep?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Stress"
    },
    {
        "question_text": "How often do you feel nervous or anxious?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Anxiety"
    },
    {
        "question_text": "Do you experience sudden panic attacks or intense fear?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Anxiety"
    },
    {
        "question_text": "Do you feel sad or hopeless most of the time?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Depression"
    },
    {
        "question_text": "Do you avoid social interactions due to fear or nervousness?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Anxiety"
    },
    {
        "question_text": "Do you feel constantly fatigued even after a full night’s rest?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Depression"
    },
    {
        "question_text": "Do you feel irritated or frustrated over minor issues?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Stress"
    },
    {
        "question_text": "Have you lost interest in activities you previously enjoyed?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Depression"
    },
    {
        "question_text": "Do you experience excessive worrying even over small things?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Anxiety"
    },
    {
        "question_text": "Do you have physical symptoms like headaches or stomachaches due to stress?",
        "options": [
            {"text": "Never", "score": 0},
            {"text": "Sometimes", "score": 1},
            {"text": "Often", "score": 2},
            {"text": "Always", "score": 3}
        ],
        "category": "Stress"
    },
    {
        "question_text": "Do you feel mentally stable and able to handle life’s challenges?",
        "options": [
            {"text": "Never", "score": 3},
            {"text": "Sometimes", "score": 2},
            {"text": "Often", "score": 1},
            {"text": "Always", "score": 0}
        ],
        "category": "Normal"
    }
]

# Insert the questions into the collection
collection.insert_many(questions)

print("Questions inserted successfully! ✅")
