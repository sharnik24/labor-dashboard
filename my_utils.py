import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets setup
SHEET_NAME = "labor_data"
CREDENTIALS_FILE = "credentials.json"  # Path to your Google service account JSON

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(credentials)
sheet = client.open(SHEET_NAME).sheet1

def get_all_data():
    """Fetch all rows from the sheet"""
    records = sheet.get_all_records()  # returns list of dicts
    return records

def get_companies():
    """Get unique company names"""
    records = get_all_data()
    companies = list({row['Company'] for row in records})
    return sorted(companies)

def get_employees_by_company(company_name):
    """Return employees for a given company"""
    records = get_all_data()
    employees = [row for row in records if row['Company'] == company_name]
    return employees

def add_employee(company_name, name, position, expiry, status, email, whatsapp):
    """Add new employee to the sheet"""
    # Append to the sheet
    new_row = [company_name, name, position, expiry, status, email, whatsapp]
    sheet.append_row(new_row)
    return True

def update_employee(row_index, new_data):
    """Update employee at row_index (1-based)"""
    # row_index = index in sheet (starting from 2 if header row is 1)
    sheet.update_cell(row_index, 2, new_data.get("Name", ""))
    sheet.update_cell(row_index, 3, new_data.get("Position", ""))
    sheet.update_cell(row_index, 4, new_data.get("Expiry", ""))
    sheet.update_cell(row_index, 5, new_data.get("Status", ""))
    sheet.update_cell(row_index, 6, new_data.get("Email", ""))
    sheet.update_cell(row_index, 7, new_data.get("WhatsApp", ""))
    return True

def get_reminder_employees():
    """Employees whose expiry is within 30 days"""
    today = datetime.today().date()
    reminder_list = []
    records = get_all_data()
    for row in records:
        try:
            expiry_date = datetime.strptime(row['Expiry'], "%Y-%m-%d").date()
            days_left = (expiry_date - today).days
            if days_left <= 30:
                reminder_list.append({
                    "Name": row['Name'],
                    "Position": row['Position'],
                    "Expiry": row['Expiry'],
                    "DaysLeft": days_left
                })
        except:
            continue
    return reminder_list
