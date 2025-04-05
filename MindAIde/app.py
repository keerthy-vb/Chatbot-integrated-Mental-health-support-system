import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify,flash
from pymongo import MongoClient
#from flask_pymongo import PyMongo
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
#import bcrypt
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False 
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  # ✅ Stores session in a file
Session(app)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]

app.config['DB'] = db

users_collection = db["users"]
quiz_collection = db["quiz_questions"]
quiz_results_collection = db["quiz_results"]
selfcare_collection = db["selfcare_resources"] 
#therapist_collection = db["therapists"]
todos_collection = db["todos"]
notifications_collection = db["notifications"]
appointments_collection = db["appointments"]



 # Added self-care collection

# Register Blueprints
app.register_blueprint(quiz_bp, url_prefix="/quiz")
app.register_blueprint(chatbot_bp, url_prefix="/chatbot")

app.register_blueprint(selfcare_bp, url_prefix="/selfcare")
app.register_blueprint(appointments_bp, url_prefix='/appointments')
#app.register_blueprint(therapists_bp, url_prefix="/")



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
        contact = data.get("contact")

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
            if not specialization or not qualification or not experience or not contact:
                return jsonify({"success": False, "message": "Specialization, Qualification, Experience, and Contact are required for Therapists"}), 400
            
            # Optional: Validate phone number format
            if not re.fullmatch(r"\d{10}", contact):
                return jsonify({"success": False, "message": "Contact must be a valid 10-digit number"}), 400

            user_data.update({
                "specialization": specialization,
                "qualification": qualification,
                "experience": int(experience),
                "contact": contact,
                "verified": False
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
        email = request.json.get("email")
        password = request.json.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required!"}), 400

        user = users_collection.find_one({"email": email})
        print("User Found:", user)  # Debugging

        if user:
            print("Stored Hash:", user["password"])  # Debugging
            print("Entered Password:", password)  # Debugging
            print("Password Match:", check_password_hash(user["password"], password))  # Debugging

        if user and check_password_hash(user["password"], password):
            print("Login successful for:", user["name"])
            session["user"] = user
            session["_id"] = user["_id"]
            session["user_id"] = str(user["_id"])
            return jsonify({"redirect": url_for("dashboard")}), 200
        else:
            return jsonify({"error": "Invalid credentials. Try again!"}), 400

    return render_template("login.html")


    
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))  # Redirect if not logged in

    user = session["user"]  # Fetch user details from session
    user_role = user.get("role", "")  # Get user role safely
    user_role = user_role.lower()
    # Redirect based on user role
    if user_role == "admin":
        return redirect(url_for("admin_dashboard"))
    elif user_role == "therapist":
        return redirect(url_for("therapist_dashboard"))
    elif user_role == "caretaker":
        return redirect(url_for("caretaker_dashboard"))
    elif user_role == "patient":
        return redirect(url_for("patient_dashboard"))
        # return render_template("patient_dashboard")  # Render patient dashboard

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
    

# @app.route('/therapist_suggestions')
# def therapist_suggestions():
#     verified_therapists = list(users_collection.find({
#         "role": "therapist",
#         "verified": True
#     }))
#     return render_template("therapist_suggestions.html", therapists=verified_therapists)


@app.route('/request_appointment/<therapist_id>', methods=['POST'])
def request_appointment(therapist_id):
    patient_id = session.get("user_id")
    if not patient_id:
        flash("Please log in first!", "danger")
        return redirect(url_for("login"))

    appointment = {
        "patient_id": patient_id,
        "therapist_id": therapist_id,
        "status": "Pending"
    }

    db.appointments.insert_one(appointment)
    flash("Appointment request sent!", "success")
    return redirect(url_for("therapist_suggestions"))






# @app.route('/manage_therapists')
# def manage_therapists():
#     # Fetch all therapists from MongoDB
#     therapists = list(therapist_collection.find())

#     # Ensure 'verified' field exists in all records
#     for t in therapists:
#         if 'verified' not in t:
#             t['verified'] = False  # Default to False for pending therapists

#     return render_template('manage_therapists.html', therapists=therapists)


# @app.route('/manage_therapists')
# def manage_therapists():
#     verified_therapists = list(therapist_collection.find({"verified": True}))
#     unverified_therapists = list(therapist_collection.find({"verified": False}))

