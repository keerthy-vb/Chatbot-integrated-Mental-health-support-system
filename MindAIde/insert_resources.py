from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
resources_collection = db["selfcare_resources"]

selfcare_resources = [
    {
        "category": "Stress",
        "Activities": ["Meditation", "Breathing Exercises", "Listening to Music", "Yoga"],
        "YouTube": [
            {"title": "5-Minute Stress Relief Meditation", "url": "https://youtu.be/O-6f5wQXSu8"},
            {"title": "Calming Music for Relaxation", "url": "https://youtu.be/2OEL4P1Rz04"}
        ],
        "Books": [
            {"title": "The Stress-Proof Brain", "url": "https://www.medicalnewstoday.com/articles/145855"},
            {"title": "10% Happier", "url": "https://www.amazon.com/dp/0062917598"}
        ],
        "Websites": [
            {"title": "Headspace (Meditation)", "url": "https://www.headspace.com/"},
            {"title": "Calm (Stress Management)", "url": "https://www.calm.com/"}
        ]
    },
    {
        "category": "Depression",
        "Activities": ["Journaling", "Exercise", "Talking to a Friend", "Outdoor Walk"],
        "YouTube": [
            {"title": "How to Overcome Depression", "url": "https://www.youtube.com/watch?v=d96akWDnx0w"},
            {"title": "Self-Help Techniques for Depression", "url": "https://youtu.be/0h-EvCVNr9I"}
        ],
        "Books": [
            {"title": "Feeling Good: The New Mood Therapy", "url": "https://www.amazon.com/dp/0380810336"},
            {"title": "Lost Connections", "url": "https://www.amazon.com/dp/163286830X"}
        ],
        "Websites": [
            {"title": "BetterHelp (Therapy)", "url": "https://www.betterhelp.com/"},
            {"title": "Mind (Mental Health Support)", "url": "https://www.mind.org.uk/"}
        ]
    },
    {
        "category": "Anxiety",
        "Activities": ["Deep Breathing", "Grounding Techniques", "Reading", "Listening to Calm Music"],
        "YouTube": [
            {"title": "Breathing Techniques for Anxiety", "url": "https://youtu.be/YiHrxB_N8i8"},
            {"title": "How to Reduce Anxiety", "url": "https://youtu.be/FWfSgYV4z3A"}
        ],
        "Books": [
            {"title": "The Anxiety and Phobia Workbook", "url": "https://www.amazon.com/dp/1626252157"},
            {"title": "Dare: The New Way to End Anxiety", "url": "https://www.amazon.com/dp/0956596258"}
        ],
        "Websites": [
            {"title": "Anxiety Canada", "url": "https://www.anxietycanada.com/"},
            {"title": "No Panic (Support for Anxiety)", "url": "https://www.nopanic.org.uk/"}
        ]
    },
    {
        "category": "Normal",
        "Activities": ["Healthy Diet", "Regular Exercise", "Engaging in Hobbies", "Good Sleep Schedule"],
        "YouTube": [
            {"title": "Daily Habits for Mental Wellness", "url": "https://youtu.be/kXkG4ZpDuBU"},
            {"title": "How to Build Healthy Routines", "url": "https://youtu.be/Im9kVpP6EsA"}
        ],
        "Books": [
            {"title": "Atomic Habits", "url": "https://www.amazon.com/dp/0735211299"},
            {"title": "The 5 AM Club", "url": "https://www.amazon.com/dp/1443456624"}
        ],
        "Websites": [
            {"title": "Verywell Mind", "url": "https://www.verywellmind.com/"},
            {"title": "Psychology Today", "url": "https://www.psychologytoday.com/"}
        ]
    }
]

# Insert into MongoDB
resources_collection.insert_many(selfcare_resources)
print("✅ Self-care resources added to MongoDB successfully!")
