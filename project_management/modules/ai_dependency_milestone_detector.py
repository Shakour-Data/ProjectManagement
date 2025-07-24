import json
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

class AIDependencyMilestoneDetector:
    def __init__(self, dataset_path='project_inputs/PM_JSON/user_inputs/dependency_dataset.json', model_path='project_management/models/dependency_model.pkl'):
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.model = None
        self.features = []
        self.labels = []

    def load_dataset(self):
        if not os.path.exists(self.dataset_path):
            print(f"Dataset file not found: {self.dataset_path}")
            return False
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.features = []
        self.labels = []
        for item in data:
            # Example features: task attributes that may influence dependencies
            feature_vector = [
                item.get('task_complexity', 1),
                item.get('task_priority', 0),
                item.get('estimated_duration', 1),
                item.get('resource_count', 1)
            ]
            self.features.append(feature_vector)
            # Label: 0 = no dependency, 1 = dependency exists
            self.labels.append(item.get('has_dependency', 0))
        self.features = np.array(self.features)
        self.labels = np.array(self.labels)
        return True

    def train_model(self):
        if not self.load_dataset():
            return False
        X_train, X_test, y_train, y_test = train_test_split(self.features, self.labels, test_size=0.2, random_state=42)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Dependency model trained. Accuracy on test set: {accuracy:.2f}")
        self.save_model()
        return True

    def save_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Dependency model saved to {self.model_path}")

    def load_model(self):
        if not os.path.exists(self.model_path):
            print(f"Dependency model file not found: {self.model_path}")
            return False
        self.model = joblib.load(self.model_path)
        return True

    def predict_dependency(self, task_features):
        """
        task_features: dict with keys matching features used in training
        Returns 1 if dependency predicted, else 0
        """
        if self.model is None:
            if not self.load_model():
                print("Dependency model not loaded. Cannot predict.")
                return None
        feature_vector = np.array([[
            task_features.get('task_complexity', 1),
            task_features.get('task_priority', 0),
            task_features.get('estimated_duration', 1),
            task_features.get('resource_count', 1)
        ]])
        prediction = self.model.predict(feature_vector)
        return int(prediction[0])

    def identify_milestones(self, tasks):
        """
        Identify start and end milestones based on dependencies.
        Adds 'is_start_milestone' and 'is_end_milestone' flags to tasks.
        """
        task_ids = {task['id'] for task in tasks}
        predecessors = {task['id']: task.get('predecessors', []) for task in tasks}
        successors = {task['id']: [] for task in tasks}
        for task_id, preds in predecessors.items():
            for pred in preds:
                if pred in successors:
                    successors[pred].append(task_id)

        for task in tasks:
            preds = predecessors.get(task['id'], [])
            succs = successors.get(task['id'], [])
            task['is_start_milestone'] = len(preds) == 0
            task['is_end_milestone'] = len(succs) == 0

        return tasks

if __name__ == "__main__":
    detector = AIDependencyMilestoneDetector()
    if not detector.load_model():
        print("Training dependency model as no pre-trained model found.")
        detector.train_model()
    # Example prediction
    example_task = {
        "task_complexity": 3,
        "task_priority": 5,
        "estimated_duration": 10,
        "resource_count": 2
    }
    dep_pred = detector.predict_dependency(example_task)
    print(f"Predicted dependency existence: {dep_pred}")
