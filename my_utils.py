import gspread
from google.oauth2.service_account import Credentials

# Setup Google Sheets client
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", 
         "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"
SHEET_NAME = "labor_data"

try:
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
    client = gspread.authorize(creds)
    try:
        sheet = client.open(SHEET_NAME).sheet1
    except gspread.SpreadsheetNotFound:
        sheet = None
        print(f"Spreadsheet '{SHEET_NAME}' not found. Please share it with the service account.")
except Exception as e:
    sheet = None
    print("Error initializing Google Sheets client:", e)

def get_all_data():
    if not sheet:
        return []
    try:
        return sheet.get_all_records()
    except Exception as e:
        print("Error fetching data:", e)
        return []

def add_employee(employee_data):
    if not sheet:
        return {"status": "error", "message": "Spreadsheet not found."}
    try:
        row = [
            employee_data.get("Company", ""),
            employee_data.get("Name", ""),
            employee_data.get("Position", ""),
            employee_data.get("Expiry", ""),
            employee_data.get("Email", ""),
            employee_data.get("WhatsAppNumber", "")
        ]
        sheet.append_row(row)
        return {"status": "success", "message": "Employee added successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_employee(row_number, new_data):
    if not sheet:
        return {"status": "error", "message": "Spreadsheet not found."}
    try:
        sheet.update_cell(row_number, 1, new_data.get("Company", ""))
        sheet.update_cell(row_number, 2, new_data.get("Name", ""))
        sheet.update_cell(row_number, 3, new_data.get("Position", ""))
        sheet.update_cell(row_number, 4, new_data.get("Expiry", ""))
        sheet.update_cell(row_number, 5, new_data.get("Email", ""))
        sheet.update_cell(row_number, 6, new_data.get("WhatsAppNumber", ""))
        return {"status": "success", "message": "Employee updated successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
