import sqlite3


DB_PATH = "instance/task_management.db"


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


columns = [
    ("description", "TEXT"),
    ("priority", "TEXT DEFAULT 'Medium'"),
    ("deadline", "TEXT"),
    ("status", "TEXT DEFAULT 'Pending'"),
    ("completed", "INTEGER DEFAULT 0"),
    ("created_at", "TEXT"),
    ("updated_at", "TEXT")
]


for column_name, column_type in columns:

    try:

        cursor.execute(
            f"ALTER TABLE task ADD COLUMN {column_name} {column_type}"
        )

        print(f"Added task column: {column_name}")

    except sqlite3.OperationalError:

        print(f"Already exists: {column_name}")



cursor.execute("""
CREATE TABLE IF NOT EXISTS task_step (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    task_id INTEGER NOT NULL,

    step_number INTEGER NOT NULL,

    title TEXT NOT NULL,

    completed INTEGER DEFAULT 0 NOT NULL,

    completed_at TEXT,

    created_at TEXT,

    FOREIGN KEY (task_id)
        REFERENCES task(id)
        ON DELETE CASCADE
)
""")


print("TaskStep table ready!")


conn.commit()
conn.close()


print("Database upgrade completed!")