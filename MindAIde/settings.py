INSTALLED_APPS = [
    "users",
    "quiz",
    "chatbot",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

from flask import Blueprint, render_template, request
from pymongo import MongoClient

quiz_bp = Blueprint("quiz", __name__, template_folder="templates")

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
quiz_collection = db["quiz_questions"]

def categorize_score(score):
    """Classify user based on quiz score"""
    if score >= 40:
        return "Depression"
    elif score >= 30:
        return "Anxiety"
    elif score >= 20:
        return "Stress"
    else:
        return "Normal"

@quiz_bp.route("/", methods=["GET"])
def quiz_page():
    questions = list(quiz_collection.find({}, {"_id": 0}))  # Fetch questions without MongoDB ObjectId
    return render_template("quiz.html", questions=questions)

@quiz_bp.route("/result", methods=["POST"])
def quiz_result_page():
    questions = list(quiz_collection.find({}, {"_id": 0}))
    total_score = sum(int(request.form.get(f'q{q["id"]}', 0)) for q in questions)
    category = categorize_score(total_score)
    return render_template("quiz_result.html", score=total_score, category=category)

