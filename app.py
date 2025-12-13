from flask import Flask, render_template, request, redirect, url_for
from my_utils import get_all_data, add_employee

app = Flask(__name__)

@app.route("/")
def dashboard():
    all_employees = get_all_data()
    print("Dashboard data:", all_employees)  # debug print
    return render_template("dashboard.html", all_employees=all_employees, expiring=[])

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
        print("Adding employee:", data)  # debug print
        add_employee(data)
        return redirect(url_for("dashboard"))
    return render_template("form.html")

@app.route("/edit")
def edit_worker():
    return render_template("edit.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
