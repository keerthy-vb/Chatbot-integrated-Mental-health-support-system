import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify,flash
from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask_session import Session
import hashlib
import base64
import traceback

from dotenv import load_dotenv
import re
# from werkzeug.security import generate_password_hash, check_password_hash
from hash_service import generate_password_hash, check_password_hash
from bson.objectid import ObjectId  # Ensure ObjectId conversion
from quiz import quiz_bp  # Importing quiz blueprint
from chatbot import chatbot_bp  # Importing chatbot blueprint
from selfcare import selfcare_bp  # Importing self-care blueprint
from appointments import appointments_bp
from therapists import therapists_bp
from flask_cors import CORS
import bcrypt
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  # ✅ Stores session in a file
Session(app)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
users_collection = db["users"]
quiz_collection = db["quiz_questions"]
quiz_results_collection = db["quiz_results"]
selfcare_collection = db["user_activities"] 
therapist_collection = db["therapists"]
 # Added self-care collection

# Register Blueprints
app.register_blueprint(quiz_bp, url_prefix="/quiz")
app.register_blueprint(chatbot_bp, url_prefix="/chatbot")

app.register_blueprint(selfcare_bp, url_prefix="/selfcare")
app.register_blueprint(appointments_bp)
app.register_blueprint(therapists_bp, url_prefix="/")









@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        name = data.get("name")
        role = data.get("role")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # Additional fields based on role
        age = data.get("age")
        gender = data.get("gender")
        interests = data.get("interests")
        specialization = data.get("specialization")
        qualification = data.get("qualification")
        experience = data.get("experience")
        patient_email = data.get("patient_email")

        # ✅ Validate required fields
        if not name or not role or not email or not password or not confirm_password:
            return jsonify({"success": False, "message": "All fields are required"}), 400

        # ✅ Check if passwords match
        if password != confirm_password:
            return jsonify({"success": False, "message": "Passwords do not match"}), 400

        # ✅ Strong password validation
        if len(password) < 6 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            return jsonify({"success": False, "message": "Password must be at least 6 characters long and contain both letters and numbers."}), 400

        # ✅ Check if email already exists
        if users_collection.find_one({"email": email}):
            return jsonify({"success": False, "message": "Email is already registered"}), 400

        # ✅ Hash the password before saving
        hashed_password = generate_password_hash(password)

        # ✅ Create user data
        user_data = {
            "name": name,
            "role": role,
            "email": email,
            "password": hashed_password,  # ✅ Save hashed password
        }

        # ✅ Handle role-specific fields
        if role == "Patient":
            if not age or not gender:
                return jsonify({"success": False, "message": "Age and Gender are required for Patients"}), 400
            user_data.update({
                "age": int(age),  # Convert age to integer
                "gender": gender,
                "interests": interests or []
            })
        elif role == "Therapist":
            if not specialization or not qualification or not experience:
                return jsonify({"success": False, "message": "Specialization, Qualification, and Experience are required for Therapists"}), 400
            user_data.update({
                "specialization": specialization,
                "qualification": qualification,
                "experience": int(experience)  # Convert experience to integer
            })
        elif role == "Caretaker":
            if not patient_email or not users_collection.find_one({"email": patient_email, "role": "Patient"}):
                return jsonify({"success": False, "message": "Invalid patient email"}), 400
            user_data.update({"patient_email": patient_email})

        # ✅ Insert into MongoDB
        users_collection.insert_one(user_data)

        return jsonify({"success": True, "message": "Account created successfully!"}), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/register", methods=["GET","POST"])
def register_page():
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    print("Form Data:", request.form)  # Debugging

    if request.method == "POST":
        email = request.json["email"]
        password = request.json["password"]

        user = users_collection.find_one({"email": email})
        print("User Found:", user)  # Debugging

        if user:
            print("Stored Hash:", user["password"])  # Debugging
            print("Entered Password:", password)  # Debugging
            print("Password Match:", check_password_hash(user["password"], password))  # Debugging

        # hashedpwd = generate_password_hash(password=password)
        if user and check_password_hash(user["password"], password):
            print("Login successful for:", user["name"])  # Debugging
            session["user"] = user 
            flash("Email and password are required!", "danger")  
            # return redirect(url_for("patient_dashboard"))
            return jsonify({"redirect": url_for("dashboard")}), 200  # JSON response for frontend

        flash("Invalid credentials. Try again!", "danger")
        # return redirect(url_for("login"))
        return jsonify({"redirect": url_for("login")}), 400

    return render_template("login.html")

    
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))  # Redirect if not logged in

    user = session["user"]  # Fetch user details from session
    user_role = user.get("role", "")  # Get user role safely

    # Redirect based on user role
    if user_role == "admin":
        return redirect(url_for("admin_dashboard"))
    elif user_role == "therapist":
        return redirect(url_for("therapist_dashboard"))
    elif user_role == "caretaker":
        return redirect(url_for("caretaker_dashboard"))
    elif user_role == "patient":
        return render_template("patient_dashboard", user=user)  # Render patient dashboard

    return redirect(url_for("login"))  # Redirect as fallback


