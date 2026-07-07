# AI Powered Clinic Managment and Summary Intake🏥

An AI‑powered full‑stack web application built with Flask and SQLite that streamlines clinic management — including patient bookings with OTP verification, appointment scheduling, reminders, doctor consultation advice, and intelligent AI‑generated summaries.

---

## 🚀 Features
- **Patient Booking with OTP Verification**  
  Patients can book appointments online, verified via OTP.

- **Admin Dashboard**  
  Secure login with OTP for administrators to view and manage appointments.

- **Appointments Management**  
  Add, edit, delete, and mark consultations as complete.

- **Doctor’s Advice**  
  Doctors can add treatment plans and advice for patients.

- **Reminders System**  
  Upcoming appointments are displayed with days left, overdue/today status, and “Online Taken” badge for online bookings.

- **CSV Export**  
  Export all appointments to CSV for record keeping.

- **PDF Reports**  
  Generate patient reports in PDF format with appointment details and doctor’s advice.

- **Feedback Collection**  
  Patients can submit ratings and comments after consultation.

## 🤖 AI Integration
This project also includes **AI-powered features** to enhance clinic management:

- **Automatic Summarization**  
  When a patient books or edits an appointment, the system uses AI to generate a concise intake summary of their details and symptoms.

- **Smart Assistance for Doctors**  
  AI helps streamline patient records by providing structured summaries that can be used in consultation notes.

- **Future Scope**  
  Planned extensions include AI-driven analytics for patient trends, automated treatment suggestions, and intelligent reminders.

---

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS (custom UI)
- **Libraries**:  
  - `reportlab` (for PDF generation)  
  - `random`, `datetime` (for OTP and reminders)

## 📂 Project Structure
Clinic Project/
│── main.py                # Flask app
│── clinic.db               # SQLite database
│── templates/              # HTML templates
│   ├── home.html
│   ├── index.html
│   ├── patient_otp.html
│   ├── appointment_confirmed.html
│   ├── appointments.html
│   ├── reminders.html
│   ├── result.html
│   └── ...
│── static/                 # CSS, JS, images
│   └── style.css
│── generate_pdf.py          # Script to generate patient reports
│── README.md                # Project documentation

## Install Dependencies
pip install flask
pip install flask reportlab
pip install qrcode[pil]

## Run the commands
python genrate_pdf.py
python import_csv.py
python main.py

## Run in browser
http://127.0.0.1:5000/






