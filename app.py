from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime
from my_utils import get_all_data, add_employee, update_employee
from collections import defaultdict

app = Flask(__name__)

def days_left(expiry):
    exp_date = datetime.strptime(expiry, "%Y-%m-%d").date()
    return (exp_date - date.today()).days

@app.route("/")
def dashboard():
    all_data = get_all_data()

    reminders = []
    company_map = defaultdict(list)
    companies = set()

    for emp in all_data:
        emp["days_left"] = days_left(emp["Expiry"])
        companies.add(emp["Company"])

        if emp["days_left"] < 0:
            emp["status"] = "Expired"
        elif emp["days_left"] <= 7:
            emp["status"] = "Expiring Soon"
            reminders.append(emp)
        else:
            emp["status"] = "Valid"

        company_map[emp["Company"]].append(emp)

    return render_template(
        "dashboard.html",
        reminders=reminders,
        company_map=company_map,
        companies=sorted(companies),
        selected_company=None
    )

@app.route("/company/<company>")
def company_view(company):
    all_data = get_all_data()

    filtered = []
    reminders = []

    for emp in all_data:
        if emp["Company"] == company:
            emp["days_left"] = days_left(emp["Expiry"])

            if emp["days_left"] < 0:
                emp["status"] = "Expired"
            elif emp["days_left"] <= 7:
                emp["status"] = "Expiring Soon"
                reminders.append(emp)
            else:
                emp["status"] = "Valid"

            filtered.append(emp)

    return render_template(
        "dashboard.html",
        reminders=reminders,
        company_map={company: filtered},
        companies=[],
        selected_company=company
    )

@app.route("/add", methods=["GET", "POST"])
def add_worker():
    if request.method == "POST":
        add_employee({
            "Company": request.form["company"],
            "Name": request.form["name"],
            "Position": request.form["position"],
            "Expiry": request.form["expiry"],
            "Email": request.form["email"],
            "WhatsAppNumber": request.form["whatsapp"]
        })
        return redirect(url_for("dashboard"))
    return render_template("form.html", data={}, action="Add")

@app.route("/edit/<company>/<name>", methods=["GET", "POST"])
def edit_worker(company, name):
    all_data = get_all_data()
    emp = next(e for e in all_data if e["Company"] == company and e["Name"] == name)

    if request.method == "POST":
        update_employee(company, name, {
            "Company": request.form["company"],
            "Name": request.form["name"],
            "Position": request.form["position"],
            "Expiry": request.form["expiry"],
            "Email": request.form["email"],
            "WhatsAppNumber": request.form["whatsapp"]
        })
        return redirect(url_for("dashboard"))

    return render_template("form.html", data=emp, action="Edit")

if __name__ == "__main__":
    app.run(debug=True)
