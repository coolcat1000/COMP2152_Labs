# ============================================================
#  WEEK 12 LAB — Q1: SCANNER INHERITANCE
#  COMP2152 — [Your Name Here]
# ============================================================

import socket
import urllib.request


class Scanner:
    """Parent class — shared by all scanner types."""

    def __init__(self, target):
        self.target = target
        self.results = []

    # TODO: Write display_results(self)
    #   Print "Results for {self.target}:"
    #   If self.results is empty: print "  (no results)"
    #   Otherwise: print each result with "  " indent
    def display_results(self):
        pass


class PortScanner(Scanner):
    """Child class — scans for open ports."""

    # TODO: Write __init__(self, target, ports)
    #   Call the parent constructor: super().__init__(target)
    #   Store self.ports (a list of port numbers)
    def __init__(self, target, ports):
        pass

    # TODO: Write scan(self)
    #   Loop through self.ports
    #   For each port:
    #     Create a socket, set timeout to 1, use connect_ex
    #     If result == 0: append f"Port {port}: OPEN" to self.results
    #     Else: append f"Port {port}: closed" to self.results
    #     Close the socket
    def scan(self):
        pass


class HTTPScanner(Scanner):
    """Child class — scans HTTP paths for accessible pages."""

    # TODO: Write __init__(self, target, paths)
    #   Call the parent constructor: super().__init__(target)
    #   Store self.paths (a list of URL paths like "/", "/admin")
    def __init__(self, target, paths):
        pass

    # TODO: Write scan(self)
    #   Loop through self.paths
    #   For each path:
    #     Try: urllib.request.urlopen(f"http://{self.target}{path}")
    #       Append f"{path} → {response.status} (accessible)" to self.results
    #     Except: Append f"{path} → NOT FOUND" to self.results
    def scan(self):
        pass


# --- Main (provided) ---
if __name__ == "__main__":
    print("=" * 60)
    print("  Q1: SCANNER INHERITANCE")
    print("=" * 60)

    print("\n--- Port Scanner ---")
    ps = PortScanner("127.0.0.1", [22, 80, 443])
    print(f"  Scanning {ps.target} ports...")
    ps.scan()
    ps.display_results()

    print("\n--- HTTP Scanner ---")
    hs = HTTPScanner("127.0.0.1", ["/", "/admin", "/.git/config"])
    print(f"  Scanning {hs.target} paths...")
    hs.scan()
    hs.display_results()

    print("\n" + "=" * 60)