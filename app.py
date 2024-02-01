import getpass
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import os
import speech_recognition as sr
import pandas as pd
from gtts import gTTS
import tempfile
import platform
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

class EmployeeUtilizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Utilization App")

        # Sample user credentials (replace with your own user data)
        self.valid_users = {'user1': 'password1', 'user2': 'password2'}

        # Create UI components
        self.label_username = ttk.Label(root, text="Username:")
        self.entry_username = ttk.Entry(root)

        self.label_password = ttk.Label(root, text="Password:")
        self.entry_password = ttk.Entry(root, show="*")

        self.button_login = ttk.Button(root, text="Login", command=self.authenticate_user)
        self.label_status = ttk.Label(root, text="")

        self.label_input_type = ttk.Label(root, text="Choose input type:")
        self.combobox_input_type = ttk.Combobox(root, values=["Text", "Voice"], state="disabled")

        self.label_user_input = ttk.Label(root, text="Enter your text input:")
        self.entry_user_input = ttk.Entry(root, state="disabled")

        self.button_voice_input = ttk.Button(root, text="Voice Input", command=self.recognize_speech, state="disabled")

        self.button_run_agent = ttk.Button(root, text="Run Agent", command=self.run_agent_with_input, state="disabled")

        self.button_generate_report = ttk.Button(root, text="Generate Report", command=self.generate_report, state="disabled")

        # Grid layout
        self.label_username.grid(row=0, column=0, sticky=tk.W)
        self.entry_username.grid(row=0, column=1)

        self.label_password.grid(row=1, column=0, sticky=tk.W)
        self.entry_password.grid(row=1, column=1)

        self.button_login.grid(row=2, column=0, columnspan=2, pady=10)
        self.label_status.grid(row=3, column=0, columnspan=2)

        self.label_input_type.grid(row=4, column=0, sticky=tk.W)
        self.combobox_input_type.grid(row=4, column=1)

        self.label_user_input.grid(row=5, column=0, sticky=tk.W)
        self.entry_user_input.grid(row=5, column=1)

        self.button_voice_input.grid(row=6, column=0, columnspan=2, pady=10)

        self.button_run_agent.grid(row=7, column=0, columnspan=2, pady=10)

        self.button_generate_report.grid(row=8, column=0, columnspan=2, pady=10)

    def authenticate_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username in self.valid_users and self.valid_users[username] == password:
            self.label_status["text"] = f"Authentication successful. Welcome, {username}"
            self.enable_input_controls()
        else:
            self.label_status["text"] = "Authentication failed."

    def enable_input_controls(self):
        self.combobox_input_type["state"] = "readonly"
        self.entry_user_input["state"] = "normal"
        self.button_voice_input["state"] = "normal"
        self.button_run_agent["state"] = "normal"
        self.button_generate_report["state"] = "normal"

    def recognize_speech(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            self.entry_user_input.delete(0, tk.END)
            self.entry_user_input.insert(0, text)
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def run_agent_with_input(self):
        input_type = self.combobox_input_type.get()

        if input_type == "Text":
            user_input = self.entry_user_input.get()
        elif input_type == "Voice":
            self.recognize_speech()
            user_input = self.entry_user_input.get()
        else:
            self.label_status["text"] = "Invalid input type. Please choose Text or Voice."
            return

        if user_input:
            filePath = "employee_data.csv"
            llm = OpenAI(temperature=0, openai_api_key='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')
            agent = create_csv_agent(llm, filePath, verbose=True)
            agent.run(user_input)

    def generate_report(self):
        # Load the dataset
        dataset = pd.read_csv("employee_data.csv")  # Replace with your actual file name

        # Plot a bar graph of employee status
        status_counts = dataset['EmployeeStatus'].value_counts()

        # Plot 1: Employee Status Distribution
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)  # 1 row, 2 columns, subplot 1

        status_counts.plot(kind='bar', color='skyblue', rot=45)  # Rotate labels by 45 degrees
        plt.title('Employee Status Distribution')
        plt.xlabel('Employee Status')
        plt.ylabel('Number of Employees')
        plt.tight_layout()  # Ensure tight layout to prevent label cutoff

        # Plot 2: Employee Status Distribution Based on Department
        plt.subplot(1, 2, 2)  # 1 row, 2 columns, subplot 2

        # Group by department and count the number of employees in each status
        department_status_counts = dataset.groupby(['DepartmentType', 'EmployeeStatus']).size().unstack(fill_value=0)

        # Plot stacked bar chart
        department_status_counts.plot(kind='bar', stacked=True, colormap='viridis', figsize=(12, 6))
        plt.title('Employee Status Distribution by Department')
        plt.xlabel('Department')
        plt.ylabel('Number of Employees')
        plt.legend(title='Employee Status', bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        plt.show()

        total_employees = len(dataset)
        if 'Active' in status_counts:
            active_percentage = (status_counts['Active'] / total_employees) * 100
            print(f"Percentage of Active Employees: {active_percentage:.2f}%")

            if active_percentage < 70:
                print("Suggestion for Active Employees: Consider assigning additional tasks or projects.")
            elif active_percentage > 90:
                print("Suggestion for Active Employees: Monitor workload to prevent burnout.")

        if 'Inactive' in status_counts:
            inactive_percentage = (status_counts['Inactive'] / total_employees) * 100
            print(f"Percentage of Inactive Employees: {inactive_percentage:.2f}%")

            if inactive_percentage > 30:
                print("Suggestion for Inactive Employees: Identify reasons for inactivity and consider reassigning tasks or providing training.")

        if 'On Leave' in status_counts:
            on_leave_percentage = (status_counts['On Leave'] / total_employees) * 100
            print(f"Percentage of Employees on Leave: {on_leave_percentage:.2f}%")

            if on_leave_percentage > 10:
                print("Suggestion for Employees on Leave: Plan for a smooth return-to-work process.")
        else:
            print("No specific suggestions. Employee status distribution is balanced.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeUtilizationApp(root)
    root.mainloop()