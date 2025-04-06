# Stella - AI Voice Assistant Chatbot

## Overview

Stella is a friendly, voice-activated AI assistant that uses Google's Gemini 1.5 Flash model to provide natural, conversational responses. Designed to sound like a soft-spoken European girl, Stella can perform various tasks through voice commands.

## Features

- **Voice Recognition**: Listens to user commands using speech recognition
- **Natural Voice Responses**: Speaks responses using text-to-speech
- **Web Navigation**: Opens websites like YouTube, Google, and Canva
- **Search Capabilities**: Can search within opened websites
- **Wikipedia Integration**: Searches and summarizes Wikipedia articles
- **System Applications**: Opens music and weather apps
- **Time Information**: Provides current time when asked
- **Conversational AI**: Engages in natural conversation using Google's Gemini model

## Requirements

- Python 3.9+
- Speech Recognition library
- Google Generative AI library
- Internet connection for API calls
- macOS (for system-specific commands)

## Setup

1. Clone the repository
2. Install required packages:
   ```
   pip install SpeechRecognition google-generativeai wikipedia
   ```
3. Set up your Google Gemini API key in `config.py`
4. Run the application:
   ```
   python main.py
   ```

## Usage

- Say "Hello" to start a conversation with Stella
- Ask questions or give commands like:
  - "Open YouTube"
  - "What's the time?"
  - "Open music"
  - "Tell me about [Wikipedia topic]"
- Say "Stella Bye" to exit

## Note

This project uses Google's Gemini AI API which requires an API key. The API key in the config file should be kept private and not shared publicly.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

[Your Name]
