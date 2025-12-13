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
    return sheet.get_all_records()


def get_companies():
    return sorted({row["Company"] for row in get_all_data()})


def get_employees_by_company(company):
    records = sheet.get_all_records()
    return [
        dict(row, _row=i + 2)
        for i, row in enumerate(records)
        if row["Company"] == company
    ]


# ✅ THIS FUNCTION FIXES YOUR ERROR
def get_employee_by_row(row_id):
    headers = sheet.row_values(1)
    values = sheet.row_values(row_id)

    if not values:
        return None

    return dict(zip(headers, values))


def add_employee(company, name, position, expiry, status, email, whatsapp):
    sheet.append_row([
        company, name, position, expiry, status, email, whatsapp
    ])


def update_employee(row_id, data):
    sheet.update(f"A{row_id}:G{row_id}", [[
        data["company"],
        data["name"],
        data["position"],
        data["expiry"],
        data["status"],
        data["email"],
        data["whatsapp"]
    ]])


# ===== DASHBOARD =====
def get_reminder_employees():
    today = datetime.today().date()
    reminders = []

    for row in get_all_data():
        try:
            expiry = datetime.strptime(row["Expiry"], "%Y-%m-%d").date()
            days_left = (expiry - today).days
            if days_left <= 30:
                reminders.append({
                    "Name": row["Name"],
                    "Company": row["Company"],
                    "Expiry": row["Expiry"],
                    "DaysLeft": days_left
                })
        except:
            pass

    return reminders


def get_stats():
    data = get_all_data()
    return {
        "total_employees": len(data),
        "total_companies": len({r["Company"] for r in data}),
        "expiring_soon": len(get_reminder_employees())
    }
