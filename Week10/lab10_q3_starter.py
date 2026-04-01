# ============================================================
#  WEEK 10 LAB — Q3: SECURITY AUDIT LOG + UNIT TESTS
#  COMP2152 — Jessica Wisnoski
# ============================================================
import sqlite3
# Imports Python's built-in SQLite library.
# SQLite lets your Python program create and use a local database file.

import unittest
# Imports Python's built-in testing framework.
# unittest lets you write small tests to check whether your functions work correctly.


DB_NAME = "audit.db"
# This variable stores the name of the database file.
# SQLite will create this file if it does not already exist.


# ============================================================
# SUMMARY
# ============================================================
# This program creates a simple security audit log system.
# It stores security-related events in a SQLite database,
# such as logins, failed logins, file access, and permission changes.
#
# The program can:
# - seed the database with sample audit events
# - display events in a readable format
# - filter events by severity level
# - get the most recent events
# - count how many events exist for each severity
# - safely run a SQL query without crashing on database errors
# - test the functions automatically using unit tests
#
# In short:
# this is a small database + security log analysis + testing program.
# ============================================================


# --- Helpers (provided) — seeds the database with sample data ---
def seed_database():
    # "def" means you are defining a function.
    # This function creates the audit_log table and fills it with sample rows.

    """Create and populate the audit_log table with sample security events."""
    # This is a docstring.
    # Triple quotes are often used to document what a function does.

    conn = sqlite3.connect(DB_NAME)
    # Opens a connection to the SQLite database file.

    cursor = conn.cursor()
    # Creates a cursor object.
    # The cursor is what you use to send SQL commands to the database.

    cursor.execute("DROP TABLE IF EXISTS audit_log")
    # Deletes the audit_log table if it already exists.
    # This gives you a fresh clean table each time you run seed_database().

    cursor.execute("""CREATE TABLE audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user TEXT,
        action TEXT,
        severity TEXT,
        details TEXT
    )""")
    # Creates a brand-new table called audit_log.
    #
    # Columns:
    # - id: unique number for each row, automatically increases
    # - timestamp: date and time of the event
    # - user: which user performed the action
    # - action: what happened
    # - severity: LOW, MEDIUM, HIGH, etc.
    # - details: extra description about the event

    sample_data = [
        ("2026-03-16 08:00:00", "admin",   "LOGIN",            "LOW",    "Successful login from 192.168.1.10"),
        ("2026-03-16 08:05:00", "root",    "FAILED_LOGIN",     "HIGH",   "Failed SSH attempt from 10.0.0.99"),
        ("2026-03-16 08:10:00", "admin",   "FILE_ACCESS",      "LOW",    "Read /etc/config.yaml"),
        ("2026-03-16 08:15:00", "root",    "FAILED_LOGIN",     "HIGH",   "Failed SSH attempt from 10.0.0.99"),
        ("2026-03-16 08:20:00", "guest",   "FILE_MODIFY",      "MEDIUM", "Modified /tmp/upload.csv"),
        ("2026-03-16 08:25:00", "admin",   "PERMISSION_CHANGE","HIGH",   "Changed permissions on /etc/shadow"),
        ("2026-03-16 08:30:00", "guest",   "LOGOUT",           "LOW",    "Session ended normally"),
        ("2026-03-16 08:35:00", "backup",  "FILE_ACCESS",      "LOW",    "Read /var/backups/db.sql"),
        ("2026-03-16 08:40:00", "guest",   "FILE_MODIFY",      "MEDIUM", "Modified /tmp/data.json"),
        ("2026-03-16 08:45:00", "admin",   "LOGOUT",           "LOW",    "Session ended normally"),
    ]
    # This is a Python list of tuples.
    # Each tuple represents one audit event row to insert into the database.

    cursor.executemany(
        "INSERT INTO audit_log (timestamp, user, action, severity, details) VALUES (?, ?, ?, ?, ?)",
        sample_data
    )
    # executemany() inserts many rows at once.
    # The ? symbols are placeholders for values from each tuple in sample_data.
    # This is safer and cleaner than manually building SQL strings.

    conn.commit()
    # Saves all changes to the database.

    conn.close()
    # Closes the database connection.


def display_events(events):
    # This function prints audit log events in a clean readable format.

    """Pretty-print a list of audit events."""

    if not events:
        print("  (no events)")
        return
        # If the list is empty, show a message and stop the function.

    for row in events:
        # Each row is a tuple from the database.
        # Row order matches the table columns:
        # row[0] = id
        # row[1] = timestamp
        # row[2] = user
        # row[3] = action
        # row[4] = severity
        # row[5] = details

        print(f"  [{row[1]}]  {row[4]:<6}  {row[2]:<8}  {row[3]:<18}  {row[5]}")
        # This is an f-string used for formatting output neatly.
        # :<6 means left-align inside 6 spaces.
        # :<8 means left-align inside 8 spaces.
        # :<18 means left-align inside 18 spaces.


# TODO: Complete get_events_by_severity(severity)
#   Connect to DB_NAME.
#   SELECT all rows from audit_log WHERE severity matches the parameter.
#   Fetch all rows, close the connection, and return the list.
def get_events_by_severity(severity):
    # This function finds all audit events with a matching severity level.

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM audit_log WHERE severity = ?", (severity,))
    # SELECT * means get all columns.
    # WHERE severity = ? filters rows to only the matching severity.
    # (severity,) is a 1-item tuple containing the value to plug in.

    rows = cursor.fetchall()
    # fetchall() gets all matching rows and stores them in a list.

    conn.close()
    return rows
    # Returns the results to whoever called the function.


