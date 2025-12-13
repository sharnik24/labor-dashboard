from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime
from my_utils import get_all_data, add_employee, update_employee

app = Flask(__name__)

# Dashboard route
@app.route("/")
def dashboard():
    try:
        all_employees = get_all_data()
        today = date.today()
        reminders = []

        companies = sorted(list(set(emp["Company"] for emp in all_employees)))

        for emp in all_employees:
            expiry_str = emp.get("Expiry")
            try:
                expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
                days_left = (expiry_date - today).days
                emp["days_left"] = days_left

                if expiry_date < today:
                    emp["status"] = "Expired"
                elif 0 <= days_left <= 7:
                    emp["status"] = "Expiring Soon"
                    reminders.append({
                        "name": emp["Name"],
                        "company": emp["Company"],
                        "position": emp["Position"],
                        "expiry": expiry_str,
                        "days_left": days_left
                    })
                else:
                    emp["status"] = "Valid"

            except Exception as e:
                emp["days_left"] = "N/A"
                emp["status"] = "Invalid Date"
                print(f"Error parsing date for {emp.get('Name', 'Unknown')}: {e}")

        return render_template(
            "dashboard.html",
            all_employees=all_employees,
            today=today.isoformat(),
            reminders=reminders,
            companies=companies
        )

    except Exception as e:
        return f"Error in dashboard: {e}"


# Add new employee
@app.route("/add", methods=["GET", "POST"])
def add_worker():
    try:
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
    except Exception as e:
        return f"Error in add_worker: {e}"


# Edit employee
@app.route("/edit/<company>/<name>", methods=["GET", "POST"])
def edit_worker(company, name):
    try:
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

    except Exception as e:
        return f"Error in edit_worker: {e}"


if __name__ == "__main__":
    app.run(debug=True)
