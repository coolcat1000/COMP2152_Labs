# ============================================================
#  WEEK 10 LAB — Q1: PASSWORD VAULT
#  COMP2152 — Jessica Wisnoski
# ============================================================









# ================================
# PASSWORD VAULT SUMMARY
# ================================
# This program creates a simple password manager using SQLite.
# It stores login credentials (website, username, password) in a database.
# You can:
# - Add new credentials
# - View all saved credentials
# - Search for credentials by website
# The program demonstrates basic database operations:
# INSERT (add), SELECT (retrieve), and simple filtering.







import sqlite3
# This imports the built-in SQLite library so Python can work with a local database file.

DB_NAME = "vault.db"
# DB_NAME is just a variable storing the database file name.
# "vault.db" is a file that SQLite will create (or open if it already exists).
# The ".db" is just a file extension (like .txt or .jpg) — it indicates this is a database file.


# --- Helpers (provided) ---
def setup_database():
    # "def" means you are DEFINING a function.
    # This function sets up your database table if it doesn't already exist.

    """Create the vault table if it doesn't exist."""
    # This is a DOCSTRING (triple quotes).
    # It is not just a comment — Python can read it as documentation for the function.

    conn = sqlite3.connect(DB_NAME)
    # Opens (or creates) the database file.

    cursor = conn.cursor()
    # A cursor lets you execute SQL commands (like INSERT, SELECT, etc.).

    cursor.execute("""CREATE TABLE IF NOT EXISTS vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT,
        username TEXT,
        password TEXT
    )""")
    # This is SQL code.
    # It creates a table called "vault" only if it doesn't already exist.
    # Columns:
    # - id: unique number, auto-increases
    # - website, username, password: stored as text

    conn.commit()
    # Saves changes to the database.

    conn.close()
    # Closes the connection (important to avoid data issues).


def display_credentials(credentials):
    """Pretty-print a list of credential rows."""
    # This function prints database results in a clean format.

    if not credentials:
        print("  (no results)")
        return
        # If the list is empty, print a message and stop.

    for row in credentials:
        # Each "row" is a tuple like: (id, website, username, password)

        print(f"  {row[1]:<14} | {row[2]:<12} | {row[3]}")
        # row[1] = website
        # row[2] = username
        # row[3] = password
        # The :<14 means "left-align in 14 spaces" (for formatting output)


def add_credential(website, username, password):
    # This function ADDS a new login entry to the database.

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO vault (website, username, password) VALUES (?, ?, ?)",
        (website, username, password)
    )
    # This inserts a new row into the table.
    # The ? are placeholders (prevents SQL injection and is safer).
    # Values are passed as a tuple.

    conn.commit()
    conn.close()


def get_all_credentials():
    # This function retrieves ALL saved credentials.

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vault ORDER BY website ASC")
    # SELECT * = get all columns
    # ORDER BY website ASC = sort alphabetically by website

    rows = cursor.fetchall()
    # fetchall() gets all results and stores them in a list.

    conn.close()
    return rows


def find_credential(website):
    # This function searches for credentials matching a specific website.

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vault WHERE website = ?", (website,))
    # WHERE filters results.
    # (website,) — the comma is required to make it a tuple in Python.

    rows = cursor.fetchall()
    conn.close()
    return rows


# --- Main (provided) ---
if __name__ == "__main__":
    # This ensures the code below only runs when the file is executed directly,
    # not when it is imported into another Python file.

    print("=" * 60)
    print("  PASSWORD VAULT")
    print("=" * 60)

    setup_database()
    # Make sure the database/table exists before using it.

    print("\n--- Adding Credentials ---")
    credentials = [
        ("github.com",  "admin",        "s3cur3P@ss"),
        ("google.com",  "maziar@gmail",  "MyP@ssw0rd"),
        ("netflix.com", "maziar",        "N3tfl1x!"),
        ("github.com",  "work_user",    "W0rkP@ss!"),
    ]
    # This is a list of tuples (sample data).

    for site, user, pw in credentials:
        # Loop through each tuple and unpack values.

        add_credential(site, user, pw)
        # Save each credential to the database.

        print(f"  Saved: {site}" + (f" ({user.split('_')[0]})" if "_" in user else ""))
        # If username has "_", split it and show part of it.


    print("\n--- All Credentials ---")
    display_credentials(get_all_credentials())
    # Get everything from DB and print it.


    print("\n--- Search for 'github.com' ---")
    display_credentials(find_credential("github.com"))
    # Search for specific website.


    print("\n--- Search for 'spotify.com' ---")
    display_credentials(find_credential("spotify.com"))
    # This will likely show no results.


    print("\n" + "=" * 60)