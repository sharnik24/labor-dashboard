import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ===== CONFIG =====
SHEET_NAME = "labor_data"
CREDENTIALS_FILE = "credentials.json"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE, scope
)
client = gspread.authorize(credentials)
sheet = client.open(SHEET_NAME).sheet1

# ===== CORE =====
def get_all_data():
    """Fetch all rows from the sheet"""
    return sheet.get_all_records()

def get_companies():
    """Get unique, stripped company names"""
    records = get_all_data()
    companies = {row["Company"].strip() for row in records if row["Company"].strip()}
    return sorted(companies)

def get_employees_by_company(company):
    """Return employees for a given company (stripped for exact match)"""
    company = company.strip()
    records = get_all_data()
    return [
        dict(row, _row=i + 2)
        for i, row in enumerate(records)
        if row["Company"].strip() == company
    ]

def get_employee_by_row(row_id):
    """Get employee data by sheet row index"""
    headers = sheet.row_values(1)
    values = sheet.row_values(row_id)
    if not values:
        return None
    return dict(zip(headers, values))

def add_employee(company, name, position, expiry, status, email, whatsapp):
    """Add new employee (all values stripped)"""
    sheet.append_row([
        company.strip(),
        name.strip(),
        position.strip(),
        expiry.strip(),
        status.strip(),
        email.strip(),
        whatsapp.strip()
    ])

def update_employee(row_id, data):
    """Update employee row with stripped values"""
    sheet.update(f"A{row_id}:G{row_id}", [[
        data["company"].strip(),
        data["name"].strip(),
        data["position"].strip(),
        data["expiry"].strip(),
        data["status"].strip(),
        data["email"].strip(),
        data["whatsapp"].strip()
    ]])

# ===== DASHBOARD =====
def get_reminder_employees():
    """Employees whose expiry is within 30 days"""
    today = datetime.today().date()
    reminders = []
    for row in get_all_data():
        try:
            expiry = datetime.strptime(row["Expiry"].strip(), "%Y-%m-%d").date()
            days_left = (expiry - today).days
            if days_left <= 30:
                reminders.append({
                    "Name": row["Name"].strip(),
                    "Company": row["Company"].strip(),
                    "Expiry": row["Expiry"].strip(),
                    "DaysLeft": days_left
                })
        except:
            continue
    return reminders

def get_stats():
    """Dashboard stats"""
    data = get_all_data()
    return {
        "total_employees": len(data),
        "total_companies": len({r["Company"].strip() for r in data if r["Company"].strip()}),
        "expiring_soon": len(get_reminder_employees())
    }