@app.route("/admin_dashboard")
def admin_dashboard():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect(url_for("login"))  # Redirect if not an admin

    return render_template("admin_dashboard.html")

@app.route("/edit_user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})  # Fetch user from MongoDB
    if not user:
        return "User not found", 404

    if request.method == "POST":
        updated_name = request.form["name"]
        updated_email = request.form["email"]
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"name": updated_name, "email": updated_email}},
        )
        return redirect(url_for("manage_users"))

    return render_template("edit_user.html", user=user)

@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    users_collection.delete_one({"_id": ObjectId(user_id)})
    flash("User deleted successfully!", "success")
    return redirect(url_for('manage_users'))


@app.route("/manage_users")
def manage_users():
    users = users_collection.find()
    users = [{**user, "_id": str(user["_id"])} for user in users]  # Convert ObjectId to str
    return render_template("manage_users.html", users=users)


@app.route('/manage_quiz')
def manage_quiz():
    questions = list(quiz_collection.find())  # Convert cursor to list
    return render_template('manage_quiz.html', questions=questions)


# ✅ Add/Edit Quiz Route
@app.route('/edit_quiz/<question_id>', methods=['GET', 'POST'])
def edit_quiz(question_id):
    """Fetch and update quiz question."""
    question = quiz_collection.find_one({"_id": ObjectId(question_id)})

    if request.method == 'POST':
        try:
            question_text = request.form['question_text']  # Ensure the correct key
            option1 = request.form['option1']
            option2 = request.form['option2']
            option3 = request.form['option3']
            option4 = request.form['option4']
            category = request.form['category']

            updated_data = {
                "question_text": question_text,
                "options": [
                    {"text": option1},
                    {"text": option2},
                    {"text": option3},
                    {"text": option4}
                ],
                "category": category
            }

            # Update in MongoDB
            quiz_collection.update_one({"_id": ObjectId(question_id)}, {"$set": updated_data})
            flash("Question updated successfully!", "success")

            return redirect(url_for('manage_quiz'))  # Redirect after successful update
        except KeyError as e:
            flash(f"Error: Missing field - {str(e)}", "danger")
            return redirect(url_for('edit_quiz', question_id=question_id))

    return render_template('edit_quiz.html', question=question)


# ✅ Delete Quiz Route
@app.route('/delete_quiz/<question_id>')
def delete_quiz(question_id):
    quiz_collection.delete_one({"_id": ObjectId(question_id)})
    return redirect(url_for('manage_quiz'))

# ✅ Add Quiz Question Route
@app.route('/add_quiz', methods=['POST'])
def add_quiz():
    try:
        print("Form Data Received:", request.form.to_dict())  # Debugging print statement

        question_text = request.form.get('question_text')  # Ensure key matches HTML form
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        category = request.form.get('category')

        # Check if data is received correctly
        if not question_text or not option1 or not option2 or not option3 or not option4 or not category:
            return "Missing required fields", 400  # Bad request if any field is missing

        new_question = {
            "question_text": question_text,
            "options": [
                {"text": option1},
                {"text": option2},
                {"text": option3},
                {"text": option4}
            ],
            "category": category
        }

        quiz_collection.insert_one(new_question)  # Save to MongoDB
        return redirect(url_for('manage_quiz'))

    except Exception as e:
        return f"Error: {str(e)}", 500



@app.route('/manage_therapists')
def manage_therapists():
    therapists = therapist_collection.find()
    return render_template('manage_therapists.html', therapists=therapists)


@app.route('/add_therapist', methods=['POST'])
def add_therapist():
    """Add a new therapist."""
    name = request.form['name']
    specialization = request.form['specialization']
    qualifications = request.form['qualifications']
    contact = request.form['contact']

    therapist_data = {
        "name": name,
        "specialization": specialization,
        "qualifications": qualifications,
        "contact": contact,
        "verified": False
    }

    therapist_collection.insert_one(therapist_data)
    flash("Therapist added successfully!", "success")
    return redirect(url_for('manage_therapists'))

