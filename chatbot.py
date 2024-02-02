from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import os
import speech_recognition as sr
from gtts import gTTS
import tempfile
import platform

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def process_input():
    print("Choose input type:")
    print("1. Text")
    print("2. Voice")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        user_input = input("Enter your text input: ")
    elif choice == "2":
        user_input = recognize_speech()
    else:
        print("Invalid choice. Please enter 1 or 2.")
        user_input = None

    return user_input

def run_agent_with_input(input_text):
    filePath = "employee_data.csv"
    llm = OpenAI(temperature=0, openai_api_key='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')
    agent = create_csv_agent(llm, filePath, verbose=True)
    agent.run(input_text)

if __name__ == "__main__":
    user_input = process_input()

    if user_input:
        run_agent_with_input(user_input)
