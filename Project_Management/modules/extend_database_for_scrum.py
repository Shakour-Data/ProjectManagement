import sqlite3
import os

DB_PATH = os.path.join('docs', 'project_management', 'project_management.db')

def connect_db():
    return sqlite3.connect(DB_PATH)

def extend_schema_for_scrum(conn):
    cursor = conn.cursor()
    # Create sprints table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sprints (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT,
        goal TEXT,
        status TEXT DEFAULT 'Planned'
    );
    """)
    # Create backlog_items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS backlog_items (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        sprint_id TEXT,
        status TEXT DEFAULT 'To Do',
        priority INTEGER DEFAULT 0,
        created_at TEXT,
        updated_at TEXT,
        FOREIGN KEY(sprint_id) REFERENCES sprints(id)
    );
    """)
    # Create burndown_data table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS burndown_data (
        sprint_id TEXT,
        date TEXT,
        remaining_work REAL,
        PRIMARY KEY (sprint_id, date),
        FOREIGN KEY(sprint_id) REFERENCES sprints(id)
    );
    """)
    conn.commit()

def main():
    conn = connect_db()
    extend_schema_for_scrum(conn)
    print("Extended database schema with Scrum-specific tables.")

if __name__ == "__main__":
    main()
