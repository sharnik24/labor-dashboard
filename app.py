from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    all_employees = []  # Temporary empty list
    expiring = []       # Temporary empty list
    return render_template(
        "dashboard.html",
        all_employees=all_employees,
        expiring=expiring
    )

@app.route("/add")
def add_worker():
    return render_template("form.html")

@app.route("/edit")
def edit_worker():
    return render_template("edit.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
