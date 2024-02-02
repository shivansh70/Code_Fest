import getpass
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import os
import speech_recognition as sr
import pandas as pd
from gtts import gTTS
import tempfile
import platform

# Sample user credentials (replace with your own user data)
valid_users = {'user1': 'password1', 'user2': 'password2'}

def authenticate_user():
    attempts = 3

    while attempts > 0:
        username = input("Enter your username: ")
        password = input("Enter your password: ")  # Using getpass for secure password input

        if username in valid_users and valid_users[username] == password:
            print("Authentication successful. Welcome,", username)
            return True
        else:
            attempts -= 1
            print(f"Authentication failed. Remaining attempts: {attempts}")

    print("Authentication failed. Exiting.")
    return False

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
    llm = OpenAI(temperature=0, openai_api_key='#')
    agent = create_csv_agent(llm, filePath, verbose=True)
    agent.run(input_text)

if __name__ == "__main__":
    if authenticate_user():
        user_input = process_input()

        if user_input:
            run_agent_with_input(user_input)
    else:
        print("Authentication failed. Exiting.")

    # Load the dataset
    dataset = pd.read_csv("employee_data.csv")  # Replace "your_data.csv" with the actual file name

    # Convert 'StartDate' and 'ExitDate' to datetime objects
    dataset['StartDate'] = pd.to_datetime(dataset['StartDate'])
    dataset['ExitDate'] = pd.to_datetime(dataset['ExitDate'])

    # Filter out rows with missing 'StartDate' or 'ExitDate'
    filtered_dataset = dataset.dropna(subset=['StartDate', 'ExitDate'])

    # Calculate the employment duration for each employee
    filtered_dataset['EmploymentDuration'] = (filtered_dataset['ExitDate'] - filtered_dataset['StartDate']).dt.days

    # Assume Performance Score is a measure of utilization (you can replace it with the relevant metric)
    utilization_data = filtered_dataset.groupby('EmpID')['Performance Score'].mean().reset_index()

    # Display the calculated utilization
    print(utilization_data)