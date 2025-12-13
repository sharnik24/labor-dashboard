from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime, timedelta
from my_utils import get_all_data, add_employee, update_employee

app = Flask(__name__)

# Dashboard route
@app.route("/")
def dashboard():
    all_employees = get_all_data()
    today = date.today()
    reminders = []

    # Check for employees expiring within 7 days
    for emp in all_employees:
        expiry_date = datetime.strptime(emp["Expiry"], "%Y-%m-%d").date()
        days_left = (expiry_date - today).days
        if 0 <= days_left <= 7:  # Reminder threshold
            reminders.append({
                "name": emp["Name"],
                "expiry": emp["Expiry"],
                "days_left": days_left
            })

    return render_template(
        "dashboard.html",
        all_employees=all_employees,
        today=today.isoformat(),
        reminders=reminders
    )

# Add new employee
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
        add_employee(data)
        return redirect(url_for("dashboard"))
    return render_template("form.html", data={}, action="Add")

# Edit employee
@app.route("/edit/<company>/<name>", methods=["GET", "POST"])
def edit_worker(company, name):
    all_employees = get_all_data()
    employee = next((emp for emp in all_employees if emp["Company"] == company and emp["Name"]_
