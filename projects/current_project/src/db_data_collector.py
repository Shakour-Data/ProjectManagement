from sqlite_db_manager import SQLiteDBManager
from feature_weights import URGENCY_FEATURE_WEIGHTS, IMPORTANCE_FEATURE_WEIGHTS

class DBDataCollector:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or SQLiteDBManager()
        self.db_manager.connect()

    def collect_and_store_tasks(self, tasks):
        """
        Collect task data including progress, resource allocation, and store in DB.
        """
        self.db_manager.insert_tasks(tasks)

    def collect_resource_allocation(self, tasks):
        """
        Analyze resource allocation and store summary in DB.
        """
        resource_usage = {}
        for task in tasks:
            for user in task.assigned_to:
                resource_usage[user] = resource_usage.get(user, 0) + 1

        cursor = self.db_manager.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resource_allocation (
                user TEXT PRIMARY KEY,
                task_count INTEGER
            )
        ''')
        cursor.execute('DELETE FROM resource_allocation')
        for user, count in resource_usage.items():
            cursor.execute('INSERT INTO resource_allocation (user, task_count) VALUES (?, ?)', (user, count))
        self.db_manager.conn.commit()

    def collect_progress_metrics(self, tasks):
        """
        Collect progress percentages and store/update in DB.
        """
        cursor = self.db_manager.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_progress (
                task_id INTEGER PRIMARY KEY,
                progress REAL
            )
        ''')
        for task in tasks:
            cursor.execute('INSERT OR REPLACE INTO task_progress (task_id, progress) VALUES (?, ?)', (task.id, task.workflow_progress_percentage()))
        self.db_manager.conn.commit()

    def insert_feature_weights(self, urgency_weights, importance_weights):
        """
        Insert predefined weights for urgency and importance features into DB.
        """
        self.db_manager.insert_urgency_feature_weights(urgency_weights)
        self.db_manager.insert_importance_feature_weights(importance_weights)

    def close(self):
        self.db_manager.close()
