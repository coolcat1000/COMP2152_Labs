# ============================================================
#  WEEK 10 LAB — Q2: LOGIN ATTEMPT TRACKER
#  COMP2152 — Jessica Wisnoski
# ============================================================


# ================================
# LOGIN ATTEMPT TRACKER SUMMARY
# ================================
# This program tracks login attempts for different users.
# Each attempt records:
# - Username
# - Whether the login was successful (True/False)
# - Timestamp of the attempt
# You can:
# - Record login attempts
# - View failed attempts for a user
# - Count failures per user (detect suspicious activity)
# - Delete/reset attempts for a user
# The program demonstrates data tracking, filtering, grouping (COUNT),
# and basic security monitoring concepts.









import sqlite3
# Built-in library that lets Python create and interact with a local SQL database.

import datetime
# Used to get the current date and time for each login attempt.


DB_NAME = "login_tracker.db"
# This is the file name of your database.
# If it doesn’t exist, SQLite will create it automatically.


# --- Helpers (provided) ---
def setup_database():
    # This function sets up your database from scratch.

    """Create the login_attempts table if it doesn't exist."""
    # Docstring: explains what the function does (used for documentation tools).

    conn = sqlite3.connect(DB_NAME)
    # Open (or create) the database file.

    cursor = conn.cursor()
    # Cursor lets you send SQL commands to the database.

    cursor.execute("DROP TABLE IF EXISTS login_attempts")
    # Deletes the table if it already exists.
    # This ensures you start fresh every time you run the program.

    cursor.execute("""CREATE TABLE login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        success INTEGER,
        attempt_date TEXT
    )""")
    # Creates a table with 4 columns:
    # - id: unique auto-incrementing number
    # - username: who tried to log in
    # - success: 1 (True) or 0 (False)
    # - attempt_date: timestamp stored as text

    conn.commit()
    # Save changes.

    conn.close()
    # Close connection.


def display_attempts(attempts):
    # This function prints login attempts in a readable format.

    """Pretty-print a list of attempt rows."""

    if not attempts:
        print("  (no results)")
        return
        # If list is empty, exit early.

    for row in attempts:
        # Each row looks like: (id, username, success, attempt_date)

        status = "success" if row[2] else "FAILED"
        # row[2] = success value (1 or 0)
        # Converts it into readable text.

        print(f"  {row[1]:<8} | {status:<7} | {row[3]}")
        # row[1] = username
        # row[3] = date
        # Formatting aligns columns for cleaner output.


def record_attempt(username, success):
    # This function saves a login attempt into the database.

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO login_attempts (username, success, attempt_date) VALUES (?, ?, ?)",
        (username, success, str(datetime.datetime.now()))
    )
    # INSERT adds a new row.
    # "?" are placeholders to safely insert values.
    # datetime.datetime.now() gets current timestamp.
    # str(...) converts it to text so it can be stored.

    conn.commit()
    conn.close()


def get_failed_attempts(username):
    # This function retrieves only FAILED attempts for a specific user.

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM login_attempts WHERE username = ? AND success = 0",
        (username,)
    )
    # WHERE filters results:
    # - username must match
    # - success = 0 means failed attempts

    rows = cursor.fetchall()
    # fetchall() returns all matching rows as a list.

    conn.close()
    return rows


def count_failures_per_user():
    # This function counts how many failed attempts each user has.

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, COUNT(*) FROM login_attempts WHERE success = 0 GROUP BY username"
    )
    # COUNT(*) counts rows.
    # GROUP BY username groups results per user.
    # So you get: (username, number_of_failures)

    rows = cursor.fetchall()

    conn.close()
    return rows


def delete_old_attempts(username):
    # This function deletes ALL login attempts for a specific user.

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM login_attempts WHERE username = ?", (username,))
    # DELETE removes rows matching the condition.

    deleted = cursor.rowcount
    # rowcount tells you how many rows were deleted.

    conn.commit()
    conn.close()

    return deleted


# --- Main (provided) ---
if __name__ == "__main__":
    # This ensures the code below runs only when this file is executed directly.

    print("=" * 60)
    print("  LOGIN ATTEMPT TRACKER")
    print("=" * 60)

    setup_database()
    # Reset and create fresh database.

    print("\n--- Recording Login Attempts ---")
    attempts = [
        ("admin", True),
        ("admin", False),
        ("admin", False),
        ("admin", False),
        ("guest", True),
        ("guest", False),
        ("root",  False),
        ("root",  False),
        ("root",  False),
        ("root",  False),
    ]
    # List of test login attempts (username, success).

    for user, success in attempts:
        # Loop through each tuple.

        record_attempt(user, success)
        # Save it to the database.

        status = "success" if success else "FAILED"
        print(f"  Recorded: {user} ({status})")


    print("\n--- Failed Attempts for 'admin' ---")
    display_attempts(get_failed_attempts("admin"))
    # Get and display only failed attempts for "admin".


    print("\n--- Failure Counts ---")
    counts = count_failures_per_user()

    if counts:
        for user, count in counts:
            msg = f"  {user:<10}  {count} failed attempts"

            if count >= 4:
                msg += f"  \u26a0 {user} has {count} failed attempts — possible brute-force!"
                # Adds a warning if too many failures (security signal).

            print(msg)
    else:
        print("  (no failures)")


    print("\n--- Reset 'root' account (delete all attempts) ---")
    deleted = delete_old_attempts("root")

    if deleted:
        print(f"  Deleted {deleted} records for root")
    else:
        print("  (nothing to delete)")


    print("\n--- Failure Counts (after reset) ---")
    counts = count_failures_per_user()

    if counts:
        for user, count in counts:
            print(f"  {user:<10}  {count} failed attempts")
    else:
        print("  (no failures)")

    print("\n" + "=" * 60)