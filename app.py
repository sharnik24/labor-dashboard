from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from my_utils import get_all_data, add_employee, update_employee

app = Flask(__name__)

@app.route("/")
def dashboard():
    all_employees = get_all_data()
    today = date.today().isoformat()
    return render_template("dashboard.html", all_employees=all_employees, today=today)

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
    all_employees = get_all_data()
    employee = next((emp for emp in all_employees if emp["Company"] == company and emp["Name"] == name), None)
    if not employee:
        return "Employee not found"

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
