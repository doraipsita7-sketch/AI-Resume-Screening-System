import sqlite3
#===============================CONNECT DB==============================
conn = sqlite3.connect("resume.db", check_same_thread=False)

cursor = conn.cursor()

def save_candidate(email, phone, skills, score, status, job_role):
    cursor.execute("""
    INSERT INTO candidates
    (email, phone, skills, score, status, job_role)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        email,
        phone,
        skills,
        score,
        status,
        job_role
    ))
    conn.commit()


#===================CLEAR DATABASE FUNCTION================
def clear_database():
    cursor.execute("DELETE FROM candidates")
    conn.commit()
#=============================TABLE CREATE=================
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    phone TEXT,
    skills TEXT,
    score INTEGER,
    status TEXT,
    job_role TEXT
  
)
""")

conn.commit()