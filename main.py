
from flask import Flask, render_template, request, redirect, session, url_for, Response
import sqlite3
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for sessions

# ---------- Database Helpers ----------
def get_all_appointments():
    connection = sqlite3.connect("clinic.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, age, gender, phone, appointment_date, symptoms, summary, missing_fields FROM appointments")
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_reminders():
    connection = sqlite3.connect("clinic.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, appointment_date, symptoms FROM appointments")
    rows = cursor.fetchall()
    connection.close()

    reminders = []
    for row in rows:
        appt_date = None
        raw_date = row[2].strip() if row[2] else None

        try:
            # Try parsing with date+time
            appt_date = datetime.strptime(raw_date, "%Y-%m-%d %H:%M").date()
        except Exception:
            try:
                # Fallback: parse with only date
                appt_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
            except Exception:
                appt_date = None

        days_left = None
        if appt_date:
            today = datetime.today().date()
            days_left = (appt_date - today).days

        # Debug print to confirm values
        print(f"DEBUG: {row[1]} | {row[2]} | days_left={days_left}")

        reminders.append({
            "id": row[0],
            "name": row[1],
            "appointment_date": row[2],
            "symptoms": row[3],
            "days_left": days_left
        })
    return reminders

# ---------- Homepage ----------
@app.route("/")
def home():
    return render_template("home.html")

# ---------- AI Chatbot ----------
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.form["message"].lower()

    # Simple rule-based responses
    if "timing" in user_message:
        reply = "Our clinic is open from 9 AM to 6 PM, Monday to Saturday."
    elif "book" in user_message:
        reply = "You can book an appointment online via the booking page."
    elif "report" in user_message:
        reply = "Reports can be collected from the admin desk or downloaded as PDF."
    else:
        reply = "I'm here to help! Please ask about clinic timings, booking, or reports."

    # ✅ Reload homepage with chatbot reply
    return render_template("home.html", reply=reply)

# ---------- Patient Booking ----------
@app.route("/book")
def book():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    age = request.form["age"]
    gender = request.form["gender"]
    phone = request.form["phone"]
    appointment_date = request.form["appointment_date"]
    appointment_time = request.form.get("appointment_time")
    symptoms = request.form["symptoms"]

    if appointment_time:
        full_datetime = f"{appointment_date} {appointment_time}"
    else:
        full_datetime = appointment_date

    # Check if phone number already exists
    connection = sqlite3.connect("clinic.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM appointments WHERE phone=?", (phone,))
    existing = cursor.fetchone()
    if existing:
        connection.close()
        return render_template("result.html", summary=None, error="Number already exists. Please use a different phone number.")

    # Generate OTP for patient verification
    otp = str(random.randint(100000, 999999))
    session["patient_pending_otp"] = otp
    session["patient_data"] = {
        "name": name,
        "age": age,
        "gender": gender,
        "phone": phone,
        "appointment_date": full_datetime,
        "symptoms": symptoms
    }

    return render_template("patient_otp.html", otp=otp)

@app.route("/verify_patient_otp", methods=["POST"])
def verify_patient_otp():
    entered_otp = request.form["otp"]
    if "patient_pending_otp" in session and entered_otp == session["patient_pending_otp"]:
        data = session["patient_data"]
        summary = f"{data['name']} ({data['age']} years) booked an appointment on {data['appointment_date']}. Reported symptoms: {data['symptoms']}. [Online     Taken]"

        
        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO appointments (name, age, gender, phone, appointment_date, symptoms, summary, missing_fields, treatment_plan)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data["name"], data["age"], data["gender"], data["phone"], data["appointment_date"], data["symptoms"], summary, None, None))

        connection.commit()
        connection.close()

        # Clear session
        session.pop("patient_pending_otp", None)
        session.pop("patient_data", None)

        # ✅ Changed here: use appointment_confirmed.html instead of result.html
        return render_template("appointment_confirmed.html", summary=summary)

    # If OTP is invalid
    return render_template("patient_otp.html", summary=None, error="Invalid OTP. Please try again.")

# ---------- Admin Login with OTP ----------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            otp = str(random.randint(100000, 999999))
            session["pending_otp"] = otp
            session["otp_expiry"] = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
            session["resend_count"] = 0
            return render_template("otp.html", otp=otp)
        else:
            return "Invalid admin credentials. Try again."
    return render_template("login.html")

@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    entered_otp = request.form["otp"]
    if "pending_otp" in session:
        expiry = datetime.strptime(session["otp_expiry"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() > expiry:
            session.pop("pending_otp", None)
            session.pop("otp_expiry", None)
            return "OTP expired. Please login again."
        if entered_otp == session["pending_otp"]:
            session.pop("pending_otp", None)
            session.pop("otp_expiry", None)
            session.pop("resend_count", None)
            session["admin_id"] = 1
            return redirect(url_for("admin_dashboard"))
    return "Invalid OTP. Try again."

@app.route("/resend_otp", methods=["POST"])
def resend_otp():
    if "resend_count" not in session:
        session["resend_count"] = 0
    if session["resend_count"] >= 3:
        return "Resend limit reached. Please login again."

    otp = str(random.randint(100000, 999999))
    session["pending_otp"] = otp
    session["otp_expiry"] = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    session["resend_count"] += 1
    return render_template("otp.html", otp=otp)

# ---------- Admin Dashboard ----------
@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))
    return render_template("admin_dashboard.html")

@app.route("/appointments")
def appointments():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))
    return render_template("appointments.html", appointments=get_all_appointments())


