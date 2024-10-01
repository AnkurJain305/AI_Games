import streamlit as st
from game1_image_recognition import ai_image_recognition_game
from game2_chatbot_voice_assistant import ai_chatbot_game
from game3_aiart import ai_art_generator_game  # Import the new AI Art Generator game

# Configure the Streamlit page settings
st.set_page_config(page_title="AI Awareness Games", layout="wide")

# Sidebar for navigation between the games
st.sidebar.title("AI Awareness for 8th Grade Students")
page = st.sidebar.selectbox(
    "Select a Game", 
    ["AI Image Recognition", "AI Chatbot with Voice Assistant", "AI Art Generator"]
)

# Main interface
if page == "AI Image Recognition":
    st.title("AI Image Recognition Game")
    ai_image_recognition_game()  # Calling the first game function from game1_image_recognition.py

elif page == "AI Chatbot with Voice Assistant":
    st.title("AI Chatbot with Voice Assistant Game")
    ai_chatbot_game()  # Calling the second game function from game2_chatbot_voice_assistant.py

elif page == "AI Art Generator":
    st.title("AI Art Generator Game")
    ai_art_generator_game()  # Calling the third game function from game3_ai_art_generator.py
