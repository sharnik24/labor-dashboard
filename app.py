import os
# app.py
from flask import Flask, render_template
from my_utils import get_all_data, get_expiring_soon
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# --- EMAIL SETTINGS ---
EMAIL_ADDRESS = os.environ.get("tusharr942@gmail.com")
EMAIL_PASSWORD = os.environ.get("qvwddaljszmaqijb")

def send_email_reminder(to_email, employee):
    msg = EmailMessage()
    msg['Subject'] = f"Labor Card Expiry Alert: {employee['Name']}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(
        f"Reminder: Labor card for {employee['Name']} ({employee['Position']}, {employee['Company']}) "
        f"is expiring on {employee['Expiry Date']}. Please renew before time."
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

@app.route('/')
def dashboard():
    all_employees = get_all_data()
    expiring = get_expiring_soon()
    
    # Send email reminders for those expiring soon
    for employee in expiring:
        send_email_reminder("boss_email@example.com", employee)
    
    return render_template("dashboard.html", all_employees=all_employees, expiring=expiring)

if __name__ == '__main__':
    app.run(debug=True)
