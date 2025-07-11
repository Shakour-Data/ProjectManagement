import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../docs/project_management/project_management.db')

class SQLiteDBManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Table for tasks with importance and urgency scores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                importance REAL,
                urgency REAL,
                status TEXT,
                progress REAL
            )
        ''')

        # Table for urgency features with weights
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urgency_features (
                feature TEXT PRIMARY KEY,
                weight REAL
            )
        ''')

        # Table for importance features with weights
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS importance_features (
                feature TEXT PRIMARY KEY,
                weight REAL
            )
        ''')

        # Additional tables for dashboards and reports can be added here
        self.conn.commit()

    def insert_urgency_feature_weights(self, features_weights):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM urgency_features')
        for feature, weight in features_weights.items():
            cursor.execute('INSERT INTO urgency_features (feature, weight) VALUES (?, ?)', (feature, weight))
        self.conn.commit()

    def insert_importance_feature_weights(self, features_weights):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM importance_features')
        for feature, weight in features_weights.items():
            cursor.execute('INSERT INTO importance_features (feature, weight) VALUES (?, ?)', (feature, weight))
        self.conn.commit()

    def insert_task(self, task):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO tasks (id, title, description, importance, urgency, status, progress)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (task.id, task.title, task.description, task.importance, task.urgency, task.status, task.workflow_progress_percentage()))
        self.conn.commit()

    def insert_tasks(self, tasks):
        for task in tasks:
            self.insert_task(task)

    def fetch_all_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        return cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()
