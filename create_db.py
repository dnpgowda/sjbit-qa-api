import sqlite3

conn = sqlite3.connect("sjbit.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS qa (
    question TEXT PRIMARY KEY,
    answer TEXT
)
""")

# Insert sample data
sample_data = [
    (
        "What courses are available in SJBIT?",
        "SJBIT offers CSE, ISE, ECE, EEE, Mechanical, Civil and MBA."
    ),
    (
        "Where is SJBIT located?",
        "SJBIT is located in Bengaluru, Karnataka."
    )
]

cursor.executemany(
    "INSERT OR IGNORE INTO qa VALUES (?, ?)",
    sample_data
)

conn.commit()
conn.close()

print("Database created successfully")