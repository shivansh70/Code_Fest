import csv

# Define the CSV file path
csv_file_path = "employee_data.csv"

# Read the CSV file into a list of dictionaries
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Ask the user for input
column_to_edit = input("Enter the column you want to edit: ")
old_value = input(f"Enter the current value in {column_to_edit}: ")
new_value = input("Enter the new value: ")

# Update the specified column in the data list
for record in data:
    if record[column_to_edit] == old_value:
        record[column_to_edit] = new_value

# Write the updated data back to the CSV file
with open(csv_file_path, 'w', newline='') as file:
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"{column_to_edit} with value {old_value} updated to {new_value} in {csv_file_path}")