@app.route('/update_therapist/<therapist_id>', methods=['POST'])
def update_therapist(therapist_id):
    """Update therapist details."""
    name = request.form['name']
    specialization = request.form['specialization']
    qualifications = request.form['qualifications']
    contact = request.form['contact']

    therapist_collection.update_one(
        {"_id": ObjectId(therapist_id)},
        {"$set": {
            "name": name,
            "specialization": specialization,
            "qualifications": qualifications,
            "contact": contact
        }}
    )

    flash("Therapist details updated!", "success")
    return redirect(url_for('manage_therapists'))

@app.route('/delete_therapist/<therapist_id>', methods=['POST'])
def delete_therapist(therapist_id):
    """Delete therapist profile."""
    therapist_collection.delete_one({"_id": ObjectId(therapist_id)})
    flash("Therapist deleted!", "danger")
    return redirect(url_for('manage_therapists'))

@app.route('/verify_therapist/<therapist_id>')
def verify_therapist(therapist_id):
    """Verify therapist profile."""
    therapist_collection.update_one(
        {"_id": ObjectId(therapist_id)},
        {"$set": {"verified": True}}
    )
    flash("Therapist verified!", "success")
    return redirect(url_for('manage_therapists'))





@app.route("/therapist_dashboard")
def therapist_dashboard():
    return render_template("therapist_dashboard.html", user=session["user"])

@app.route("/caretaker_dashboard")
def caretaker_dashboard():
    return render_template("caretaker_dashboard.html", user=session["user"])

@app.route("/patient_dashboard")
def patient_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user = users_collection.find_one({"_id": ObjectId(session["user_id"])})

    return render_template("dashboard.html", user=user["name"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# Function to calculate quiz result
def calculate_result(selected_answers):
    category_scores = {"Anxiety": 0, "Depression": 0, "Stress": 0, "Normal": 0}
    
    for answer in selected_answers:
        category, score = answer.split(":")
        category_scores[category] += int(score)
    
    return max(category_scores, key=category_scores.get)

@app.route("/quiz_page")
def quiz_page():
    if "user" not in session:
        return redirect(url_for("login"))
    
    questions = list(quiz_collection.find({}, {"_id": 0}))
    return render_template("quiz.html", questions=questions)

@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    # ✅ Ensure user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    data = request.json  # ✅ Get JSON data (not form data)
    if not data or "answers" not in data:
        return jsonify({"error": "Invalid request data"}), 400

    # ✅ Initialize category scores
    category_scores = {"Anxiety": 0, "Depression": 0, "Stress": 0, "Normal": 0}

    questions = list(db.quiz_questions.find())  # ✅ Fetch all questions

    if len(data["answers"]) != len(questions):
        return jsonify({"error": "Please answer all questions!"}), 400

    # ✅ Process answers
    for i, question in enumerate(questions):
        try:
            category, score = question["options"][data["answers"][i]].split(":")
            category_scores[category] += int(score.strip())
        except (ValueError, IndexError, KeyError):
            return jsonify({"error": f"Invalid answer format for question {i + 1}"}), 400

    # ✅ Determine result category
    result_category = max(category_scores, key=category_scores.get)

    # ✅ Store result in database
    quiz_results_collection.insert_one({
        "user_id": ObjectId(session["user_id"]),  
        "name": session["user"],
        "quiz_result": result_category
    })

    return render_template("quiz_result.html", result=result_category)

@app.route("/check_session")
def check_session():
    return jsonify({"user_id": session.get("user_id")})



@app.route("/get_results", methods=["GET"])
def get_results():
    results = list(quiz_results_collection.find({}, {"_id": 0}))
    return jsonify(results)

# Chatbot Page
@app.route("/chatbot_page")
def chatbot_page():
    if "user" not in session:
        return redirect(url_for("login"))
    
    return render_template("chatbot.html")

# Self-care Page
@app.route("/selfcare_page")
def selfcare_page():
    if "user" not in session:
        return redirect(url_for("login"))
    
    user_activities = selfcare_collection.find_one({"user_id": ObjectId(session.get("user_id"))})
    
    return render_template("selfcare.html", user_data=user_activities)

if __name__ == "__main__":
    app.run(debug=True)
