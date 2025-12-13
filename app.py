# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    # TEMPORARY DUMMY DATA (to avoid crashes)
    all_employees = []
    expiring = []

    return render_template(
        "dashboard.html",
        all_employees=all_employees,
        expiring=expiring
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
