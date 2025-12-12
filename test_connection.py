# test_connection.py
from my_utils import get_sheet  # Import the function from my_utils.py

sheet = get_sheet()

# Get all values from the sheet (includes headers)
data = sheet.get_all_values()

if not data:
    print("No data found in the sheet!")
else:
    print("Data from the sheet:\n")

# Loop through rows and skip empty rows
for row in data:
    if any(cell.strip() for cell in row):  # Skip completely empty rows
        print(row)
