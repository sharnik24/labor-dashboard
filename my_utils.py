import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Connect to Google Sheet
def connect_sheet():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("labor_data").sheet1  # Make sure your sheet name matches
    return sheet

# Get all employees
def get_all_data():
    sheet = connect_sheet()
    records = sheet.get_all_records()  # Returns a list of dicts
    return records

# Add new employee
def add_employee(data):
    sheet = connect_sheet()
    sheet.append_row([
        data["Company"],
        data["Name"],
        data["Position"],
        data["Expiry"],
        data["Email"],
        data["WhatsAppNumber"]
    ])

