import os
import streamlit as st
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# Set up Streamlit UI
st.set_page_config(page_title="ChatBot 🤖 - MIND AIDE", page_icon="🤖")
st.title("ChatBot 🤖 - MIND AIDE")

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")  # Adjust if needed
db = client["mental_health_db"]
collection = db["quiz_questions"]

# Initialize session state for chat and quiz
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# Fetch quiz questions from MongoDB
def get_quiz_questions():
    questions = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectID
    return questions

# Process quiz results
def process_quiz_results():
    scores = {"Stress": 0, "Depression": 0, "Anxiety": 0, "Normal": 0}
    
    for question in st.session_state.quiz_questions:
        category = question["category"]
        selected_score = st.session_state.quiz_answers.get(question["question_text"], 0)
        scores[category] += selected_score

    # Determine the highest category
    final_result = max(scores, key=scores.get)
    return final_result

# Initialize LangChain chatbot
@st.cache_resource
def load_conversation():
    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini")
    memory = ConversationBufferMemory()
    conversation = ConversationChain(llm=llm, memory=memory)
    return conversation

conversation = load_conversation()

# Navigation options
page = st.sidebar.radio("Select Feature", ["ChatBot 🤖", "Mental Health Quiz 🧠"])

# Chatbot Section
if page == "ChatBot 🤖":
    st.subheader("Chat with AI")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        response = conversation.predict(input=prompt)

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

# Mental Health Quiz Section
elif page == "Mental Health Quiz 🧠":
    st.subheader("Mental Health Assessment")

    if not st.session_state.quiz_started:
        if st.button("Start Quiz"):
            st.session_state.quiz_started = True
            st.session_state.quiz_questions = get_quiz_questions()
            st.session_state.quiz_answers = {}

    if st.session_state.quiz_started:
        for question in st.session_state.quiz_questions:
            options = {opt["text"]: opt["score"] for opt in question["options"]}
            selected_option = st.radio(
                question["question_text"], options.keys(), key=question["question_text"]
            )
            st.session_state.quiz_answers[question["question_text"]] = options[selected_option]

        if st.button("Submit Quiz"):
            result = process_quiz_results()
            st.success(f"Your result is: **{result}**")
            st.session_state.quiz_started = False  # Reset quiz after submission
