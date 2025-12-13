from flask import Flask, render_template, request, redirect, url_for
from my_utils import get_companies, get_employees_by_company, add_employee, get_reminder_employees

app = Flask(__name__)

@app.route("/")
def dashboard():
    company = request.args.get("company")  # optional
    companies = get_companies()
    if company:
        employees = get_employees_by_company(company)
    else:
        employees = []
    reminders = get_reminder_employees()
    return render_template("dashboard.html", companies=companies, selected_company=company, employees=employees, reminders=reminders)

@app.route("/add_employee", methods=["POST"])
def add_employee_route():
    company = request.form.get("company")
    name = request.form.get("name")
    position = request.form.get("position")
    expiry = request.form.get("expiry")
    status = request.form.get("status")
    email = request.form.get("email")
    whatsapp = request.form.get("whatsapp")

    add_employee(company, name, position, expiry, status, email, whatsapp)
    return redirect(url_for("dashboard", company=company))

if __name__ == "__main__":
    app.run(debug=True)
