"""Test suite for dictionary driven checker package"""

import unittest
import os

def run_all_tests():
    """Run all tests in the package"""
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern="test_*.py")
    runner = unittest.TextTestRunner()
    return runner.run(suite)

if __name__ == '__main__':
    run_all_tests()