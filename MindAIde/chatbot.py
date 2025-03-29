import os
from flask import Blueprint, request, jsonify, render_template
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure OpenAI API Key is loaded
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("⚠️ OpenAI API Key is missing. Add it to your .env file.")

# Initialize chatbot
chatbot_bp = Blueprint("chatbot", __name__, template_folder="templates")
llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
memory = ConversationBufferMemory()

def get_chatbot_response(user_input):
    """Processes user input and returns chatbot response."""
    return llm.predict(user_input)

# Chatbot Route
@chatbot_bp.route("/", methods=["GET", "POST"])
def chatbot_page():
    if request.method == "POST":
        user_message = request.json.get("message")
        bot_response = get_chatbot_response(user_message)
        return jsonify({"response": bot_response})
    
    return render_template("chatbot.html")  # Ensure chatbot.html exists!
