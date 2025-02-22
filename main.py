import speech_recognition as sr
import os
import google.generativeai as genai
import webbrowser
import datetime
from config import apikey
import wikipedia

genai.configure(api_key=apikey)


def converse(query):

    # Create the model
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

    chat_session = model.start_chat(
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
            "Hello! I'm Stella, nice to meet you.  How can I help you today? \n",
          ],
        },
      ]
    )

    response = chat_session.send_message(query)

    say(response.text)
    print(response.text)


def say(text):
    safe_text = text.replace('"', '\\"')  # Escape double quotes if present
    os.system(f'say "{safe_text}"')


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en -in")
            print(f'User said: {query}')
            return query
        except Exception as e:
            return'Sorry i did not get that '


def search_site(query):
    sites = [["Youtube", "https://youtube.com"], ["Google", "https://google.com"], ["Canva", "https://canva.com"]]
    for site in sites:
        if f'open {site[0]}'.lower() in query.lower():
            say(f'Opening {site[0]} Sir...')
            webbrowser.open(site[1])

            say(f"What would you like to search on {site[0]}?")
            query2 = take_command()

            if site[0].lower() == 'youtube':
                search_url = f"https://www.youtube.com/results?search_query={query2.replace(' ', '+')}"
                say(f"Searching {query2}")
            elif site[0].lower() == 'google':
                search_url = f"https://www.google.com/search?q={query2.replace(' ', '+')}"
                say(f"Searching {query2}")
            webbrowser.open(search_url)
            return True  # Query handled, return True


if 1+1 == 2:
    say("Hello I am Stella")
    print("Hello I am Stella")
    while True:
        print('listening...')
        query = take_command()
        search_site(query)
        if 'open music' in query:
            say(f'Opening music Sir...')
            musicPath = "/System/Applications/Music.app"
            os.system(f"open {musicPath}")

        elif "the weather app".lower() in query.lower():
            say('Showing weather sir...')
            weatherPath = "/System/Applications/Weather.app"
            os.system(f"open {weatherPath}")

        elif 'wikipedia' in query.lower():
            say("Searching in wikipedia..")
            try:
                query = query.replace('wikipedia', '')
                results = wikipedia.summary(query, sentences=1)
                say("According to Wikipedia:")
                print(results)
                say(results)
            except:
                say("No result found")

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours {minute} minutes")
        elif "Stella Bye".lower() in query.lower():
            print("Thank you ")
            say("Thank You ")
            exit()
        else:
            print("Processing...")
            converse(query)

