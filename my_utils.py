import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ------------------- GOOGLE SHEET SETUP -------------------
# Scope and credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Your Google Sheet name
SHEET_NAME = "labor_data"

# ------------------- GET ALL DATA -------------------
def get_all_data():
    try:
        sheet = client.open(SHEET_NAME).sheet1
        all_records = sheet.get_all_records()
        return all_records
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

# ------------------- ADD EMPLOYEE -------------------
def add_employee(data):
    try:
        sheet = client.open(SHEET_NAME).sheet1
        # Make sure the order matches the header in Google Sheet
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
        print(f"Error adding employee: {e}")
        return False

# ------------------- UPDATE EMPLOYEE -------------------
def update_employee(company, name, new_data):
    try:
        sheet = client.open(SHEET_NAME).sheet1
        all_records = sheet.get_all_records()
        for i, emp in enumerate(all_records, start=2):  # Start=2 because header is row 1
            if emp["Company"] == company and emp["Name"] == name:
                # Update each column
                sheet.update_cell(i, 1, new_data.get("Company", emp["Company"]))
                sheet.update_cell(i, 2, new_data.get("Name", emp["Name"]))
                sheet.update_cell(i, 3, new_data.get("Position", emp["Position"]))
                sheet.update_cell(i, 4, new_data.get("Expiry", emp["Expiry"]))
                sheet.update_cell(i, 5, new_data.get("Email", emp["Email"]))
                sheet.update_cell(i, 6, new_data.get("Wha
