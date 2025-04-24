import unittest
import os
import yaml
import sys

# Add the project directory to the path so we can import from it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class BaseTest(unittest.TestCase):
    """Base test class for ProjectL tests"""
    
    @classmethod
    def setUpClass(cls):
        """Load test configurations"""
        test_config_path = os.path.join(os.path.dirname(__file__), 'configs', 'test_configs.yaml')
        with open(test_config_path, 'r') as f:
            cls.test_configs = yaml.safe_load(f)
    
    def setUp(self):
        """Set up test fixtures, if any."""
        pass
    
    def tearDown(self):
        """Clean up after each test."""
        pass
