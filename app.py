from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime
from my_utils import get_all_data, add_employee, update_employee

app = Flask(__name__)

# ------------------- DASHBOARD -------------------
@app.route("/")
def dashboard():
    try:
        all_employees = get_all_data()

        # Calculate days left and check expiry
        today = date.today()
        for emp in all_employees:
            expiry_date = datetime.strptime(emp["Expiry"], "%Y-%m-%d").date()
            emp["DaysLeft"] = (expiry_date - today).days
            emp["Status"] = "Expired" if emp["DaysLeft"] < 0 else "Expiring Soon" if emp["DaysLeft"] <= 7 else "Valid"

        # List of unique companies
        companies = sorted(set(emp["Company"] for emp in all_employees))

        # Optional filter by company
        selected_company = request.args.get("company")
        if selected_company:
            filtered_employees = [emp for emp in all_employees if emp["Company"] == selected_company]
        else:
            filtered_employees = all_employees

        return render_template(
            "dashboard.html",
            employees=filtered_employees,
            companies=companies,
            selected_company=selected_company
        )
    except Exception as e:
        return f"Error loading dashboard: {e}", 500

# ------------------- ADD EMPLOYEE -------------------
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        try:
            data = {
                "Company": request.form.get("Company", "").strip(),
                "Name": request.form.get("Name", "").strip(),
                "Position": request.form.get("Position", "").strip(),
                "Expiry": request.form.get("Expiry", "").strip(),
                "Email": request.form.get("Email", "").strip(),
                "WhatsAppNumber": request.form.get("WhatsAppNumber", "").strip()
            }

            # Validation
            if not data["Company"] or not data["]()
