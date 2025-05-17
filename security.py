import sqlite3
ACCESS_CODE = "VD2122"

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

def update_access_code(new_code):
    # Connect to the database
    conn = sqlite3.connect("society_security.db")
    cursor = conn.cursor()

    # Update the access code
    cursor.execute("UPDATE access_codes SET code = ? WHERE id = 1", (new_code,))
    conn.commit()
    conn.close()


def emergency_alert(phone, alert_type):
    if alert_type == "fire":
        message = "Fire alert! Evacuate immediately."
    elif alert_type == "emergency":
        message = "Emergency alert! Take immediate action."
    send_sms(phone, message)
