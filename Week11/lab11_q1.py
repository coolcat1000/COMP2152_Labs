# ============================================================
#  WEEK 11 LAB — Q1: PORT SCANNER CLASS
#  COMP2152 — Jessica Wisnoski
# ============================================================
import socket


class SimpleScanner:

    def __init__(self, target):
        self.target = target
        self.open_ports = []

    def scan_port(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        try:
            result = s.connect_ex((self.target, port))
            if result == 0:
                print(f"  Port {port} is OPEN")
                self.open_ports.append(port)
                return True
            else:
                return False
        finally:
            s.close()

    def scan_range(self, start_port, end_port):
        for port in range(start_port, end_port + 1):
            self.scan_port(port)

    def display_results(self):
        print(f"\nResults for {self.target}:")
        if not self.open_ports:
            print("  No open ports found.")
        else:
            for port in self.open_ports:
                print(f"  Port {port}")


# --- Main (provided) ---
if __name__ == "__main__":
    print("=" * 60)
    print("  Q1: PORT SCANNER CLASS")
    print("=" * 60)

    print("\n--- Scanner 1: localhost ---")
    scanner1 = SimpleScanner("127.0.0.1")
    print(f"  Scanning {scanner1.target} ports 78-82...")
    scanner1.scan_range(78, 82)
    scanner1.display_results()

    print("\n--- Scanner 2: different target ---")
    scanner2 = SimpleScanner("127.0.0.1")
    print(f"  Scanning {scanner2.target} ports 20-25...")
    scanner2.scan_range(20, 25)
    scanner2.display_results()

    print("\n" + "=" * 60)