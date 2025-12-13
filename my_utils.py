import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_sheet():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("labor_data").sheet1  # Make sure the sheet name is exactly "LaborData"
        return sheet
    except Exception as e:
        print("Error connecting to Google Sheet:", e)
        return None

def get_all_data():
    sheet = connect_sheet()
    if sheet is None:
        return []
    try:
        records = sheet.get_all_records()
        return records
    except Exception as e:
        print("Error reading data from sheet:", e)
        return []

def add_employee(data):
    sheet = connect_sheet()
    if sheet is None:
        print("Cannot add employee, sheet not connected")
        return
    try:
        sheet.append_row([
            data["Company"],
            data["Name"],
            data["Position"],
            data["Expiry"],
            data["Email"],
            data["WhatsAppNumber"]
        ])
    except Exception as e:
        print("Error adding employee:", e)
