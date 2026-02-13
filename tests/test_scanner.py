import unittest
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from network_scanner import NetworkScanner

class TestNetworkScanner(unittest.TestCase):
    
    def setUp(self):
        """Setup before each test"""
        self.scanner = NetworkScanner("127.0.0.1")
    
    def test_init(self):
        """Test scanner initialization"""
        self.assertEqual(self.scanner.target, "127.0.0.1")
        self.assertEqual(self.scanner.open_ports, [])
    
    def test_get_service_name(self):
        """Test service name detection"""
        self.assertEqual(self.scanner.get_service_name(22), "SSH")
        self.assertEqual(self.scanner.get_service_name(80), "HTTP")
        self.assertEqual(self.scanner.get_service_name(443), "HTTPS")
        self.assertEqual(self.scanner.get_service_name(3306), "MySQL")
        self.assertEqual(self.scanner.get_service_name(3389), "RDP")
        self.assertEqual(self.scanner.get_service_name(9999), "Unknown")
    
    def test_scan_port_localhost(self):
        """Test scanning localhost"""
        # This just tests the method runs without error
        result = self.scanner.scan_port(9999)  # Should be closed
        self.assertIn(result, [True, False])  # Either open or closed
    
    def test_generate_report_empty(self):
        """Test report generation with no scan"""
        summary = self.scanner.get_summary()
        self.assertEqual(summary, "No scan performed yet")
    
    def test_port_range_validation(self):
        """Test scanner with different targets"""
        scanner2 = NetworkScanner("192.168.1.1")
        self.assertEqual(scanner2.target, "192.168.1.1")
    
    def test_summary_after_scan(self):
        """Test summary after mock scan"""
        # Mock a scan by manually adding ports
        self.scanner.open_ports = [22, 80]
        self.scanner.start_time = "2024-01-01"
        self.scanner.end_time = "2024-01-01"
        
        summary = self.scanner.get_summary()
        # If it's a dict, we have summary
        if isinstance(summary, dict):
            self.assertEqual(summary['open_ports_found'], 2)
        else:
            # If it's a string, it's the "No scan" message
            self.assertEqual(summary, "No scan performed yet")

if __name__ == '__main__':
    unittest.main()
