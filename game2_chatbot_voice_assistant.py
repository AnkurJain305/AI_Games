import streamlit as st
import os
import textwrap
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import threading
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API key not found in environment variables.")
else:
    genai.configure(api_key=api_key)

# Function to get response from Gemini model
def get_gemini_response(question):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        st.error(f"Error fetching response from Gemini model: {e}")
        return ""

# Speech-to-Text function using microphone input
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
        try:
            st.info("Recognizing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError:
            st.error("Could not request results; check your internet connection.")
            return ""

# Text-to-Speech function
def text_to_speech(text):
    engine = pyttsx3.init()
    for sentence in text.split('.'):
        if sentence.strip():
            engine.say(sentence.strip())
            engine.runAndWait()
        if st.session_state.stop_speech:
            break
    st.session_state.is_speaking = False

# Function to run text-to-speech in a separate thread
def run_text_to_speech(text):
    st.session_state.stop_speech = False
    st.session_state.is_speaking = True
    thread = threading.Thread(target=text_to_speech, args=(text,))
    thread.start()

# AI Chatbot with Voice Assistant Game
def ai_chatbot_game():
    st.subheader("AI Chatbot with Voice Assistant")

    # Initialize session state
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""
    if 'response' not in st.session_state:
        st.session_state.response = ""
    if 'stop_speech' not in st.session_state:
        st.session_state.stop_speech = False
    if 'is_speaking' not in st.session_state:
        st.session_state.is_speaking = False

    # Button for speech input
    if st.button("Use Voice Input"):
        st.session_state.input_text = speech_to_text()
        if st.session_state.input_text:
            st.text(f"Recognized Speech: {st.session_state.input_text}")
            st.info("Fetching response from Gemini model...")
            st.session_state.response = get_gemini_response(st.session_state.input_text)
            if st.session_state.response:
                st.subheader("The response is:")
                st.write(st.session_state.response)
                run_text_to_speech(st.session_state.response)

    # Text input field
    input_text = st.text_input("Or type your question:", key="input", value=st.session_state.input_text)

    # Update session state when text input changes
    if input_text != st.session_state.input_text:
        st.session_state.input_text = input_text

    # Button for submitting the typed question
    if st.button("Ask the question"):
        if st.session_state.input_text:
            st.info("Fetching response from Gemini model...")
            st.session_state.response = get_gemini_response(st.session_state.input_text)
            if st.session_state.response:
                st.subheader("The response is:")
                st.write(st.session_state.response)
                run_text_to_speech(st.session_state.response)
        else:
            st.write("Please provide input to ask the question.")

    # Display the current response (if any)
    if st.session_state.response:
        st.subheader("Last response:")
        st.write(st.session_state.response)

        # Stop button for text-to-speech
        if st.session_state.is_speaking:
            if st.button("Stop Reading"):
                st.session_state.stop_speech = True
                st.success("Stopping the speech...")
        else:
            if st.button("Read Aloud"):
                run_text_to_speech(st.session_state.response)
