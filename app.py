from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date
from my_utils import get_all_data, add_employee, update_employee

app = Flask(__name__)

@app.route("/")
def dashboard():
    employees = get_all_data()
    today = date.today()

    for emp in employees:
        expiry = datetime.strptime(emp["Expiry"], "%Y-%m-%d").date()
        emp["days_left"] = (expiry - today).days
        emp["status"] = "Expired" if emp["days_left"] < 0 else "Valid"

    companies = sorted(set(e["Company"] for e in employees))

    selected_company = request.args.get("company")

    if selected_company:
        employees = [e for e in employees if e["Company"] == selected_company]

    reminders = [e for e in employees if 0 <= e["days_left"] <= 7]

    return render_template(
        "dashboard.html",
        employees=employees,
        companies=companies,
        selected_company=selected_company,
        reminders=reminders
    )


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

    company = request.args.get("company")
    return render_template("add_employee.html", company=company)


@app.route("/edit/<company>/<name>", methods=["GET", "POST"])
def edit(company, name):
    employees = get_all_data()
    emp = next(e for e in employees if e["Company"] == company and e["Name"] == name)

    if request.method == "POST":
        new_data = {
            "Company": request.form["Company"],
            "Name": request.form["Name"],
            "Position": request.form["Position"],
            "Expiry": request.form["Expiry"],
            "Email": request.form["Email"],
            "WhatsAppNumber": request.form["WhatsAppNumber"]
        }
        update_employee(company, name, new_data)
        return redirect(url_for("dashboard", company=new_data["Company"]))

    return render_template("add_employee.html", company=company, emp=emp)


if __name__ == "__main__":
    app.run(debug=True)
