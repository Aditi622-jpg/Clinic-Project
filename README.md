🏥 AI-Powered Clinic Management and Patient Intake Summary System

An AI-powered full-stack web application built using Flask and SQLite that streamlines clinic management. The system enables patients to book appointments with OTP verification, allows administrators to manage appointments efficiently, assists doctors with AI-generated patient intake summaries, and provides reporting, reminders, analytics, and patient feedback management.

---

✨ Features

👨‍⚕️ Patient Booking

- Book appointments online.
- OTP verification before confirming appointments.
- Secure storage of appointment details in the SQLite database.
- Automatic AI-generated patient intake summary.

🔐 Admin Dashboard

- Secure administrator login.
- View all appointments.
- Add, edit, and delete appointments.
- Mark consultations as completed.

🩺 Doctor Consultation

- View patient details.
- Review AI-generated intake summaries.
- Add treatment plans and doctor's advice.

⏰ Appointment Reminder System

- Display upcoming appointments with the number of days remaining.
- Highlight today's and overdue appointments.
- Show an "Online Taken" badge for online bookings.

📊 Dashboard Analytics

- Interactive daily appointment bar chart using Chart.js.
- Automatically counts appointments based on actual appointment dates stored in the database.

📄 Reports

- Export appointment records to CSV.
- Generate PDF patient reports containing appointment details and doctor's advice.
- QR code support for patient reports.

⭐ Feedback System

- Patients can submit ratings and comments after their consultation.
- Feedback is stored for future review and quality improvement.

🤖 SunnyBot AI Chatbot

- AI chatbot integrated into the homepage.
- Answers common patient questions.
- Assists users with bookings, clinic timings, appointments, and reports.

---

🤖 AI Integration

Automatic Patient Intake Summary

When a patient books or edits an appointment, the system automatically generates a structured summary of the patient's symptoms and information to assist doctors during consultation.

Smart Doctor Assistance

AI-generated summaries help doctors quickly understand patient cases and improve consultation efficiency.

---

🛠️ Tech Stack

Backend

- Python
- Flask

Frontend

- HTML
- CSS
- JavaScript
- Chart.js

Database

- SQLite

Python Libraries

- Flask
- ReportLab
- qrcode[pil]
- matplotlib
- random
- datetime

---

📂 Project Structure

Clinic-Project/
│
├── main.py
├── database.py
├── update_db.py
├── import_csv.py
├── reschedule.py
├── README.md
├── clinic.db
├── appointments.csv
│
├── templates/
│   ├── home.html
│   ├── index.html
│   ├── patient_otp.html
│   ├── appointment_confirmed.html
│   ├── appointments.html
│   ├── reminders.html
│   ├── result.html
│   └── ...
│
├── static/
│   ├── style.css
│   ├── script.js
│   ├── images/
│   └── ...
│
└── patient_report.pdf

---

🚀 Installation

1. Clone the Repository

git clone https://github.com/Aditi622-jpg/Clinic-Project.git
cd Clinic-Project

2. Install Dependencies

pip install flask
pip install reportlab
pip install qrcode[pil]
pip install matplotlib

---

▶️ Running the Project

Initialize the Database (if required)

python database.py

Import Sample Data (Optional)

python import_csv.py

Start the Flask Application

python main.py

After running the application, open your browser and visit:

http://127.0.0.1:5000

---

🔮 Future Scope

- AI-powered patient trend analysis.
- Intelligent appointment reminders.
- Automated treatment recommendations.
- Email and SMS notifications.
- Online payment integration.
- Multi-doctor and multi-clinic support.
- Cloud database deployment.
- Enhanced chatbot knowledge base.

---

🎓 Learning Outcomes

This project demonstrates:

- Full-stack web development using Flask.
- Database management using SQLite.
- OTP-based authentication.
- AI-assisted patient intake summarization.
- PDF and CSV report generation.
- Dashboard analytics using Chart.js.
- Real-world healthcare workflow implementation.

---

👩‍💻 Author

Aditi Bajpai

GitHub: https://github.com/Aditi622-jpg/Clinic-Project
