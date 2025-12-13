# my_utils.py
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAME = "labor_data"

def get_sheet():
    creds = Credentials.from_service_account_file("/etc/secrets/credentials.json", scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open(SHEET_NAME)
    worksheet = sh.sheet1
    return worksheet

def get_all_data():
    worksheet = get_sheet()
    data = worksheet.get_all_records()
    return data

def get_expiring_soon(days=6):
    data = get_all_data()
    expiring = []
    today = datetime.today().date()
    for row in data:
        expiry_str = row.get("Expiry Date")  # Column in your sheet
        if expiry_str:
            expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
            if 0 <= (expiry_date - today).days <= days:
                expiring.append(row)
    return expiring

