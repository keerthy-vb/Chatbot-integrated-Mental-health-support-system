from flask import Blueprint, render_template, request, session, redirect, url_for
from pymongo import MongoClient

quiz_bp = Blueprint("quiz", __name__, template_folder="templates")

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
quiz_collection = db["quiz_questions"]

def get_quiz_questions():
    """Fetch quiz questions from MongoDB"""
    questions = list(quiz_collection.find({}, {"_id": 0}))  
    return questions

def process_quiz_results(user_answers):
    """Calculate total scores and determine the category"""
    scores = {"Stress": 0, "Depression": 0, "Anxiety": 0, "Normal": 0}

    for question in get_quiz_questions():
        question_text = question["question_text"]  # Unique identifier for answers
        category = question["category"]

        # Extract the score from the user's selected answer
        selected_value = user_answers.get(f'answers_{question_text}')
        if selected_value:  
            _, score = selected_value.split(":")  # Extracting category and score
            scores[category] += int(score)  # Add score to respective category

    # Find the category with the highest score
    final_category = max(scores, key=scores.get)  
    session["quiz_result"] = final_category  # Store in session
    return final_category

@quiz_bp.route("/", methods=["GET", "POST"])
def quiz_page():
    """Render quiz page with fetched questions"""
    if request.method == "GET":
        questions = get_quiz_questions()
        return render_template("quiz.html", questions=questions)

    elif request.method == "POST":
        user_answers = request.form
        result = process_quiz_results(user_answers)
        return redirect(url_for("quiz.quiz_result_page"))

@quiz_bp.route("/result")
def quiz_result_page():
    """Display quiz results"""
    result = session.get("quiz_result", "Unknown")
    return render_template("quiz_result.html", result=result)
