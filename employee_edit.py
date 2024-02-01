import csv
import os

csv_file_path = os.path.abspath("employee_data.csv")

# Read the CSV file into a list of dictionaries
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Ask the user for input
department_to_edit = input("Enter the department: ")
empid_to_edit = input("Enter the empid: ")
new_status = input("Enter the new employee status: ")

# Update the specified column in the data list
for record in data:
    if 'EmpID' in record and record['DepartmentType'] == department_to_edit and record['EmpID'] == empid_to_edit:
        record['EmployeeStatus'] = new_status

# Write the updated data back to the CSV file
with open(csv_file_path, 'w', newline='') as file:
    fieldnames = ['EmpID', 'FirstName', 'LastName', 'ProjectStartDate', 'ProjectExitDate', 'Title', 'Supervisor', 'ADEmail', 'BusinessUnit', 'EmployeeStatus', 'EmployeeType', 'PayZone', 'EmployeeClassificationType', 'TerminationType', 'TerminationDescription', 'DepartmentType', 'Division', 'DOB', 'State', 'JobFunctionDescription', 'GenderCode', 'LocationCode', 'RaceDesc', 'MaritalDesc', 'Performance Score', 'Current Employee Rating']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Employee status in department {department_to_edit} with empid {empid_to_edit} updated to {new_status} in {csv_file_path}")