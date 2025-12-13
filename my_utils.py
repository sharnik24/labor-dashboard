import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets setup
SCOPE = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"  # Make sure this file is in your project root
SHEET_NAME = "labor_data"

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
except gspread.SpreadsheetNotFound:
    sheet = None
    print(f"ERROR: Spreadsheet '{SHEET_NAME}' not found or access not granted.")
except Exception as e:
    sheet = None
    print(f"ERROR: Could not open spreadsheet. Details: {e}")


def get_all_data():
    if not sheet:
        return []
    try:
        data = sheet.get_all_records()
        return data
    except Exception as e:
        print(f"ERROR: Failed to get data from sheet. Details: {e}")
        return []


def add_employee(employee_data):
    """
    employee_data = {
        "Company": "Company Name",
        "Name": "Employee Name",
        "Position": "Job Title",
        "Expiry": "YYYY-MM-DD",
        "Email": "email@example.com",
        "WhatsAppNumber": "971XXXXXXXXX"
    }
    """
    if not sheet:
        return {"status": "error", "message": "Spreadsheet not accessible"}

    try:
        # Append a new row
        row = [
            employee_data.get("Company", ""),
            employee_data.get("Name", ""),
            employee_data.get("Position", ""),
            employee_data.get("Expiry", ""),
            employee_data.get("Email", ""),
            employee_data.get("WhatsAppNumber", "")
        ]
        sheet.append_row(row)
        return {"status": "success", "message": "Employee added"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def update_employee(row_index, new_data):
    """
    row_index: the row number in the sheet (1-based)
    new_data: dictionary with keys matching column headers
    """
    if not sheet:
        return {"status": "error", "message": "Spreadsheet not accessible"}

    try:
        if "Company" in new_data:
            sheet.update_cell(row_index, 1, new_data["Company"])
        if "Name" in new_data:
            sheet.update_cell(row_index, 2, new_data["Name"])
        if "Position" in new_data:
            sheet.update_cell(row_index, 3, new_data["Position"])
        if "Expiry" in new_data:
            sheet.update_cell(row_index, 4, new_data["Expiry"])
        if "Email" in new_data:
            sheet.update_cell(row_index, 5, new_data["Email"])
        if "WhatsAppNumber" in new_data:
            sheet.update_cell(row_index, 6, new_data["WhatsAppNumber"])
        return {"status": "success", "message": "Employee updated"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
