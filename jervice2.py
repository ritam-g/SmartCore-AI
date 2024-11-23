import pyttsx3  # Converts text to speech
import speech_recognition as sr  # For voice recognition
import datetime  # To fetch the current time and date
import wikipedia  # To perform Wikipedia searches
import webbrowser  # To open web pages
import os  # To interact with the operating system
import random  # To select random songs or items
import sys  # For exiting the program

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set to the first available voice

# Function for text-to-speech
def speak(audio):
    """Speaks the given text using the pyttsx3 engine."""
    engine.say(audio)
    engine.runAndWait()

# Function to wish the user based on the time of the day
def wish_me():
    """Greets the user based on the current time."""
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis, your assistant. How can I help you today?")

# Function to take commands from the microphone
def take_command():
    """Takes voice input from the user and returns it as a string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except sr.UnknownValueError:
        print("I couldn't understand. Could you repeat that?")
        speak("I couldn't understand. Could you repeat that?")
        return "None"
    except sr.RequestError:
        print("Voice service is unavailable.")
        speak("Sorry, voice service is currently unavailable.")
        return "None"
    return query.lower()

# Additional functionalities
def open_application(path, app_name):
    """Opens a specified application."""
    if os.path.exists(path):
        speak(f"Opening {app_name}")
        os.startfile(path)
    else:
        speak(f"Sorry, I couldn't find {app_name}")

def play_random_music(directory):
    """Plays a random music file from a specified directory."""
    if os.path.exists(directory):
        songs = os.listdir(directory)
        if songs:
            song = random.choice(songs)
            speak(f"Playing {song}")
            os.startfile(os.path.join(directory, song))
        else:
            speak("No songs found in the music directory.")
    else:
        speak("Music directory not found.")

def calculator():
    """Simple calculator to perform basic arithmetic."""
    speak("Please tell me the first number")
    num1 = float(take_command())
    speak("Please tell me the operator")
    operator = take_command()
    speak("Please tell me the second number")
    num2 = float(take_command())
    try:
        if "plus" in operator or "+" in operator:
            result = num1 + num2
        elif "minus" in operator or "-" in operator:
            result = num1 - num2
        elif "multiply" in operator or "times" in operator or "*" in operator:
            result = num1 * num2
        elif "divide" in operator or "/" in operator:
            result = num1 / num2
        else:
            speak("Operator not recognized")
            return
        speak(f"The result is {result}")
    except Exception as e:
        speak("An error occurred while performing the calculation")

def take_notes():
    """Allows the user to create a quick note."""
    speak("What should I write down?")
    note = take_command()
    if note != "None":
        with open("notes.txt", "a") as file:
            file.write(f"{datetime.datetime.now()} - {note}\n")
        speak("Note saved successfully!")

# Main driver function
def main():
    """Main function to handle user commands."""
    speak("Initializing system...")
    wish_me()

    while True:
        query = take_command()
        if query == "none":
            continue

        # Core functionalities
        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("youtube.com")

        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("google.com")

        elif "play music" in query:
            music_dir = "C:\\Users\\swaru\\OneDrive\\Desktop\\JERVICE\\jervice_music"
            play_random_music(music_dir)

        elif "what is the time" in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {time}")

        elif "open editor" in query:
            editor_path = "C:\\Users\\swaru\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            open_application(editor_path, "Visual Studio Code")

        elif "calculator" in query:
            calculator()

        elif "take notes" in query or "write a note" in query:
            take_notes()

        elif "exit" in query or "quit" in query:
            speak("Goodbye! Have a great day!")
            sys.exit()

        else:
            speak("I didn't understand that command. Please try again.")

# Run the main function
if __name__ == "__main__":
    main()
