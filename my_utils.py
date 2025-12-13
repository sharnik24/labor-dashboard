import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

SHEET_NAME = "labor_data"  # your Google Sheet name

def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet

def get_all_data():
    sheet = connect_sheet()
    data = sheet.get_all_records()
    # Optional: convert expiry to datetime object
    for row in data:
        row["Expiry"] = row["Expiry"]
    return data

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

def update_employee(old_company, old_name, new_data):
    sheet = connect_sheet()
    all_records = sheet.get_all_records()
    for i, row in enumerate(all_records):
        if row["Company"] == old_company and row["Name"] == old_name:
            row_number = i + 2  # 1-indexed + header row
            sheet.update(f"A{row_number}", [[
                new_data["Company"],
                new_data["Name"],
                new_data["Position"],
                new_data["Expiry"],
                new_data["Email"],
                new_data["WhatsAppNumber"]
            ]])
            return True
    return False
