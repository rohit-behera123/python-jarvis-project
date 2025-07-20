from flask import Flask, render_template
import speech_recognition as sr
from gtts import gTTS
import playsound
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import webbrowser
import threading
import time
import keyboard  # <-- Added for spacebar control

app = Flask(__name__)
logs = []

# === Logging Function ===
def log(text):
    print(text)
    logs.append(text)
    if len(logs) > 100:
        logs.pop(0)

# === Speak using gTTS and auto-delete file ===
def speak(text):
    log(f"🧠 Jarvis: {text}")
    try:
        filename = "voice.mp3"
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
        playsound.playsound(filename)
        time.sleep(0.2)
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        log(f"⚠️ Speak error: {e}")

# === Greet on start ===
def greet_user():
    speak("Hello Rohit, I am Jarvis. How can I help you today?")
    log("🎤 Listening...")  # Initial listening prompt

# === Handle voice commands ===
def handle_command(command):
    command = command.lower()
    log(f"🎙️ You: {command}")

    try:
        if 'play' in command:
            song = command.replace('play', '')
            speak('Playing ' + song)
            pywhatkit.playonyt(song)

        elif 'pause the video' in command:
            speak("OK")
            keyboard.press_and_release('space')  # Simulate spacebar key press

        elif 'resume the video' in command:
            speak("resuming the video")
            keyboard.press_and_release('space')  # Simulate spacebar key press

        elif 'time' in command:
            time_now = datetime.datetime.now().strftime('%I:%M %p')
            speak('Current time is ' + time_now)

        elif 'who is' in command:
            person = command.replace('who is', '')
            info = wikipedia.summary(person, 1)
            speak(info)

        elif 'joke' in command:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'open youtube' in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'open chatgpt' in command:
            speak("Opening ChatGPT")
            webbrowser.open("https://chat.openai.com")

        elif 'stop' in command or 'exit' in command:
            speak("Goodbye Rohit!")
            os._exit(0)

        else:
            speak("Sorry, I didn't understand that.")
    
    except Exception as e:
        log(f"⚠️ Error: {str(e)}")

    log("🎤 Listening...")

# === Run handle_command in a background thread ===
def process_command(command):
    threading.Thread(target=handle_command, args=(command,), daemon=True).start()

# === Listening Loop ===
def listen():
    r = sr.Recognizer()
    greet_user()

    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, timeout=5)
                command = r.recognize_google(audio)
                process_command(command)
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                log("🤷 Couldn't understand audio")
                log("🎤 Listening...")
            except sr.RequestError:
                log("⚠️ Could not connect to speech service")
                log("🎤 Listening...")

# === Flask route for browser log viewer ===
@app.route("/")
def index():
    return render_template("index.html", logs=logs)

# === Start listener in thread ===
def run_jarvis():
    listen()

# === Main Flask App Entry ===
if __name__ == "__main__":
    threading.Thread(target=run_jarvis, daemon=True).start()
    print("🌐 Flask is running at http://127.0.0.1:5000")
    app.run(debug=False, use_reloader=False, host="127.0.0.1", port=5000)
