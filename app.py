from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime
from my_utils import get_all_data, add_employee, update_employee

app = Flask(__name__)

@app.route("/")
def dashboard():
    try:
        all_employees = get_all_data()
        today = date.today()
        
        # Prepare reminders
        reminders = []
        for emp in all_employees:
            expiry_date = datetime.strptime(emp['Expiry'], "%Y-%m-%d").date()
            days_left = (expiry_date - today).days
            if days_left <= 7:
                reminders.append({
                    "Name": emp['Name'],
                    "Position": emp['Position'],
                    "Company": emp['Company'],
                    "Expiry": emp['Expiry'],
                    "DaysLeft": days_left
                })
        
        # Get unique company list
        companies = sorted(list({emp['Company'] for emp in all_employees}))
        
        return render_template(
            "dashboard.html",
            all_employees=all_employees,
            reminders=reminders,
            companies=companies,
            today=today
        )
    except Exception as e:
        return f"Error: {e}"

@app.route("/company/<company_name>")
def company_view(company_name):
    all_employees = get_all_data()
    company_employees = [emp for emp in all_employees if emp['Company'] == company_name]
    return render_template(
        "company.html",
        employees=company_employees,
        company_name=company_name
    )

@app.route("/add", methods=["GET", "POST"])
def add_worker():
    if request.method == "POST":
        data = {
            "Company": request.form.get("company"),
            "Name": request.form.get("name"),
            "Position": request.form.get("position"),
            "Expiry": request.form.get("expiry"),
            "Email": request.form.get("email"),
            "WhatsAppNumber": request.form.get("whatsapp")
        }
