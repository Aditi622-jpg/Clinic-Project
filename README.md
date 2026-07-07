# AI Powered Clinic Managment and Summary Intake🏥
An AI‑powered full‑stack web application built with Flask and SQLite that streamlines clinic management — including patient bookings with OTP verification, appointment scheduling, reminders, doctor consultation advice, and intelligent AI‑generated summaries.
---
## Features
Patient Booking with OTP Verification  
Patients can book appointments online, verified via OTP.

## Admin Dashboard  
Secure login with OTP for administrators to view and manage appointments.

## Appointments Management  
Add, edit, delete, and mark consultations as complete.

## Doctor’s Advice  
Doctors can add treatment plans and advice for patients.

## Reminders System  
Upcoming appointments are displayed with days left, overdue/today status, and “Online Taken” badge for online bookings.

## CSV Export  
Export all appointments to CSV for record keeping.

## PDF Reports  
Generate patient reports in PDF format with appointment details and doctor’s advice.

## Feedback Collection  
Patients can submit ratings and comments after consultation.

## Daily Appointments Chart  
A dynamic bar chart is displayed in the admin appointments view, automatically counting appointments per real date from the database.

## 🤖 AI Integration
Automatic Summarization  
When a patient books or edits an appointment, the system uses AI to generate a concise intake summary of their details and symptoms.

## Smart Assistance for Doctors  
AI helps streamline patient records by providing structured summaries that can be used in consultation notes.

## 🔮 Future Scope
Planned extensions include AI‑driven analytics for patient trends, automated treatment suggestions, and intelligent reminders.

## 🛠️ Tech Stack
Backend: Flask (Python)

Database: SQLite

Frontend: HTML, CSS (custom UI)

Libraries:

reportlab (for PDF generation)

random, datetime (for OTP and reminders)

chart.js (for interactive appointment charts)

## 📂 Project Structure
Code
Clinic Project/
│── main.py                # Flask app
│── clinic.db              # SQLite database
│── templates/             # HTML templates
│   ├── home.html
│   ├── index.html
│   ├── patient_otp.html
│   ├── appointment_confirmed.html
│   ├── appointments.html  # Includes dynamic chart
│   ├── reminders.html
│   ├── result.html
│   └── ...
│── static/                # CSS, JS, images
│   └── style.css
│── generate_pdf.py        # Script to generate patient reports
│── README.md              # Project documentation

## ⚙️ Install Dependencies
bash
pip install flask
pip install reportlab
pip install qrcode[pil]
pip install matplotlib
pip install seaborn

## ▶️ Run the commands
python generate_pdf.py
python import_csv.py
python main.py

## 🌐 Run in browser
Code
http://127.0.0.1:5000/
