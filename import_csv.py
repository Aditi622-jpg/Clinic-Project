import sqlite3
import csv

connection = sqlite3.connect("clinic.db")
cursor = connection.cursor()

with open("appointments.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Combine date and time into one string for storage
        if row.get("appointment_time"):
            full_datetime = f"{row['appointment_date']} {row['appointment_time']}"
        else:
            full_datetime = row["appointment_date"]

        cursor.execute("""
        INSERT INTO appointments
        (name, age, gender, phone, appointment_date,
         symptoms, summary, missing_fields)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["name"],
            row["age"],
            row["gender"],
            row["phone"],
            full_datetime,
            row["symptoms"],
            row["summary"],
            row["missing_fields"]
        ))

connection.commit()
connection.close()

print("CSV data with date & time imported successfully!")
