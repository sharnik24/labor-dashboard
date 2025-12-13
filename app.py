from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date
from my_utils import get_all_data, add_employee, update_employee

app = Flask(__name__)

REMINDER_DAYS = 7


def process_employees():
    employees = get_all_data()
    today = date.today()

    company_map = {}
    reminders = []

    for emp in employees:
        expiry_date = datetime.strptime(emp["Expiry"], "%Y-%m-%d").date()
        days_left = (expiry_date - today).days

        if days_left < 0:
            status = "Expired"
        elif days_left <= REMINDER_DAYS:
            status = "Expiring Soon"
            reminders.append({
                **emp,
                "days_left": days_left
            })
        else:
            status = "Valid"

        emp["days_left"] = days_left
        emp["status"] = status

        company = emp["Company"]
        if company not in company_map:
            company_map[company] = []

        company_map[company].append(emp)

    return company_map, reminders


@app.route("/")
def dashboard():
    company_map, reminders = process_employees()

    return render_template(
        "dashboard.html",
        company_map=company_map,
        companies=company_map.keys(),
        reminders=reminders,
        selected_company=None
    )


@app.route("/company/<company_name>")
def company_view(company_name):
    company_map, reminders = process_employees()

    filtered_map = {
        company_name: company_map.get(company_name, [])
    }

    return render_template(
        "dashboard.html",
        company_map=filtered_map,
        companies=company_map.keys(),
        reminders=reminders,
        selected_company=company_name
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
        add_employee(data)
        return redirect(url_for("dashboard"))

    return render_template("form.html", data={}, action="Add")


@app.route("/edit/<company>/<name>", methods=["GET", "POST"])
def edit_worker(company, name):
    employees = get_all_data()
    employee = next(
        (e for e in employees if e["Company"] == company and e["Name"] == name),
        None
    )

    if not employee:
        return "Employee not found", 404

    if request.method == "POST":
        new_data = {
            "Company": request.form.get("company"),
            "Name": request.form.get("name"),
            "Position": request.form.get("position"),
            "Expiry": request.form.get("expiry"),
            "Email": request.form.get("email"),
            "WhatsAppNumber": request.form.get("whatsapp")
        }
        update_employee(company, name, new_data)
        return redirect(url_for("dashboard"))

    return render_template("form.html", data=employee, action="Edit")


if __name__ == "__main__":
    app.run(debug=True)
