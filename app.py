from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import google.generativeai as genai
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import tempfile
import webbrowser
import datetime
import wikipedia
from config import apikey

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Configure API key
genai.configure(api_key=apikey)

# Initialize chat model
def initialize_chat_model():
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )

    return model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "your name is stella who is an ai chatbot that is friendly and talks in a natural and human like manner you have the traits of a soft spoken european girl and answer questions in a short and precise way and also dont use emojis while answering\n",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Hello! I'm Stella, nice to meet you. How can I help you today? \n",
                ],
            },
        ]
    )

# Global chat session
chat_session = initialize_chat_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/message', methods=['POST'])
def process_message():
    data = request.json
    query = data.get('message', '')
    
    if not query:
        return jsonify({"error": "No message provided"}), 400
    
    # Check for special commands
    result = handle_special_commands(query)
    if result:
        return jsonify(result)
    
    try:
        # Get response from AI
        response = chat_session.send_message(query)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    
    # Save the uploaded audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
        audio_file.save(temp_audio.name)
        temp_filename = temp_audio.name
    
    try:
        # Process audio with speech recognition
        r = sr.Recognizer()
        with sr.AudioFile(temp_filename) as source:
            audio = r.record(source)
            try:
                text = r.recognize_google(audio, language="en-in")
                os.unlink(temp_filename)  # Clean up temp file
                return jsonify({"text": text})
            except Exception as e:
                os.unlink(temp_filename)  # Clean up temp file
                return jsonify({"error": f"Speech recognition error: {str(e)}"}), 500
    except Exception as e:
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)  # Clean up temp file
        return jsonify({"error": f"Error processing audio: {str(e)}"}), 500

def handle_special_commands(query):
    query_lower = query.lower()
    
    # Handle website opening
    sites = [["Youtube", "https://youtube.com"], ["Google", "https://google.com"], ["Canva", "https://canva.com"]]
    for site in sites:
        if f'open {site[0]}'.lower() in query_lower:
            webbrowser.open(site[1])
            return {"response": f"Opening {site[0]}. What would you like to search there?", "action": "open_website", "site": site[0]}
    
    # Handle app opening
    if 'open music' in query_lower:
        musicPath = "/System/Applications/Music.app"
        os.system(f"open {musicPath}")
        return {"response": "Opening Music app for you."}
        
    elif "the weather app" in query_lower:
        weatherPath = "/System/Applications/Weather.app"
        os.system(f"open {weatherPath}")
        return {"response": "Opening Weather app for you."}
        
    # Wikipedia search
    elif 'wikipedia' in query_lower:
        try:
            search_term = query.replace('wikipedia', '').strip()
            results = wikipedia.summary(search_term, sentences=1)
            return {"response": f"According to Wikipedia: {results}"}
        except:
            return {"response": "No result found on Wikipedia for that query."}
        
    # Time request
    elif "the time" in query_lower:
        hour = datetime.datetime.now().strftime("%H")
        minute = datetime.datetime.now().strftime("%M")
        return {"response": f"The time is {hour} hours {minute} minutes"}
        
    # Exit command
    elif "stella bye" in query_lower:
        return {"response": "Thank you for chatting with me. Goodbye!"}
        
    return None

if __name__ == '__main__':
    app.run(debug=True, port=5000)