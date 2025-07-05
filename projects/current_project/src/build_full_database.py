import json
import sqlite3
import os

DB_PATH = os.path.join('docs', 'project_management', 'project_management.db')
WBS_DATA_PATH = os.path.join('docs', 'project_management', 'wbs_data.json')
WBS_SCORES_PATH = os.path.join('docs', 'project_management', 'wbs_scores.json')

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def drop_tables(conn):
    cursor = conn.cursor()
    tables = ['tasks', 'importance_features', 'urgency_features', 'task_progress', 'resource_allocation']
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table};")
    conn.commit()

def create_tables(conn):
    cursor = conn.cursor()
    # Create tasks table
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
    # Create importance_features table
    cursor.execute("""
    CREATE TABLE importance_features (
        feature TEXT PRIMARY KEY,
        weight REAL
    );
    """)
    # Create urgency_features table
    cursor.execute("""
    CREATE TABLE urgency_features (
        feature TEXT PRIMARY KEY,
        weight REAL
    );
    """)
    # Create task_progress table
    cursor.execute("""
    CREATE TABLE task_progress (
        task_id TEXT PRIMARY KEY,
        progress REAL,
        FOREIGN KEY(task_id) REFERENCES tasks(id)
    );
    """)
    # Create resource_allocation table
    cursor.execute("""
    CREATE TABLE resource_allocation (
        user TEXT PRIMARY KEY,
        task_count INTEGER
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
    cursor.execute("""
        INSERT INTO tasks (id, title, level, parent_id, description)
        VALUES (?, ?, ?, ?, ?)
    """, (task_id, title, level, parent_id, description))
    conn.commit()
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

def initialize_feature_tables(conn):
    cursor = conn.cursor()
    # Initialize importance_features with example data or empty
    importance_data = [
        ('Feature1', 1.0),
        ('Feature2', 0.8),
        ('Feature3', 0.5)
    ]
    cursor.executemany("INSERT INTO importance_features (feature, weight) VALUES (?, ?);", importance_data)
    # Initialize urgency_features with example data or empty
    urgency_data = [
        ('FeatureA', 1.0),
        ('FeatureB', 0.7),
        ('FeatureC', 0.4)
    ]
    cursor.executemany("INSERT INTO urgency_features (feature, weight) VALUES (?, ?);", urgency_data)
    conn.commit()

def main():
    conn = connect_db()
    drop_tables(conn)
    create_tables(conn)
    wbs_data = load_json_file(WBS_DATA_PATH)
    wbs_scores = load_json_file(WBS_SCORES_PATH)
    for task in wbs_data:
        insert_task(conn, task)
    update_task_scores(conn, wbs_scores)
    initialize_feature_tables(conn)
    print("Full project management database has been built and initialized.")

if __name__ == "__main__":
    main()
