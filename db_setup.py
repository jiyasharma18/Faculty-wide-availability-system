import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect("faculty.db")
cursor = conn.cursor()

# Delete old table (so structure stays correct)
cursor.execute("DROP TABLE IF EXISTS faculty_status")

# Create new table
cursor.execute("""
CREATE TABLE faculty_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    cabin TEXT NOT NULL,
    status TEXT,
    last_seen TEXT
)
""")

# Insert sample data
faculty_data = [
    ("Dr. Mehta", "CSE", "A-101", "Not Present", "-"),
    ("Dr. Iyer", "ECE", "B-202", "Not Present", "-"),
    ("Dr. Sharma", "IT", "C-303", "Not Present", "-"),
    ("Dr. Patil", "MECH", "D-404", "Not Present", "-")
]

cursor.executemany("""
INSERT INTO faculty_status (name, department, cabin, status, last_seen)
VALUES (?, ?, ?, ?, ?)
""", faculty_data)

# Save changes
conn.commit()
conn.close()

print("Database created successfully with sample data")