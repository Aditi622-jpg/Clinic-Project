import sqlite3
from datetime import datetime, timedelta

def check_availability(date_str, limit=5):
    """Check if doctor is available on a given date."""
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date=?", (date_str,))
    count = cursor.fetchone()[0]
    conn.close()
    return count < limit  # True if available

def find_next_available(date_str, limit=5):
    """Find the next available date after the given one."""
    suggested_date = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)
    while True:
        if check_availability(suggested_date.strftime("%Y-%m-%d"), limit):
            return suggested_date.strftime("%Y-%m-%d")
        suggested_date += timedelta(days=1)

def reschedule_or_cancel(patient_id):
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    # Get patient appointment
    cursor.execute("SELECT appointment_date, name FROM appointments WHERE id=?", (patient_id,))
    row = cursor.fetchone()

    if not row:
        print("Patient not found")
        return

    old_date, name = row
    print(f"\n📅 Current appointment for {name}: {old_date}")

    # Ask patient choice
    choice = input("Do you want to [keep] the date, [reschedule], or [cancel]? ").strip().lower()

    if choice == "cancel":
        cursor.execute("DELETE FROM appointments WHERE id=?", (patient_id,))
        conn.commit()
        print(f"❌ Appointment for {name} on {old_date} has been cancelled.")

    elif choice == "reschedule":
        new_date = input("Enter new date (YYYY-MM-DD): ").strip()
        if check_availability(new_date):
            cursor.execute("UPDATE appointments SET appointment_date=? WHERE id=?", (new_date, patient_id))
            conn.commit()
            print(f"✅ Appointment for {name} rescheduled to {new_date}.")
        else:
            suggested = find_next_available(new_date)
            print(f"❌ Doctor not available on {new_date}. Suggested next available date: {suggested}")

    elif choice == "keep":
        if check_availability(old_date):
            print(f"✅ Doctor available on {old_date}. Appointment confirmed for {name}.")
        else:
            suggested = find_next_available(old_date)
            print(f"❌ Doctor not available on {old_date}. Suggested next available date: {suggested}")

    else:
        print("⚠️ Invalid choice. Please type 'keep', 'reschedule', or 'cancel'.")

    conn.close()


# 🔎 Example usage
patient_id = int(input("Enter patient ID to check: "))
reschedule_or_cancel(patient_id)

