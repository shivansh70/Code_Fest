import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('employee_data.csv')

# Take user input for the number of EmpIDs to change
num_empids = int(input("Enter the number of EmpIDs you want to change: "))

for _ in range(num_empids):
    # Take user input for EmpID
    emp_id = int(input("Enter EmpID: "))

    # Find the employee in the DataFrame
    employee = df[df['EmpID'] == emp_id]

    if not employee.empty:
        # Display current projects for the selected employee
        print(f"Current projects for EmpID {emp_id}: {employee['Projects'].values[0]}")

        # Check if the current projects count is zero before allowing decrease
        if employee['Projects'].values[0] == 0:
            action = 'add'
        else:
            # Ask the user whether to add or decrease projects
            action = input("Do you want to add or decrease projects? (Type 'add' or 'decrease'): ").lower()

        # Take user input for the number of projects to add or decrease
        project_change = int(input("Enter the number of projects to add or decrease: "))

        # Update the number of projects based on user input
        if action == 'add':
            df.loc[df['EmpID'] == emp_id, 'Projects'] += project_change
        elif action == 'decrease':
            df.loc[df['EmpID'] == emp_id, 'Projects'] -= project_change

        # Check if the updated projects count is greater than 0 and update EmployeeStatus accordingly
        if df.loc[df['EmpID'] == emp_id, 'Projects'].values[0] > 0:
            df.loc[df['EmpID'] == emp_id, 'EmployeeStatus'] = 'Active'
            # Reset ProjectDivision if projects are greater than 0 and status is made active
            df.loc[df['EmpID'] == emp_id, 'ProjectDivision'] = ''
        else:
            # Set EmployeeStatus to 'Inactive' if projects become 0
            df.loc[df['EmpID'] == emp_id, 'EmployeeStatus'] = 'Inactive'

            # Ask for project division name if the employee status is inactive
            project_division = input("Enter the project division name: ")
            df.loc[df['EmpID'] == emp_id, 'ProjectDivision'] = project_division

    else:
        print(f"No employee found with EmpID {emp_id}.")

# Save the updated DataFrame to the existing CSV file
df.to_csv('employee_data.csv', index=False)

print("Updated projects, EmployeeStatus in the existing employee_data.csv for the specified EmpIDs.")