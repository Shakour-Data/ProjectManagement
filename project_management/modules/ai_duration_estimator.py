import json
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

class AIDurationEstimator:
    def __init__(self, dataset_path='project_inputs/PM_JSON/user_inputs/duration_dataset.json', model_path='project_management/models/duration_model.pkl'):
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
            # Example features: complexity, resource_count, estimated_cost, priority_score
            feature_vector = [
                item.get('complexity', 1),
                item.get('resource_count', 1),
                item.get('estimated_cost', 0),
                item.get('priority_score', 0)
            ]
            self.features.append(feature_vector)
            self.labels.append(item.get('duration_hours', 1))
        self.features = np.array(self.features)
        self.labels = np.array(self.labels)
        return True

    def train_model(self):
        if not self.load_dataset():
            return False
        X_train, X_test, y_train, y_test = train_test_split(self.features, self.labels, test_size=0.2, random_state=42)
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        print(f"Model trained. Mean Absolute Error on test set: {mae:.2f} hours")
        self.save_model()
        return True

    def save_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}")

    def load_model(self):
        if not os.path.exists(self.model_path):
            print(f"Model file not found: {self.model_path}")
            return False
        self.model = joblib.load(self.model_path)
        return True

    def predict_duration(self, task_features):
        """
        task_features: dict with keys matching features used in training
        Returns predicted duration in hours
        """
        if self.model is None:
            if not self.load_model():
                print("Model not loaded. Cannot predict.")
                return None
        feature_vector = np.array([[
            task_features.get('complexity', 1),
            task_features.get('resource_count', 1),
            task_features.get('estimated_cost', 0),
            task_features.get('priority_score', 0)
        ]])
        prediction = self.model.predict(feature_vector)
        return float(prediction[0])

if __name__ == "__main__":
    estimator = AIDurationEstimator()
    if not estimator.load_model():
        print("Training model as no pre-trained model found.")
        estimator.train_model()
    # Example prediction
    example_task = {
        "complexity": 3,
        "resource_count": 2,
        "estimated_cost": 500,
        "priority_score": 7
    }
    predicted_duration = estimator.predict_duration(example_task)
    print(f"Predicted duration (hours): {predicted_duration:.2f}")
