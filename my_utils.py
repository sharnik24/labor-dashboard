import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Google Sheets setup
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", 
         "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"
SHEET_NAME = "labor_data"

try:
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
except FileNotFoundError:
    sheet = None
    print(f"Credentials file '{CREDS_FILE}' not found.")
except gspread.SpreadsheetNotFound:
    sheet = None
    print(f"Spreadsheet '{SHEET_NAME}' not found. Share it with the service account.")
except Exception as e:
    sheet = None
    print("Error initializing Google Sheets:", e)

def get_all_data():
    if not sheet:
        return []
    try:
        data = sheet.get_all_records()
        for row in data:
            try:
                expiry_date = datetime.strptime(row.get("Expiry", ""), "%Y-%m-%d")
                row["Days Left"] = (expiry_date - datetime.now()).days
                row["Status"] = "Expired" if row["Days Left"] < 0 else "Active"
            except:
                row["Days Left"] = "-"
                row["Status"] = "Unknown"
        return data
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
