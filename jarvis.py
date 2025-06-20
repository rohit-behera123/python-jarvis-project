#here's the full code
# python-jarvis-project
#Python AI based jarvis project
import speech_recognition as sr
from gtts import gTTS
import playsound
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import webbrowser
import random

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = f"voice{random.randint(1,100000)}.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def listen_command():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            command = command.lower()
            print("You said:", command)
            return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Sorry, I couldn't reach the speech service.")
        return ""

def run_jarvis():
    command = listen_command()

    if 'play' in command:
        song = command.replace('play', '')
        speak(f'Playing {song}')
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f'The current time is {time}')

    elif 'who is' in command:
        person = command.replace('who is', '')
        try:
            info = wikipedia.summary(person, 1)
            print(info)
            speak(info)
        except:
            speak("I couldn't find information about that person.")

    elif 'open notepad' in command:
        os.system('start notepad')

    elif 'open chrome' in command:
        os.system('start chrome')

    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")

    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")

    elif 'search' in command:
        query = command.replace('search', '')
        pywhatkit.search(query)
        speak(f"Searching for {query}")

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif 'stop' in command or 'exit' in command:
        speak("Goodbye!")
        exit()

    else:
        speak("I didn't understand. Please say it again.")

# Keep running
while True:
    run_jarvis()