#     return render_template('manage_therapists.html', 
#                            verified_therapists=verified_therapists, 
#                            unverified_therapists=unverified_therapists)



# @app.route('/add_therapist', methods=['POST'])
# def add_therapist():
#     """Add a new therapist."""
#     name = request.form['name']
#     specialization = request.form['specialization']
#     qualifications = request.form['qualifications']
#     contact = request.form['contact']

#     therapist_data = {
#         "name": name,
#         "specialization": specialization,
#         "qualifications": qualifications,
#         "contact": contact,
#         "verified": False
#     }

#     therapist_collection.insert_one(therapist_data)
#     flash("Therapist added successfully!", "success")
#     return redirect(url_for('manage_therapists'))

# @app.route('/update_therapist/<therapist_id>', methods=['POST'])
# def update_therapist(therapist_id):
#     """Update therapist details."""
#     name = request.form['name']
#     specialization = request.form['specialization']
#     qualifications = request.form['qualifications']
#     contact = request.form['contact']

#     therapist_collection.update_one(
#         {"_id": ObjectId(therapist_id)},
#         {"$set": {
#             "name": name,
#             "specialization": specialization,
#             "qualifications": qualifications,
#             "contact": contact
#         }}
#     )

#     flash("Therapist details updated!", "success")
#     return redirect(url_for('manage_therapists'))

# @app.route('/delete_therapist/<therapist_id>', methods=['POST'])
# def delete_therapist(therapist_id):
#     """Delete therapist profile."""
#     therapist_collection.delete_one({"_id": ObjectId(therapist_id)})
#     flash("Therapist deleted!", "danger")
#     return redirect(url_for('manage_therapists'))

# @app.route('/verify_therapist/<therapist_id>')
# def verify_therapist(therapist_id):
#     """Verify therapist profile."""
#     therapist_collection.update_one(
#         {"_id": ObjectId(therapist_id)},
#         {"$set": {"verified": True}}
#     )
#     flash("Therapist verified!", "success")
#     return redirect(url_for('manage_therapists'))

# @app.route('/reject_therapist/<therapist_id>')
# def reject_therapist(therapist_id):
#     """Reject therapist profile and remove it from the database."""
#     therapist_collection.delete_one({"_id": ObjectId(therapist_id)})
#     flash("Therapist rejected and removed!", "danger")
#     return redirect(url_for('manage_therapists'))


# from bson import ObjectId

# Show Manage Therapists Page (Admin Dashboard)
@app.route('/manage_therapists')
def manage_therapists():
    # Update any therapists who don't have the 'verified' field
    users_collection.update_many(
        {"role": "Therapist", "verified": {"$exists": False}},
        {"$set": {"verified": False}}
    )

    unverified_therapists = list(users_collection.find({
        "role": "Therapist",
        "verified": False
    }))

    verified_therapists = list(users_collection.find({
        "role": "Therapist",
        "verified": True
    }))

    return render_template('manage_therapists.html',
                           unverified_therapists=unverified_therapists,
                           verified_therapists=verified_therapists)




# Register Therapist (or Admin adding one manually)
# @app.route('/add_therapist', methods=['POST'])
# def add_therapist():
#     name = request.form['name']
#     specialization = request.form['specialization']
#     qualifications = request.form['qualifications']
#     contact = request.form['contact']
#     email = request.form['email']
#     password = generate_password_hash(request.form['password'])

#     therapist_data = {
#         "name": name,
#         "email": email,
#         "password": password,
#         "specialization": specialization,
#         "qualifications": qualifications,
#         "contact": contact,
#         "role": "therapist",
#         "verified": False
#     }

#     users_collection.insert_one(therapist_data)
#     flash("Therapist registered and pending verification.", "info")
#     return redirect(url_for('manage_therapists'))

# Verify Therapist
# @app.route('/verify_therapist/<therapist_id>')
# def verify_therapist(therapist_id):
#     users_collection.update_one(
#         {"_id": ObjectId(therapist_id)},
#         {"$set": {"verified": True}}
#     )
#     flash("Therapist has been verified.", "success")
#     return redirect(url_for('manage_therapists'))

# @app.route('/reject_therapist/<therapist_id>')
# def reject_therapist(therapist_id):
#     users_collection.delete_one({"_id": ObjectId(therapist_id)})
#     flash("Therapist rejected and deleted.", "danger")
#     return redirect(url_for('manage_therapists'))


