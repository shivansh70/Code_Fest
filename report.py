import pandas as pd
import matplotlib.pyplot as plt

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
