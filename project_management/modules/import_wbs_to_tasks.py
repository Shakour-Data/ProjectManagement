import json
import sqlite3
import os

DB_PATH = os.path.join('docs', 'project_management', 'project_management.db')
WBS_DATA_PATH = os.path.join('PM_JSON', 'user_inputs', 'detailed_wbs.json')
WBS_SCORES_PATH = os.path.join('docs', 'project_management', 'wbs_scores.json')

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_tasks_table(conn):
    """
    Recreate the tasks table with the updated schema:
    - id as TEXT primary key
    - title TEXT not null
    - level INTEGER
    - parent_id TEXT (nullable)
    - description TEXT
    - importance REAL
    - urgency REAL
    - status TEXT
    - progress REAL
    """
    cursor = conn.cursor()
    # Drop existing tasks table
    cursor.execute("DROP TABLE IF EXISTS tasks;")
    # Create new tasks table
    cursor.execute("""
    CREATE TABLE tasks (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        level INTEGER,
        parent_id TEXT,
        description TEXT,
        importance REAL DEFAULT 0,
        urgency REAL DEFAULT 0,
        status TEXT DEFAULT 'Not Started',
        progress REAL DEFAULT 0,
        FOREIGN KEY(parent_id) REFERENCES tasks(id)
    );
    """)
    conn.commit()

def load_json_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def insert_task(conn, task, parent_id=None):
    cursor = conn.cursor()
    task_id = task.get('id')
    title = task.get('title')
    level = task.get('level')
    description = task.get('description', '')  # optional
    # Insert task with default importance, urgency, status, progress
    cursor.execute("""
        INSERT INTO tasks (id, title, level, parent_id, description)
        VALUES (?, ?, ?, ?, ?)
    """, (task_id, title, level, parent_id, description))
    conn.commit()
    # Insert subtasks recursively
    subtasks = task.get('subtasks', [])
    for subtask in subtasks:
        insert_task(conn, subtask, parent_id=task_id)

def update_task_scores(conn, scores):
    cursor = conn.cursor()
    for task_id, score in scores.items():
        importance = score.get('importance', 0)
        urgency = score.get('urgency', 0)
        cursor.execute("""
            UPDATE tasks
            SET importance = ?, urgency = ?
            WHERE id = ?
        """, (importance, urgency, task_id))
    conn.commit()

def main():
    conn = connect_db()
    initialize_tasks_table(conn)
    wbs_data = load_json_file(WBS_DATA_PATH)
    wbs_scores = load_json_file(WBS_SCORES_PATH)
    # Insert tasks and subtasks
    for task in wbs_data:
        insert_task(conn, task)
    # Update importance and urgency scores
    update_task_scores(conn, wbs_scores)
    print("Tasks table has been updated from JSON files.")

if __name__ == "__main__":
    main()
