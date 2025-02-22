import random
import speech_recognition as sr
import os
import google.generativeai as genai
import webbrowser
import openai
import datetime
from config import apikey


chatStr = ""

genai.configure(api_key=os.getenv("api_key_here"))

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
chat = model.start_chat(history=[])


def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"Tanish: {query}\n Stella: "
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def ai(prompt):
    openai.api_key = apikey
    text = f"Gemini response for Prompt: {prompt}\n ****************\n\n"

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response["choices"][0]["text"])
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)


def say(text):
    os.system(f"say {text}")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en -in")
            print(f'User said: {query}')
            return query
        except Exception as e:
            return'Sorry i did not get that '


def search_site(query):
    sites = [["Youtube", "https://youtube.com"], ["Wikipedia", "https://wikipedia.com"], ["Google", "https://google.com"], ["Canva", "https://canva.com"]]
    for site in sites:
        # Check if the user wants to open a specific site
        if f'open {site[0]}'.lower() in query.lower():
            say(f'Opening {site[0]} Sir...')
            webbrowser.open(site[1])

            # Ask what to search on the site
            say(f"What would you like to search on {site[0]}?")
            query2 = take_command()

            # Format the search URL for specific sites
            if site[0].lower() == 'youtube':
                search_url = f"https://www.youtube.com/results?search_query={query2.replace(' ', '+')}"
                say(f"searching {query2}")
            elif site[0].lower() == 'wikipedia':
                search_url = f"https://en.wikipedia.org/wiki/{query2.replace(' ', '_')}"
                say(f"searching {query2}")
            elif site[0].lower() == 'google':
                search_url = f"https://www.google.com/search?q={query2.replace(' ', '+')}"
                say(f"searching {query2}")
            webbrowser.open(search_url)
            break
            # Open the search URL

        else:
            say("Sorry, I didn't understand which site you want to open.")


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
        if "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours {minute} minutes")
        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        elif "Stella Quit".lower() in query.lower():
            print("Thank you")
            say("Thank You")
            exit()
        elif "Stella reset chat".lower() in query.lower():
            chatStr = ""
        else:
            print("Chatting...")
            chat(query)
