import sqlite3

# Connect to your database file
connection = sqlite3.connect("clinic.db")
cursor = connection.cursor()

# Add the new column for doctor's advice
cursor.execute("ALTER TABLE appointments ADD COLUMN treatment_plan TEXT;")

# Save changes and close
connection.commit()
connection.close()

print("Column 'treatment_plan' added successfully!")
