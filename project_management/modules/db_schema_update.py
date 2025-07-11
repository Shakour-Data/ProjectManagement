import sqlite3

def create_task_schedule_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a new table for task schedules with resource assignments and start/end dates
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        resource_id TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        FOREIGN KEY(task_id) REFERENCES tasks(id)
    )
    ''')

    conn.commit()
    conn.close()
    print("task_schedule table created or already exists.")

if __name__ == '__main__':
    db_path = 'projects/current_project/docs/project_management.db'
    create_task_schedule_table(db_path)
