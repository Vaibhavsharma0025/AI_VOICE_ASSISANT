import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import google.generativeai as genai
import threading
import time

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "9dd617449de44314b3f90ec76d5e3167"  # Replace with your News API key
gemini_api = "AIzaSyBrHxaqYt4MJEi2pw3euZ32s0IiMDJHldA"  # Replace with your Gemini API key

# Configure Gemini
genai.configure(api_key=gemini_api)

def speak(text):
    """Fast TTS using pyttsx3"""
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    """Call Gemini to process AI commands"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(command)
    return response.text if response else "Sorry, I couldn’t process that."

def speak_ai_response(command):
    """Threaded AI response"""
    answer = aiProcess(command)
    speak(answer)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            webbrowser.open(link)
        else:
            speak("Song not found in library.")
    elif "news" in c.lower():
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                if not articles:
                    speak("Sorry, no news found.")
                else:
                    speak("Here are the top 5 news headlines for today:")
                    # Combine headlines into one string to speak at once
                    headlines_text = ""
                    for idx, article in enumerate(articles[:5], 1):
                        headline = article['title']
                        print(f"{idx}. {headline}")
                        headlines_text += f"Headline {idx}: {headline}. "
                    speak(headlines_text)  # Speak all at once
            else:
                speak("Sorry, I couldn't fetch the news right now.")
        except Exception as e:
            print("Error fetching news:", e)
            speak("Sorry, I couldn't fetch the news right now.")
    else:
        # Threaded Gemini AI processing for any question
        threading.Thread(target=speak_ai_response, args=(c,)).start()

if __name__ == "__main__":
    speak("Initializing ramu....")
    r = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Listening for wake word...")
                audio = r.listen(source)
            
            word = r.recognize_google(audio)
            print("Heard:", word)

            if "ramu" in word.lower():
                speak("Ya")
                
                # Listen for next command
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening for command...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=8)
                    command = r.recognize_google(audio)
                    print("Command:", command)
                    processCommand(command)

        except sr.WaitTimeoutError:
            print("Listening timed out, trying again...")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except Exception as e:
            print("Error:", e)