# # Update Therapist (optional)
# @app.route('/update_therapist/<therapist_id>', methods=['POST'])
# def update_therapist(therapist_id):
#     users_collection.update_one(
#         {"_id": ObjectId(therapist_id)},
#         {"$set": {
#             "name": request.form['name'],
#             "specialization": request.form['specialization'],
#             "qualifications": request.form['qualifications'],
#             "contact": request.form['contact']
#         }}
#     )
#     flash("Therapist details updated.", "success")
#     return redirect(url_for('manage_therapists'))

# @app.route('/delete_therapist/<therapist_id>')
# def delete_therapist(therapist_id):
#     users_collection.delete_one({"_id": ObjectId(therapist_id)})
#     flash("Therapist deleted successfully.", "danger")
#     return redirect(url_for('manage_therapists'))



@app.route('/verify_therapist/<therapist_id>')
def verify_therapist(therapist_id):
    users_collection.update_one(
        {"_id": ObjectId(therapist_id)},
        {"$set": {"verified": True}}
    )
    flash("Therapist has been verified.", "success")
    return redirect(url_for('manage_therapists'))

@app.route('/reject_therapist/<therapist_id>')
def reject_therapist(therapist_id):
    users_collection.delete_one({"_id": ObjectId(therapist_id)})
    flash("Therapist application has been rejected.", "warning")
    return redirect(url_for('manage_therapists'))

# @app.route('/edit_therapist/<therapist_id>', methods=['GET', 'POST'])
# def edit_therapist(therapist_id):
#     therapist = users_collection.find_one({"_id": ObjectId(therapist_id)})

#     if request.method == 'POST':
#         updated_data = {
#             "name": request.form['name'],
#             "email": request.form['email'],
#             "specialization": request.form['specialization'],
#             "qualification": request.form['qualification'],
#             "experience": request.form['experience'],
#             "contact": request.form['contact']
#         }
#         users_collection.update_one(
#             {"_id": ObjectId(therapist_id)},
#             {"$set": updated_data}
#         )
#         flash("Therapist information updated.", "success")
#         return redirect(url_for('manage_therapists'))

#     return render_template("edit_therapist.html", therapist=therapist)

@app.route('/edit_therapist/<therapist_id>')
def edit_therapist(therapist_id):
    therapist = users_collection.find_one({"_id": ObjectId(therapist_id)})
    return render_template('edit_therapist.html', therapist=therapist)

@app.route('/update_therapist/<therapist_id>', methods=['POST'])
def update_therapist(therapist_id):
    updated_data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "specialization": request.form['specialization'],
        "qualification": request.form['qualification'],
        "experience": request.form['experience'],
        "contact": request.form['contact']
    }

    users_collection.update_one(
        {"_id": ObjectId(therapist_id)},
        {"$set": updated_data}
    )

    flash("Therapist details updated successfully.", "success")
    return redirect(url_for('manage_therapists'))



@app.route('/delete_therapist/<therapist_id>')
def delete_therapist(therapist_id):
    users_collection.delete_one({"_id": ObjectId(therapist_id)})
    flash("Therapist has been deleted.", "danger")
    return redirect(url_for('manage_therapists'))









@app.route("/therapist_dashboard")
def therapist_dashboard():
    return render_template("therapist_dashboard.html", user=session["user"])

@app.route("/caretaker_dashboard")
def caretaker_dashboard():
    return render_template("caretaker_dashboard.html", user=session["user"])

@app.route("/patient_dashboard")
def patient_dashboard():
    if "user" not in session or session["user"]["role"] != "Patient":
        return redirect(url_for("login"))  # Redirect if not an admin

    return render_template("dashboard.html")
    
    # user = users_collection.find_one({"_id": ObjectId(session["user_id"])})

    # return render_template("dashboard.html", user=user["name"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# Function to calculate quiz result
