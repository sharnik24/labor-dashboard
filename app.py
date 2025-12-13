from flask import Flask, render_template, request, redirect, url_for
from my_utils import (
    get_companies,
    get_employees_by_company,
    add_employee,
    get_employee_by_row,
    update_employee,
    get_reminder_employees,
    get_stats
)

app = Flask(__name__)


@app.route("/")
def dashboard():
    companies = get_companies()
    reminders = get_reminder_employees()
    stats = get_stats()
    return render_template(
        "dashboard.html",
        companies=companies,
        reminders=reminders,
        stats=stats
    )


@app.route("/employees/<company>")
def employee_table(company):
    employees = get_employees_by_company(company)
    return render_template(
        "employee_table.html",
        company=company,
        employees=employees
    )


@app.route("/add/<company>", methods=["GET", "POST"])
def add(company):
    if request.method == "POST":
        add_employee(
            request.form["company"],
            request.form["name"],
            request.form["position"],
            request.form["expiry"],
            request.form["status"],
            request.form["email"],
            request.form["whatsapp"]
        )
        return redirect(url_for("employee_table", company=company))

    return render_template("form.html", company=company)


@app.route("/edit/<int:row_id>", methods=["GET", "POST"])
def edit(row_id):
    emp = get_employee_by_row(row_id)

    if request.method == "POST":
        update_employee(row_id, request.form)
        return redirect(url_for("employee_table", company=emp["Company"]))

    return render_template("edit.html", emp=emp, row_id=row_id)


if __name__ == "__main__":
    app.run(debug=True)
