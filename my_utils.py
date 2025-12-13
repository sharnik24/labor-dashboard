import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---- Setup Google Sheets connection ----
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Replace with your Google Sheet name
SHEET_NAME = "LaborData"
sheet = client.open(SHEET_NAME).sheet1

# ---- Get all employees ----
def get_all_data():
    try:
        records = sheet.get_all_records()
        return records
    except Exception as e:
        print("Error in get_all_data:", e)
        return []

# ---- Add new employee ----
def add_employee(data):
    try:
        # Order: Company, Name, Position, Expiry, Email, WhatsAppNumber
        row = [
            data.get("Company", ""),
            data.get("Name", ""),
            data.get("Position", ""),
            data.get("Expiry", ""),
            data.get("Email", ""),
            data.get("WhatsAppNumber", "")
        ]
        sheet.append_row(row)
        return True
    except Exception as e:
        print("Error in add_employee:", e)
        return False

# ---- Update existing employee ----
def update_employee(company, name, new_data):
    try:
        all_data = sheet.get_all_records()
        for i, emp in enumerate(all_data, start=2):  # start=2 because Google Sheets includes header
            if emp["Company"] == company and emp["Name"] == name:
                # Update each column
                sheet.update_cell(i, 1, new_data.get("Company", emp["Company"]))
                sheet.update_cell(i, 2, new_data.get("Name", emp["Name"]))
                sheet.update_cell(i, 3, new_data.get("Position", emp["Position"]))
                sheet.update_cell(i, 4, new_data.get("Expiry", emp["Expiry"]))
                sheet.update_cell(i, 5, new_data.get("Email", emp["Email"]))
                sheet.update_cell(i, 6, new_data.get("WhatsAppNumber", emp["WhatsAppNumber"]))
                return True
        return False
    except Exception as e:
        print("Error in update_employee:", e)
        return False
