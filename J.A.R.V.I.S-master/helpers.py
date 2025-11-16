import traceback
import pyttsx3
import pyautogui
import psutil
import pyjokes
import speech_recognition as sr
import json
import requests
import geocoder
from difflib import get_close_matches


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
g = geocoder.ip('me')
data = json.load(open('data.json'))

def speak(audio) -> None:
        engine.say(audio)
        engine.runAndWait()

def screenshot() -> None:
    img = pyautogui.screenshot()
    img.save('D:\\Screenshots\\screenshot.png')

def cpu() -> None:
    usage = str(psutil.cpu_percent())
    speak("CPU is at"+usage)

    battery = psutil.sensors_battery()
    speak("battery is at")
    speak(battery.percent)

def joke() -> None:
    for i in range(5):
        speak(pyjokes.get_jokes()[i])

def takeCommand() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.energy_threshold = 494
        r.adjust_for_ambient_noise(source, duration=1.5)
        audio = r.listen(source)

    try:
        print('Recognizing..')
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query}\n')

    except Exception as e:
        # print(e)

        print('Say that again please...')
        return 'None'
    return query

def weather():
    # --- DEFINE YOUR API HERE ---
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": ""+g.city+", "+g.country,
        "appid": "YOUR_API_KEY_HERE",
        "units": "metric"
    }
    # ----------------------------

    try:
        print(f"[weather] Request -> {url}")
        print(f"[weather] Params -> {params}")
        resp = requests.get(url, params=params, timeout=10)
    except requests.RequestException as e:
        print("[weather] Network/requests error:", repr(e))
        traceback.print_exc()
        return None

    print(f"[weather] HTTP {resp.status_code} Content-Type: {resp.headers.get('Content-Type')}")
    body = resp.text or ""
    print(f"[weather] Body length: {len(body)}")
    print("[weather] Body preview:\n", body[:600].replace("\n", "\\n"))

    if resp.status_code != 200:
        print("[weather] Non-200 response ->", resp.status_code)
        return None

    # try parsing JSON
    try:
        data = resp.json()
        print("[weather] JSON OK. Keys:", list(data.keys()))
        return data
    except ValueError:
        print("[weather] JSON parse failed.")
        print("[weather] Full body:\n", body)
        return None


def translate(word):
    word = word.lower()
    if word in data:
        speak(data[word])
    elif len(get_close_matches(word, data.keys())) > 0:
        x = get_close_matches(word, data.keys())[0]
        speak('Did you mean ' + x +
              ' instead,  respond with Yes or No.')
        ans = takeCommand().lower()
        if 'yes' in ans:
            speak(data[x])
        elif 'no' in ans:
            speak("Word doesn't exist. Please make sure you spelled it correctly.")
        else:
            speak("We didn't understand your entry.")

    else:
        speak("Word doesn't exist. Please double check it.")
