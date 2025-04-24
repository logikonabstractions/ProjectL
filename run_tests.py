#!/usr/bin/env python3
import unittest
import os
import sys
import argparse

# Add the main directory to path for imports to work correctly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_tests(pattern=None, verbosity=2):
    """Run all tests matching the given pattern"""
    loader = unittest.TestLoader()
    
    if pattern:
        test_suite = loader.discover('tests', pattern=f'test_{pattern}.py')
    else:
        test_suite = loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(test_suite)
    return result

def main():
    parser = argparse.ArgumentParser(description='Run ProjectL tests')
    parser.add_argument('module', nargs='?', help='Specific module to test (e.g. pieces, card, actions)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase verbosity')
    
    args = parser.parse_args()
    verbosity = 3 if args.verbose else 2
    
    if args.module:
        print(f"Running tests for module: {args.module}")
        result = run_tests(pattern=args.module, verbosity=verbosity)
    else:
        print("Running all tests")
        result = run_tests(verbosity=verbosity)
    
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
