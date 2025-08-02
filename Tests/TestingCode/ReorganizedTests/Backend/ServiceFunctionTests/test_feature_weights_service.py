import unittest
from project_management.modules.main_modules import feature_weights

class TestFeatureWeightsServiceFunctions(unittest.TestCase):
    """Test cases for feature_weights service functions according to Unit_Testing.md standards."""

    def setUp(self):
        """Setup any necessary test data or state."""
        pass

    # Service Function Tests - Test individual backend service functions for correct output
    def test_calculate_weights_basic(self):
        """Test calculate_weights with basic valid input."""
        features = {"feature1": 1, "feature2": 2}
        weights = feature_weights.calculate_weights(features)
        self.assertIsInstance(weights, dict)
        self.assertIn("feature1", weights)
        self.assertIn("feature2", weights)

    def test_calculate_weight_with_predefined_features(self):
        """Test calculate_weights with predefined features."""
        features = {"deadline_proximity": 1, "dependency": 2}
        weights = feature_weights.calculate_weights(features)
        self.assertIsInstance(weights, dict)
        self.assertIn("deadline_proximity", weights)
        self.assertIn("dependency", weights)

    def test_calculate_weight_with_mixed_features(self):
        """Test calculate_weights with mix of predefined and custom features."""
        features = {"deadline_proximity": 1, "custom_feature": 2}
        weights = feature_weights.calculate_weights(features)
        self.assertIsInstance(weights, dict)
        self.assertIn("deadline_proximity", weights)
        self.assertIn("custom_feature", weights)

if __name__ == "__main__":
    unittest.main()