# Function to calculate quiz result based on answers
def calculate_result(selected_answers):
    category_scores = {"Anxiety": 0, "Depression": 0, "Stress": 0, "Normal": 0}

    for answer in selected_answers:
        if ":" not in answer or answer.endswith(":"):  
            continue  # Skip invalid/missing answers
        
        try:
            category, score = answer.split(":")
            category_scores[category] += int(score)
        except ValueError:
            continue  

    print(f"Final category scores: {category_scores}")  # Debugging output

    # 🔥 **Correct Fix for "All Never" Case**
    if all(score == 0 for cat, score in category_scores.items() if cat != "Normal"):
        return "Normal"  # If every category except "Normal" is zero, return "Normal"

    # Finding the highest-scoring category
    max_score = max(category_scores.values())  
    highest_categories = [cat for cat, score in category_scores.items() if score == max_score]

    # **Advanced Tie-Breaking Logic**
    if len(highest_categories) > 1:
        priority_order = ["Depression", "Anxiety", "Stress", "Normal"]  
        for category in priority_order:
            if category in highest_categories:
                return category

    return highest_categories[0]  # Return the highest-scoring category





@app.route("/quiz_page")
def quiz_page():
    if "user" not in session:
        return redirect(url_for("dashboard"))

    questions = list(quiz_collection.find({}, {"_id": 0}))  # Fetch all questions
    return render_template("quiz.html", questions=questions)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    if "user" not in session:
        return redirect(url_for("dashboard"))

    # Ensure all questions are answered
    answers = list(request.form.values())  # Collect selected answers
    print("Received Answers:", answers)
    if not answers or "" in answers:  # Check if any answer is missing
        flash("Please answer all questions before submitting.", "danger")
        return redirect(url_for("quiz_page"))  # Redirect back to quiz page

    result_category = calculate_result(answers)  # Determine category

    # Store quiz result in MongoDB
    quiz_results_collection = db["quiz_results"]
    quiz_results_collection.insert_one({
        "user_id": session["user_id"],
        "name": session["user"],
        "quiz_result": result_category
    })

    return render_template("quiz_result.html", result=result_category)




# Route to fetch quiz results (For Testing)
@app.route('/get_results', methods=['GET'])
def get_results():
    results = list(quiz_results_collection.find({}, {"_id": 0}))
    return jsonify(results)




@app.route("/check_session")
def check_session():
    return jsonify({"user_id": session.get("user_id")})


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

@app.route('/suggestions/', methods=['GET'])
def suggestions():
    category = request.args.get('category')  # Get category from URL
    if not category:
        return "Category not provided", 400  # Handle missing category

    data = selfcare_collection.find_one({"category": category})
    
    if data:
        return render_template('suggestions.html', resources=data["resources"], category=category)
    else:
        return render_template('suggestions.html', resources={}, category=category)  # No data found case
    
@app.route("/get_resources")
def get_resources():
    category = request.args.get("category")
    
    if not category:
        return jsonify({"error": "Category not provided"}), 400

    resource_data = selfcare_collection.find_one({"category": category}, {"_id": 0})

    if not resource_data:
        return jsonify({"error": "No resources found for this category"}), 404

    return jsonify(resource_data)

#todo and notifications

@app.route("/add_todo", methods=["POST"])
def add_todo():
    data = request.json
    print("Received To-Do:", data)
    todos_collection.insert_one({"text": data["text"]})
    return jsonify({"message": "To-Do saved successfully!"})

@app.route("/get_todos", methods=["GET"])
def get_todos():
    todos = list(todos_collection.find({}, {"_id": 0}))
    return jsonify(todos)

@app.route("/delete_todo", methods=["POST"])
def delete_todo():
    data = request.json
    todos_collection.delete_one({"text": data["text"]})
    return jsonify({"message": "To-Do deleted successfully!"})

@app.route("/add_notification", methods=["POST"])
def add_notification():
    data = request.json
    print("Received Notification:", data)
    notifications_collection.insert_one({"text": data["text"], "time": data["time"]})
    return jsonify({"message": "Notification saved successfully!"})

@app.route("/get_notifications", methods=["GET"])
def get_notifications():
    notifications = list(notifications_collection.find({}, {"_id": 0}))
    return jsonify(notifications)

# @app.route("/update_notification", methods=["POST"])
# def update_notification():
#     data = request.json
#     notification_id = data["id"]
#     new_status = data["status"]
#     notifications_collection.update_one(
#         {"_id": ObjectId(notification_id)},
#         {"$set": {"status": new_status}}
#     )
#     return jsonify({"message": "Notification updated successfully!"})

# @app.route("/delete_notification", methods=["POST"])
# def delete_notification():
#     data = request.json
#     notification_id = data["id"]
#     notifications_collection.delete_one({"_id": ObjectId(notification_id)})
#     return jsonify({"message": "Notification deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
