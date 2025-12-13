import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("labor_data").sheet1  # Sheet name: labor_data

def get_all_data():
    records = sheet.get_all_records()
    return records

def add_employee(data):
    row = [
        data["Company"],
        data["Name"],
        data["Position"],
        data["Expiry"],
        data["Email"],
        data["WhatsAppNumber"]
    ]
    sheet.append_row(row)

def update_em_