@app.route("/view_doctor_advice")
def view_doctor_advice():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = sqlite3.connect("clinic.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, appointment_date, symptoms, treatment_plan FROM appointments ORDER BY appointment_date DESC")
    rows = cursor.fetchall()
    connection.close()

    return render_template("view_doctor_advice.html", advice=rows)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    connection = sqlite3.connect("clinic.db")
    cursor = connection.cursor()
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        appointment_date = request.form["appointment_date"]
        appointment_time = request.form.get("appointment_time")
        symptoms = request.form["symptoms"]

        if appointment_time:
            full_datetime = f"{appointment_date} {appointment_time}"
        else:
            full_datetime = appointment_date

        summary = f"{name} ({age} years) booked an appointment on {full_datetime}. Reported symptoms: {symptoms}."
        # ✅ Collect doctor's advice from edit.html
        treatment_plan = request.form.get("treatment_plan")

        # ✅ Update SQL to also save treatment_plan
        cursor.execute("""
            UPDATE appointments
            SET name=?, age=?, gender=?, phone=?, appointment_date=?, symptoms=?, summary=?, treatment_plan=?
            WHERE id=?
        """, (name, age, gender, phone, full_datetime, symptoms, summary, treatment_plan, id))

        connection.commit()
        connection.close()
        return redirect("/appointments")
    else:
        cursor.execute("SELECT * FROM appointments WHERE id=?", (id,))
        appointment = cursor.fetchone()
        connection.close()
        return render_template("edit.html", appointment=appointment)

@app.route("/delete/<int:id>")
def delete(id):
    connection = sqlite3.connect("clinic.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM appointments WHERE id=?", (id,))
    connection.commit()
    connection.close()
    return redirect("/appointments")

@app.route("/reminders")
def reminders():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))
    return render_template("reminders.html", reminders=get_reminders())

# ---------- CSV Export ----------
@app.route("/export_csv")
def export_csv():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = sqlite3.connect("clinic.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, age, gender, phone, appointment_date, symptoms, summary, missing_fields FROM appointments")
    rows = cursor.fetchall()
    connection.close()
def generate():
    header = ["id", "name", "age", "gender", "phone", "appointment_date", "appointment_time", "symptoms", "summary", "missing_fields"]
    yield ",".join(header) + "\n"
    for row in rows:
        # row[5] is appointment_date, which may include both date and time
        # Split into date and time parts for CSV clarity
        if row[5]:
            parts = row[5].split(" ")
            appt_date = parts[0]
            appt_time = parts[1] if len(parts) > 1 else ""
        else:
            appt_date = ""
            appt_time = ""

        # Build the row with appointment_date and appointment_time separated
        csv_row = [
            str(row[0]) if row[0] is not None else "",
            str(row[1]) if row[1] is not None else "",
            str(row[2]) if row[2] is not None else "",
            str(row[3]) if row[3] is not None else "",
            str(row[4]) if row[4] is not None else "",
            appt_date,
            appt_time,
            str(row[6]) if row[6] is not None else "",
            str(row[7]) if row[7] is not None else "",
            str(row[8]) if row[8] is not None else ""
        ]
        yield ",".join(csv_row) + "\n"

# ---------- Send Reminder ----------
@app.route("/send_reminder/<int:id>")
def send_reminder(id):
    connection = sqlite3.connect("clinic.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name, appointment_date FROM appointments WHERE id=?", (id,))
    row = cursor.fetchone()
    connection.close()

    if not row:
        return render_template("result.html", summary=None, error="Appointment not found")

    name, appt_datetime = row

    # Try parsing with date+time, fallback to date only
    try:
        appt_date = datetime.strptime(appt_datetime, "%Y-%m-%d %H:%M").date()
    except:
        appt_date = datetime.strptime(appt_datetime, "%Y-%m-%d").date()

    today = datetime.today().date()
    days_left = (appt_date - today).days

    # Decide message
    if days_left > 0:
        message = f"Reminder: Appointment for {name} is upcoming in {days_left} days on {appt_datetime}."
    elif days_left == 0:
        message = f"Reminder: Appointment for {name} is today ({appt_datetime})."
    else:
        message = f"Reminder: Appointment for {name} was overdue on {appt_datetime}. Please update with a new date."

    return render_template("reminder_message.html", message=message)

# ---------- Logout ----------
@app.route("/logout")
def logout():
    session.pop("admin_id", None)
    return redirect(url_for("home"))

# ---------- Mark Consultation Complete ----------
@app.route("/mark_consultation/<int:id>")
def mark_consultation(id):
    connection = sqlite3.connect("clinic.db")
    cursor = connection.cursor()
    cursor.execute("SELECT summary, treatment_plan FROM appointments WHERE id=?", (id,))
    row = cursor.fetchone()
    connection.close()

    if row:
        summary, treatment_plan = row
        return render_template("result.html", summary=summary, treatment_plan=treatment_plan, error=None, show_qr=True, appointment_id=id)

    else:
        return render_template("result.html", summary=None, error="Appointment not found")


# ---------- Submit Feedback ----------
@app.route("/submit_feedback/<int:appointment_id>", methods=["POST"])
def submit_feedback(appointment_id):
    rating = request.form.get("rating")
    comments = request.form.get("comments")

    connection = sqlite3.connect("clinic.db")
    cursor = connection.cursor()

    # Create feedback table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id INTEGER,
            rating INTEGER,
            comments TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("INSERT INTO feedback (appointment_id, rating, comments) VALUES (?, ?, ?)",
                   (appointment_id, rating, comments))
    connection.commit()
    connection.close()

    return render_template("thank_you.html")


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
