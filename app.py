from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date

from my_utils import get_all_data, add_employee

app = Flask(__name__)

# ---------- DASHBOARD ----------
@app.route("/")
def dashboard():
    employees = get_all_data()
    today = date.today()

    # Calculate days left
    for emp in employees:
        expiry_date = datetime.strptime(emp["Expiry"], "%Y-%m-%d").date()
        emp["days_left"] = (expiry_date - today).days
        emp["status"] = "Expired" if emp["days_left"] < 0 else "Valid"

    # Companies list
    companies = sorted(set(emp["Company"] for emp in employees))

    # Expiring within 7 days
    reminders = [e for e in employees if 0 <= e["days_left"] <= 7]

    selected_company = request.args.get("company", "ALL")

    if selected_company != "ALL":
        employees = [e for e in employees if e["Company"] == selected_company]

    return render_template(
        "dashboard.html",
        employees=employees,
        companies=companies,
        reminders=reminders,
        selected_company=selected_company
    )

# ---------- ADD EMPLOYEE ----------
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data = {
            "Company": request.form["Company"],
            "Name": request.form["Name"],
            "Position": request.form["Position"],
            "Expiry": request.form["Expiry"],
            "Email": request.form["Email"],
            "WhatsAppNumber": request.form["WhatsAppNumber"]
        }
        add_employee(data)
        return redirect(url_for("dashboard"))

    return render_template("add_employee.html")


if __name__ == "__main__":
    app.run(debug=True)
