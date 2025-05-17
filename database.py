import sqlite3

def create_tables():
    conn = sqlite3.connect('society.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS guests (
                      id INTEGER PRIMARY KEY, 
                      name TEXT, 
                      phone TEXT, 
                      flat_no TEXT, 
                      visit_time TEXT, 
                      reason TEXT, 
                      vehicle_number TEXT, 
                      photo BLOB)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                      id INTEGER PRIMARY KEY, 
                      name TEXT, 
                      phone TEXT, 
                      flat_no TEXT, 
                      mail TEXT, 
                      status TEXT)''')
    
    conn.commit()
    conn.close()



def get_guest_data(date, from_time, to_time):
    conn = sqlite3.connect('society.db')
    cursor = conn.cursor()

    # Format the input to create the query
    start_datetime = f"{date} {from_time}"
    end_datetime = f"{date} {to_time}"

    # Query the guests table
    cursor.execute('''
        SELECT id, name, phone, flat_no, visit_time, reason, vehicle_number
        FROM guests
        WHERE datetime(visit_time) BETWEEN ? AND ?
    ''', (start_datetime, end_datetime))

    rows = cursor.fetchall()
    conn.close()
    return rows


def validate_flat(flat_number):
    conn = sqlite3.connect('society.db')
    cursor = conn.cursor()
    cursor.execute("SELECT flat_no FROM members WHERE flat_no = ?", (flat_number,))
    result =cursor.fetchone()
    return result is not None

def insert_guest(name, phone, flat_no, visit_time, reason, vehicle_number, photo):
    conn = sqlite3.connect('society.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO guests (name, phone, flat_no, visit_time, reason, vehicle_number, photo) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (name, phone, flat_no, visit_time, reason, vehicle_number, photo))
    conn.commit()
    conn.close()

def insert_member(name, phone, flat_no, mail, status):
    conn = sqlite3.connect('society.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO members (name, phone, flat_no, mail, status) VALUES (?, ?, ?, ?, ?)",
                   (name, phone, flat_no, mail, status))
    conn.commit()
    conn.close()

def get_guest(name):
    conn = sqlite3.connect('society.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guests WHERE name=?", (name,))
    guest = cursor.fetchone()
    conn.close()
    return guest



def get_all_guests():
    conn = sqlite3.connect('society.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guests")
    guests = cursor.fetchall()
    conn.close()
    return guests

def get_all_members():
    conn = sqlite3.connect('society.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    conn.close()
    return members
def create_access_code_table():
    conn = sqlite3.connect("society_security.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_codes (
            id INTEGER PRIMARY KEY,
            code TEXT NOT NULL
        )
    ''')

    # Insert default access code if not present
    cursor.execute("INSERT OR IGNORE INTO access_codes (id, code) VALUES (1, '1234')")
    
    conn.commit()
    conn.close()

def validate_access_code(input_code):
    # Connect to the database
    conn = sqlite3.connect("society_security.db")
    cursor = conn.cursor()

    # Query to get the stored access code
    cursor.execute("SELECT code FROM access_codes WHERE id=1")
    stored_code = cursor.fetchone()

    conn.close()

    # Check if stored code matches the input code
    if stored_code and stored_code[0] == input_code:
        return True
    else:
        return False

def create_tables():
    conn = sqlite3.connect("society_security.db")
    cursor = conn.cursor()

    # Create access_codes table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS access_codes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        code TEXT NOT NULL
                      )''')

    # Check if an access code already exists
    cursor.execute("SELECT * FROM access_codes WHERE id=1")
    existing_code = cursor.fetchone()

    # Insert default access code if none exists
    if not existing_code:
        cursor.execute("INSERT INTO access_codes (code) VALUES (?)", ("VD2122",))

    conn.commit()
    conn.close()

# Call this function to create the table when initializing your system
create_tables()

def check_member_existence(phone, email, flat, name):
    conn = sqlite3.connect('society.db')
    cursor = conn.cursor()

    # Check for phone conflict
    cursor.execute("SELECT * FROM members WHERE phone = ?", (phone,))
    if cursor.fetchone():
        conn.close()
        return "phone"

    # Check for email conflict
    cursor.execute("SELECT * FROM members WHERE mail = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return "email"

    # Check for flat number conflict
    cursor.execute("SELECT * FROM members WHERE flat_no = ?", (flat,))
    if cursor.fetchone():
        conn.close()
        return "flat"

    # Check for name conflict
    cursor.execute("SELECT * FROM members WHERE name = ?", (name,))
    if cursor.fetchone():
        conn.close()
        return "name"

    # Check for an exact match of all details (optional, based on your requirements)
    cursor.execute("SELECT * FROM members WHERE phone = ? AND mail = ? AND flat_no = ? AND name = ?", (phone, email, flat, name))
    if cursor.fetchone():
        conn.close()
        return "member"

    conn.close()
    return None
