# resourcify_app.py
import streamlit as st
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import os
import speech_recognition as sr
import pandas as pd
import matplotlib.pyplot as plt
from subprocess import run
import re

# Sample user credentials (replace with your own user data)
valid_users = {'user1': 'password1', 'user2': 'password2'}

# Function to set the page configuration
def set_page_config():
    st.set_page_config(
        page_title="Resourcify",
        layout="wide",
        initial_sidebar_state="expanded",
    )

# Function to style the Streamlit app
def style_app():
    st.markdown(
        """
        <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .stSidebar {
            background-color: #2e2e2e;
            color: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stMain {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def authenticate_user():
    attempts = 3

    while attempts > 0:
        username = st.sidebar.text_input("Enter your username:")
        password = st.sidebar.text_input("Enter your password:", type='password')

        if username in valid_users and valid_users[username] == password:
            st.success(f"Authentication successful. Welcome, {username}")
            return True
        else:
            attempts -= 1
            st.warning(f"Authentication failed. Remaining attempts: {attempts}")

    st.error("Authentication failed. Exiting.")
    return False

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.text("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        st.text("Recognizing...")
        text = recognizer.recognize_google(audio)
        st.text(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.warning("Could not understand audio.")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def process_input():
    st.sidebar.text("Choose input type:")
    choice = st.sidebar.radio("Select input type:", ["Text", "Voice"])

    if choice == "Text":
        user_input = st.text_area("Enter your text input:")
    elif choice == "Voice":
        user_input = recognize_speech()
    else:
        st.warning("Invalid choice. Please select Text or Voice.")
        user_input = None

    return user_input

def run_agent_with_input(input_text):
    filePath = "employee_data.csv"
    llm = OpenAI(temperature=0, openai_api_key='#')
    agent = create_csv_agent(llm, filePath, verbose=True)

    # Store observations in a list
    conversation = []

    # User input
    conversation.append({"role": "user", "text": input_text})

    # Chatbot response
    chatbot_response = agent.run(input_text)
    conversation.append({"role": "chatbot", "text": chatbot_response})

    st.text_area("Chatbot Response:", chatbot_response, height=200, key="chatbot_response")  # Adjust height as needed


    # Ask the user if they want to run employee_edit
    run_employee_edit = st.checkbox("Run the employee_edit functionality?", key="run_employee_edit")

    if run_employee_edit:
        # Run employee_edit functionality
        employee_edit_function()

    # Ask the user if they want to see the report
    show_report = st.checkbox("Show the statistics?", key="show_report")

    if show_report:
        # Run analysis and generate a report
        analyze_and_generate_report(chatbot_response)

    # Display the entire conversation
    st.text("Entire Conversation:")
    for entry in conversation:
        st.text(f"{entry['role'].capitalize()}: {entry['text']}")

    # Clear the conversation list
    conversation.clear()





def analyze_and_generate_report(chatbot_response):
    # Load the dataset
    dataset = pd.read_csv("employee_data.csv")  # Replace with your actual file name

    # Plot a bar graph of employee status
    status_counts = dataset['EmployeeStatus'].value_counts()

    # Plot 1: Employee Status Distribution
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.bar(status_counts.index, status_counts.values, color='skyblue')
    ax1.set_title('Employee Status Distribution')
    ax1.set_xlabel('Employee Status')
    ax1.set_ylabel('Number of Employees')
    plt.xticks(rotation=45)  # Rotate labels by 45 degrees
    plt.tight_layout()  # Ensure tight layout to prevent label cutoff

    # Plot 2: Employee Status Distribution Based on Department
    fig2, ax2 = plt.subplots(figsize=(12, 6))

    # Group by department and count the number of employees in each status
    department_status_counts = dataset.groupby(['DepartmentType', 'EmployeeStatus']).size().unstack(fill_value=0)

    # Plot stacked bar chart
    department_status_counts.plot(kind='bar', stacked=True, colormap='viridis', ax=ax2)
    ax2.set_title('Employee Status Distribution by Department')
    ax2.set_xlabel('Department')
    ax2.set_ylabel('Number of Employees')
    ax2.legend(title='Employee Status', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Display the plots in Streamlit app
    st.pyplot(fig1)
    st.pyplot(fig2)

    # Display additional suggestions based on analysis
    total_employees = len(dataset)
    if 'Active' in status_counts:
        active_percentage = (status_counts['Active'] / total_employees) * 100
        st.text(f"Percentage of Active Employees: {active_percentage:.2f}%")

        if active_percentage < 70:
            st.text("Suggestion for Active Employees: Consider assigning additional tasks or projects.")
        elif active_percentage > 90:
            st.text("Suggestion for Active Employees: Monitor workload to prevent burnout.")

    if 'Inactive' in status_counts:
        inactive_percentage = (status_counts['Inactive'] / total_employees) * 100
        st.text(f"Percentage of Inactive Employees: {inactive_percentage:.2f}%")

        if inactive_percentage > 30:
            st.text("Suggestion for Inactive Employees: Identify reasons for inactivity and consider reassigning tasks or providing training.")

    if 'On Leave' in status_counts:
        on_leave_percentage = (status_counts['On Leave'] / total_employees) * 100
        st.text(f"Percentage of Employees on Leave: {on_leave_percentage:.2f}%")

        if on_leave_percentage > 10:
            st.text("Suggestion for Employees on Leave: Plan for a smooth return-to-work process.")
    else:
        st.text("No specific suggestions. Employee status distribution is balanced.")

def employee_edit_function():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('employee_data.csv')

    # Take user input for the number of EmpIDs to change
    num_empids = int(st.text_input("Enter the number of EmpIDs you want to change:", key="num_empids"))

    for _ in range(num_empids):
        # Take user input for EmpID
        emp_id = int(st.text_input("Enter EmpID:", key="emp_id"))

        # Find the employee in the DataFrame
        employee = df[df['EmpID'] == emp_id]

        if not employee.empty:
            # Display current projects for the selected employee
            st.text(f"Current projects for EmpID {emp_id}: {employee['Projects'].values[0]}")

            # Ask the user whether to add or decrease projects
            action = st.selectbox("Do you want to add or decrease projects?", ['add', 'decrease'], key="action")

            # Take user input for the number of projects to add or decrease
            project_change = int(st.text_input("Enter the number of projects to add or decrease:", key="project_change"))

            if action == 'add':
                # Prompt the user to enter the project division name for addition
                st.text("Enter the project division names for addition:")
                project_divisions = [st.text_input(f"Project Division {i + 1}:") for i in range(project_change)]
                if project_change < 0:
                    st.warning("Project count cannot be less than 0. Please enter a valid count.")
                    return
            else:
                # Prompt the user to enter the project division name for decrease
                st.text("Enter the project division names for decrease:")
                project_divisions = [st.text_input(f"Project Division {i + 1}:") for i in range(project_change)]
                if project_change > employee['Projects'].values[0]:
                    st.warning(f"Project count cannot be decreased by {project_change}. It is greater than the current count.")
                    return

            # Save the current row for later comparison
            old_row = employee.copy()

            # Update the number of projects based on user input
            if action == 'add':
                df.loc[df['EmpID'] == emp_id, 'Projects'] += project_change

                # Update the project divisions
                existing_divisions = df.loc[df['EmpID'] == emp_id, 'ProjectDivision'].values[0].split(',')
                for division in project_divisions:
                    if division not in existing_divisions:
                        existing_divisions.append(division)

                df.loc[df['EmpID'] == emp_id, 'ProjectDivision'] = ','.join(existing_divisions)

            elif action == 'decrease':
                df.loc[df['EmpID'] == emp_id, 'Projects'] -= project_change

                # Remove the project divisions
                existing_divisions = df.loc[df['EmpID'] == emp_id, 'ProjectDivision'].values[0].split(',')
                for division in project_divisions:
                    if division in existing_divisions:
                        existing_divisions.remove(division)

                df.loc[df['EmpID'] == emp_id, 'ProjectDivision'] = ','.join(existing_divisions)

            # Check if the updated projects count is greater than or equal to 0
            if df.loc[df['EmpID'] == emp_id, 'Projects'].values[0] >= 0:
                # Check if the updated projects count is greater than 0 and update EmployeeStatus accordingly
                if df.loc[df['EmpID'] == emp_id, 'Projects'].values[0] > 0:
                    df.loc[df['EmpID'] == emp_id, 'EmployeeStatus'] = 'Active'
                else:
                    # Set EmployeeStatus to 'Inactive' if projects become 0
                    df.loc[df['EmpID'] == emp_id, 'EmployeeStatus'] = 'Inactive'

                # Show the entire updated row
                st.text("Updated row:")
                st.dataframe(df[df['EmpID'] == emp_id])

                # You can also show the changes in each column
                st.text("Changes:")
                st.text(f"Projects Change: {old_row['Projects'].values[0]} -> {df.loc[df['EmpID'] == emp_id, 'Projects'].values[0]}")
                st.text(f"EmployeeStatus Change: {old_row['EmployeeStatus'].values[0]} -> {df.loc[df['EmpID'] == emp_id, 'EmployeeStatus'].values[0]}")

            else:
                st.warning("Project count cannot be less than 0. Please enter a valid count.")

        else:
            st.text(f"No employee found with EmpID {emp_id}.")

    # Save the updated DataFrame to the existing CSV file
    df.to_csv('employee_data.csv', index=False)

    st.success("Updated projects, EmployeeStatus, and ProjectDivision in the existing employee_data.csv for the specified EmpIDs.")

if __name__ == "__main__":
    set_page_config()
    style_app()
    st.title("Resourcify")

    if authenticate_user():
        user_input = process_input()

        if user_input:
            run_agent_with_input(user_input)
    else:
        st.error("Authentication failed. Exiting.")
