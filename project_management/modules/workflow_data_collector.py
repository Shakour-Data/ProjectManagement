from sqlite_db_manager import SQLiteDBManager

class WorkflowDataCollector:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or SQLiteDBManager()
        self.db_manager.connect()

    def create_scrum_workflow_tables(self):
        cursor = self.db_manager.conn.cursor()
        # Table for Scrum sprints
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scrum_sprints (
                sprint_id INTEGER PRIMARY KEY,
                name TEXT,
                start_date DATE,
                end_date DATE,
                goal TEXT
            )
        ''')
        # Table for Scrum tasks linked to sprints
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scrum_tasks (
                task_id INTEGER PRIMARY KEY,
                sprint_id INTEGER,
                title TEXT,
                status TEXT,
                priority INTEGER,
                progress REAL,
                FOREIGN KEY (sprint_id) REFERENCES scrum_sprints(sprint_id)
            )
        ''')
        # Table for Scrum burndown data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scrum_burndown (
                sprint_id INTEGER,
                day DATE,
                remaining_work REAL,
                PRIMARY KEY (sprint_id, day),
                FOREIGN KEY (sprint_id) REFERENCES scrum_sprints(sprint_id)
            )
        ''')
        self.db_manager.conn.commit()

    def update_scrum_task(self, task_id, sprint_id, title, status, priority, progress):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO scrum_tasks (task_id, sprint_id, title, status, priority, progress)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (task_id, sprint_id, title, status, priority, progress))
        self.db_manager.conn.commit()

    def update_scrum_burndown(self, sprint_id, day, remaining_work):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO scrum_burndown (sprint_id, day, remaining_work)
            VALUES (?, ?, ?)
        ''', (sprint_id, day, remaining_work))
        self.db_manager.conn.commit()

    def generate_scrum_report(self, sprint_id):
        cursor = self.db_manager.conn.cursor()
        cursor.execute('''
            SELECT day, remaining_work FROM scrum_burndown WHERE sprint_id = ? ORDER BY day
        ''', (sprint_id,))
        return cursor.fetchall()

    def close(self):
        self.db_manager.close()

# Note: Integration with GitHub should be handled in src/github_integration.py or related modules,
# ensuring synchronization of Scrum workflow stages with GitHub Issues, Pull Requests, and Projects.