# TODO: Complete get_recent_events(limit)
#   Connect to DB_NAME.
#   SELECT all rows from audit_log ORDER BY timestamp DESC LIMIT ?
#   Use the limit parameter for the LIMIT value.
#   Fetch all rows, close the connection, and return the list.
def get_recent_events(limit):
    # This function gets the newest audit events.

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT ?", (limit,))
    # ORDER BY timestamp DESC sorts from newest to oldest.
    # LIMIT ? means only return a certain number of rows.

    rows = cursor.fetchall()

    conn.close()
    return rows


# TODO: Complete count_by_severity()
#   Connect to DB_NAME.
#   Execute: SELECT severity, COUNT(*) FROM audit_log
#            GROUP BY severity ORDER BY COUNT(*) DESC
#   Fetch all rows, close the connection, and return the list.
def count_by_severity():
    # This function counts how many events belong to each severity level.

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT severity, COUNT(*) FROM audit_log GROUP BY severity ORDER BY COUNT(*) DESC"
    )
    # COUNT(*) counts rows.
    # GROUP BY severity groups rows into LOW, MEDIUM, HIGH, etc.
    # ORDER BY COUNT(*) DESC puts the biggest count first.

    rows = cursor.fetchall()

    conn.close()
    return rows


# TODO: Complete safe_query(query)
#   Connect to DB_NAME.
#   Try to execute the query using cursor.execute(query).
#   If successful, fetch all rows and return them.
#   If sqlite3.Error occurs, print f"Database error: {e}" and return [].
#   Always close the connection in a finally block.
def safe_query(query):
    # This function runs a SQL query safely.
    # If the query fails, the program will not crash.

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Code inside try runs first.
        # If an error happens, Python jumps to except.

        cursor.execute(query)
        # Runs whatever SQL query string was passed in.

        return cursor.fetchall()
        # If query works, return all resulting rows.

    except sqlite3.Error as e:
        # This catches SQLite-related errors.

        print(f"Database error: {e}")
        # Prints the error message so you know what went wrong.

        return []
        # Returns an empty list instead of crashing.

    finally:
        # finally always runs whether there was an error or not.

        conn.close()
        # Ensures the database connection is closed every time.


# ============================================================
#  UNIT TESTS — fill in the test methods
# ============================================================
class TestAuditLog(unittest.TestCase):
    # This class groups together automated tests for the program.
    # unittest.TestCase gives you access to assertion methods like assertEqual().

    def setUp(self):
        # setUp() runs before EACH test method.
        # This resets the database so every test starts with known sample data.
        seed_database()

    def test_high_severity(self):
        # Test that there are exactly 3 HIGH severity events.
        events = get_events_by_severity("HIGH")
        self.assertEqual(len(events), 3)

    def test_recent_events(self):
        # Test that asking for 5 recent events returns 5 rows.
        events = get_recent_events(5)
        self.assertEqual(len(events), 5)

    def test_count(self):
        # Test that the severity count results include ("HIGH", 3).
        counts = count_by_severity()
        self.assertIn(("HIGH", 3), counts)

    def test_safe_bad_query(self):
        # Test that a bad SQL query does not crash the program.
        result = safe_query("SELECT * FROM fake_table")
        self.assertEqual(result, [])
        # Because the table does not exist, safe_query should return [].


# --- Main (provided) ---
if __name__ == "__main__":
    # This block only runs if you execute this file directly.
    # It will not run if the file is imported into another Python file.

    print("=" * 60)
    print("  SECURITY AUDIT LOG")
    print("=" * 60)

    seed_database()
    # Creates and fills the database with the sample audit data.

    print("\n--- HIGH Severity Events ---")
    display_events(get_events_by_severity("HIGH"))
    # Shows only HIGH severity events.

    print("\n--- 5 Most Recent Events ---")
    display_events(get_recent_events(5))
    # Shows the latest 5 audit events.

    print("\n--- Event Counts by Severity ---")
    counts = count_by_severity()

    if counts:
        for severity, count in counts:
            print(f"  {severity:<8}  {count}")
            # Prints something like:
            # HIGH      3
            # LOW       5
            # MEDIUM    2
    else:
        print("  (none)")

    print("\n--- Safe Query (valid) ---")
    results = safe_query("SELECT user, action FROM audit_log WHERE severity = 'HIGH'")
    # Runs a valid custom SQL query.

    if results:
        for row in results:
            print(f"  {row[0]:<8}  {row[1]}")
            # row[0] = user
            # row[1] = action

    print("\n--- Safe Query (invalid — should not crash) ---")
    results = safe_query("SELECT * FROM nonexistent_table")
    # This query is intentionally wrong.
    # The function should catch the error and return [] instead of crashing.

    print(f"  Returned: {results}")

    print("\n--- Running Unit Tests ---")
    unittest.main(verbosity=2, exit=False)
    # Runs the test methods in the TestAuditLog class.
    # verbosity=2 gives more detailed test output.
    # exit=False prevents the script from stopping immediately after tests.

    print("\n" + "=" * 60)