import unittest
import os
import sys

# Add the parent directory to the path so we can import modules correctly
sys.path.append('/tmp/inputs')

# Import the test class
from test_game_integration import TestGameIntegration

if __name__ == '__main__':
    # Create a test suite with all tests from TestGameIntegration
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestGameIntegration)
    
    # Run the test suite
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    
    # Return non-zero exit code if tests failed
    sys.exit(not result.wasSuccessful())
