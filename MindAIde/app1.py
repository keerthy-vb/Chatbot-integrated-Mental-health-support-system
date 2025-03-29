import os
from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from quiz import quiz_bp
from chatbot import chatbot_bp
from selfcare import selfcare_bp  # Import self-care module
from appointments import appointments_bp  # Import therapist suggestions module

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
users_collection = db["users"]

# Register Blueprints
app.register_blueprint(quiz_bp, url_prefix="/quiz")
app.register_blueprint(chatbot_bp, url_prefix="/chatbot")
app.register_blueprint(selfcare_bp, url_prefix="/selfcare")  # Register self-care
app.register_blueprint(appointments_bp, url_prefix="/appointments")  # Register therapist suggestions

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        
        if users_collection.find_one({"email": email}):
            return "User already exists. Try logging in!"
        
        users_collection.insert_one({"name": name, "email": email, "password": password})
        return redirect(url_for("home"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.json["email"]
        password = request.json["password"]
        
        user = users_collection.find_one({"email": email})
        if user and check_password_hash(user["password"], password):
            session["user"] = user["name"]
            return redirect(url_for("home"))
        
        return "Invalid credentials. Try again!"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
    print("hello")
