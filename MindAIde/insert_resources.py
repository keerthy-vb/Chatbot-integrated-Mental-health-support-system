from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]  # Your database name
selfcare_collection = db["selfcare_resources"]  # Collection for self-care resources

# Self-care resources data
resources_data = [
    {
        "category": "Anxiety",
        "resources": {
            "activities": ["Meditation", "Breathing exercises", "Journaling", "Listening to calm music", "Taking a nature walk"],
            "exercises": ["Yoga", "Stretching", "Progressive muscle relaxation", "Tai Chi"],
            "youtube_videos": [
                {"title": "Guided Meditation for Anxiety", "url": "https://youtu.be/inspired_video1"},
                {"title": "Breathing Exercises to Reduce Anxiety", "url": "https://youtu.be/inspired_video2"}
            ],
            "articles": [
                {"title": "How to Manage Anxiety Effectively", "url": "https://example.com/article_anxiety1"},
                {"title": "Top 10 Ways to Reduce Anxiety Naturally", "url": "https://example.com/article_anxiety2"}
            ],
            "books": [
                {"title": "The Anxiety and Phobia Workbook", "url": "https://example.com/book_anxiety1"},
                {"title": "Dare: The New Way to End Anxiety", "url": "https://example.com/book_anxiety2"}
            ]
        }
    },
    {
        "category": "Depression",
        "resources": {
            "activities": ["Talking to a friend", "Painting or drawing", "Listening to uplifting music", "Cooking a new recipe"],
            "exercises": ["Walking", "Aerobic exercises", "Dancing", "Cycling"],
            "youtube_videos": [
                {"title": "How to Overcome Depression", "url": "https://youtu.be/inspired_video3"},
                {"title": "Daily Routine to Improve Mood", "url": "https://youtu.be/inspired_video4"}
            ],
            "articles": [
                {"title": "Understanding Depression: Symptoms & Solutions", "url": "https://example.com/article_depression1"},
                {"title": "10 Tips to Boost Your Mood", "url": "https://example.com/article_depression2"}
            ],
            "books": [
                {"title": "Feeling Good: The New Mood Therapy", "url": "https://example.com/book_depression1"},
                {"title": "The Noonday Demon: An Atlas of Depression", "url": "https://example.com/book_depression2"}
            ]
        }
    },
    {
        "category": "Stress",
        "resources": {
            "activities": ["Deep breathing", "Listening to nature sounds", "Practicing gratitude", "Reading a book"],
            "exercises": ["Stretching", "Running", "Tai Chi", "Swimming"],
            "youtube_videos": [
                {"title": "Quick Stress Relief Techniques", "url": "https://youtu.be/inspired_video5"},
                {"title": "How to Stay Calm Under Pressure", "url": "https://youtu.be/inspired_video6"}
            ],
            "articles": [
                {"title": "How to Manage Stress in Everyday Life", "url": "https://example.com/article_stress1"},
                {"title": "Effective Strategies for Coping with Stress", "url": "https://example.com/article_stress2"}
            ],
            "books": [
                {"title": "Why Zebras Don’t Get Ulcers", "url": "https://example.com/book_stress1"},
                {"title": "The Stress-Proof Brain", "url": "https://example.com/book_stress2"}
            ]
        }
    }
]

# Insert data into MongoDB
selfcare_collection.delete_many({})  # Clear existing data to avoid duplicates
selfcare_collection.insert_many(resources_data)

print("✅ Resources inserted successfully into MongoDB!")
