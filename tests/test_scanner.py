import unittest
import sys
import os

# Path fix
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from network_scanner import NetworkScanner

class TestNetworkScanner(unittest.TestCase):
    
    def setUp(self):
        self.scanner = NetworkScanner("127.0.0.1")
    
    def test_import(self):
        """Test ke liye simple import check"""
        self.assertIsNotNone(self.scanner)
        print("✅ Import successful!")

if __name__ == '__main__':
    unittest.main()
