import socket
import subprocess
import sys
from datetime import datetime

class NetworkScanner:
    def __init__(self, target):
        self.target = target
        self.open_ports = []
        self.start_time = None
        self.end_time = None
        
    def scan_port(self, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            sock.close()
            
            if result == 0:
                service = self.get_service_name(port)
                print(f"[+] Port {port}: OPEN ({service})")
                self.open_ports.append(port)
                return True
        except Exception as e:
            pass
        return False
    
    def get_service_name(self, port):
        """Get common service name for port"""
        services = {
            20: "FTP-data",
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            111: "RPCbind",
            135: "MSRPC",
            139: "NetBIOS",
            143: "IMAP",
            443: "HTTPS",
            445: "SMB",
            993: "IMAPS",
            995: "POP3S",
            1723: "PPTP",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            6379: "Redis",
            27017: "MongoDB"
        }
        return services.get(port, "Unknown")
    
    def scan_common_ports(self):
        """Scan most common ports"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 
                        443, 445, 993, 995, 1723, 3306, 3389, 5432, 5900, 
                        6379, 27017]
        
        self.start_time = datetime.now()
        print(f"\n[*] Scanning target: {self.target}")
        print(f"[*] Started at: {self.start_time}")
        print("-" * 50)
        
        for port in common_ports:
            self.scan_port(port)
        
        self.end_time = datetime.now()
        return self.open_ports
    
    def scan_port_range(self, start, end):
        """Scan a range of ports"""
        self.start_time = datetime.now()
        print(f"\n[*] Scanning target: {self.target}")
        print(f"[*] Scanning ports: {start}-{end}")
        print(f"[*] Started at: {self.start_time}")
        print("-" * 50)
        
        for port in range(start, end + 1):
            self.scan_port(port)
        
        self.end_time = datetime.now()
        return self.open_ports
    
    def get_summary(self):
        """Get scan summary"""
        if not self.start_time:
            return "No scan performed yet"
        
        scan_time = self.end_time - self.start_time
        return {
            "target": self.target,
            "total_ports_scanned": len(self.open_ports) if self.open_ports else 0,
            "open_ports_found": len(self.open_ports),
            "open_ports_list": self.open_ports,
            "scan_duration": str(scan_time).split('.')[0],
            "start_time": self.start_time,
            "end_time": self.end_time
        }
    
    def generate_report(self):
        """Generate a simple report"""
        summary = self.get_summary()
        
        report = []
        report.append("=" * 60)
        report.append("NETWORK SCAN REPORT")
        report.append("=" * 60)
        report.append(f"Target: {summary['target']}")
        report.append(f"Scan started: {summary['start_time']}")
        report.append(f"Scan ended: {summary['end_time']}")
        report.append(f"Scan duration: {summary['scan_duration']}")
        report.append(f"Open ports found: {summary['open_ports_found']}")
        report.append("-" * 60)
        
        if self.open_ports:
            report.append("OPEN PORTS:")
            for port in self.open_ports:
                service = self.get_service_name(port)
                report.append(f"  - Port {port}/tcp -> {service}")
        else:
            report.append("No open ports found")
        
        report.append("=" * 60)
        report.append("IMPORTANT: Only scan systems you own!")
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    print("=" * 60)
    print("AI NETWORK ENUMERATOR (Educational Purpose Only)")
    print("=" * 60)
    print("\nWARNING: Only scan systems you own or have permission to test!")
    print("   Unauthorized scanning is illegal.\n")
    
    while True:
        print("\nMENU:")
        print("1. Scan common ports")
        print("2. Scan port range")
        print("3. Generate report")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            target = input("Enter target IP or hostname: ").strip()
            if not target:
                print("Target cannot be empty!")
                continue
            
            scanner = NetworkScanner(target)
            scanner.scan_common_ports()
            
            save = input("\nSave report? (y/n): ").lower()
            if save == 'y':
                filename = f"scan_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                report = scanner.generate_report()
                # FIX: encoding='utf-8' add kiya hai
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"[+] Report saved to {filename}")
        
        elif choice == "2":
            target = input("Enter target IP or hostname: ").strip()
            if not target:
                print("Target cannot be empty!")
                continue
            
            try:
                start = int(input("Enter start port: ").strip())
                end = int(input("Enter end port: ").strip())
                
                if start > end:
                    print("Start port cannot be greater than end port!")
                    continue
                    
                scanner = NetworkScanner(target)
                scanner.scan_port_range(start, end)
                
                save = input("\nSave report? (y/n): ").lower()
                if save == 'y':
                    filename = f"scan_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    report = scanner.generate_report()
                    # FIX: encoding='utf-8' add kiya hai
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(report)
                    print(f"[+] Report saved to {filename}")
            except ValueError:
                print("Please enter valid port numbers!")
        
        elif choice == "3":
            if 'scanner' in locals():
                print("\n" + scanner.generate_report())
            else:
                print("No scan performed yet")
        
        elif choice == "4":
            print("\nStay ethical! Scan responsibly.")
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()