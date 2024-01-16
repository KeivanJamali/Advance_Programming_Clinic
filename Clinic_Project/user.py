import mysql.connector
from datetime import datetime
import re
from email_validator import validate_email, EmailNotValidError

# Assuming you have a MySQL database set up with the following credentials
db_config = {
    'host': 'your_mysql_host',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'your_database_name'
}

create_user_table_query = """
-- User table
CREATE TABLE User (
    user_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(20) NOT NULL,
    user_type ENUM('patient', 'clinic_staff') NOT NULL
);
"""

# Establish a connection to the MySQL server
conn = mysql.connector.connect(**db_config)

# Create a cursor object to interact with the database
cursor = conn.cursor()
cursor.execute(create_user_table_query)
cursor.execute(create_user_table_query)
class User:
    def __init__(self, user_id, name, email, password, user_type):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type

    def validate_user_id(self):
        # Validate user_id using regular expression
        return re.match(r'^[a-zA-Z0-9]{5,20}$', self.user_id) is not None

    def validate_password(self):
        # Validate password using regular expression
        return re.match(r'^[a-zA-Z0-9]{5,20}$', self.password) is not None

    def validate_name(self):
        # Validate name using regular expression
        return re.match(r'^[a-zA-Z0-9]{5,20}$', self.name) is not None

    def validate_email(self):
        # Validate email using email_validator library
        try:
            validate_email(self.email)
            return True
        except EmailNotValidError as e:
            print(f"Invalid email: {e}")
            return False

    def register(self):
        # Implementation for user registration with validation checks
        if self.validate_user_id() and self.validate_password() and self.validate_name() and self.validate_email():
            # Insert user into the database
            sql = 'INSERT INTO User (user_id, name, email, password, user_type, login_status) VALUES (%s, %s, %s, %s, %s, %s)'
            values = (self.user_id, self.name, self.email, self.password, self.user_type, False)
            cursor.execute(sql, values)
            conn.commit()
            print(f"[INFO] User {self.name} registered successfully.")
        else:
            print("[ERROR] Invalid registration details.")

    def login(self, username, password):
        # Implementation for user login
        # Retrieve user information from the database based on user_id or email
        sql = 'SELECT * FROM User WHERE username = %s OR self.email = %s'
        values = (username, self.email)
        cursor.execute(sql, values)
        user_data = cursor.fetchone()

        if user_data and user_data[3] == password:  # Check if user exists and password matches
            # Update login status in the database
            sql_update_status = 'UPDATE User SET login_status = True WHERE user_id = %s'
            cursor.execute(sql_update_status, (user_data[0],))
            conn.commit()
            print(f"User {self.name} logged in successfully.")
            return True
        else:
            print("Invalid login credentials.")
            return False

    def update_profile(self):
        # Implementation for updating user profile
        # Check if the user is logged in
        if self.login():
            print("Choose the attribute you want to update:")
            print("1. Name")
            print("2. Email")
            print("3. Password")
            choice = input("Enter the number of your choice: ")

            if choice == "1":
                new_name = input("Enter your new name: ")
                # Update name in the database
                sql_update_name = 'UPDATE User SET name = %s WHERE user_id = %s'
                cursor.execute(sql_update_name, (new_name, self.user_id))
                conn.commit()
                print("Name updated successfully.")
            elif choice == "2":
                new_email = input("Enter your new email: ")
                # Validate the new email
                if self.validate_email():
                    # Update email in the database
                    sql_update_email = 'UPDATE User SET email = %s WHERE user_id = %s'
                    cursor.execute(sql_update_email, (new_email, self.user_id))
                    conn.commit()
                    print("Email updated successfully.")
                else:
                    print("Invalid email format. Update canceled.")
            elif choice == "3":
                new_password = input("Enter your new password: ")
                # Validate the new password
                if self.validate_password():
                    # Update password in the database
                    sql_update_password = 'UPDATE User SET password = %s WHERE user_id = %s'
                    cursor.execute(sql_update_password, (new_password, self.user_id))
                    conn.commit()
                    print("Password updated successfully.")
                else:
                    print("Invalid password format. Update canceled.")
            else:
                print("Invalid choice. Update canceled.")

    def view_appointments(self, past_appointments=False):
        # Implementation for viewing past or future appointments for the user
        # Check if the user is logged in
        if self.login():
            current_datetime = datetime.now()

            # Determine the SQL condition based on whether to retrieve past or future appointments
            condition = '<' if past_appointments else '>='

            # Fetch appointments for the user from the database based on the specified condition
            sql = f'SELECT * FROM Appointment WHERE user_id = %s AND date_time {condition} %s'
            values = (self.user_id, current_datetime)
            cursor.execute(sql, values)
            appointments = cursor.fetchall()

            if appointments:
                time_frame = 'Past' if past_appointments else 'Future'
                print(f"{time_frame} Appointments for {self.name}:")
                for appointment in appointments:
                    print(f"Appointment ID: {appointment[0]}, Clinic ID: {appointment[1]}, "
                          f"Date and Time: {appointment[3]}, Status: {appointment[4]}")
            else:
                time_frame = 'past' if past_appointments else 'future'
                print(f"No {time_frame} appointments found for {self.name}.")

class Clinic:
    def __init__(self, clinic_id, name, address, contact_info, services, availability):
        self.clinic_id = clinic_id
        self.name = name
        self.address = address
        self.contact_info = contact_info
        self.services = services
        self.availability = availability

    def validate_clinic_id(self):
        # Validate clinic_id using regular expression
        return re.match(r'^[a-zA-Z0-9]{5,20}$', self.clinic_id) is not None

    def validate_name(self):
        # Validate name using regular expression
        return re.match(r'^[a-zA-Z0-9 ]{5,50}$', self.name) is not None

    def validate_address(self):
        # Validate address using regular expression
        return re.match(r'^[a-zA-Z0-9, ]{5,100}$', self.address) is not None

    def validate_contact_info(self):
        # Validate contact_info using regular expression
        return re.match(r'^[0-9]{10}$', self.contact_info) is not None

    def add_clinic(self):
        # Implementation for adding a new clinic with validation checks
        if self.validate_clinic_id() and self.validate_name() and self.validate_address() and self.validate_contact_info():
            # Insert clinic into the database
            sql = 'INSERT INTO Clinic (clinic_id, name, address, contact_info) VALUES (%s, %s, %s, %s)'
            values = (self.clinic_id, self.name, self.address, self.contact_info)
            cursor.execute(sql, values)
            conn.commit()
            print(f"Clinic {self.name} added successfully.")
        else:
            print("Invalid clinic details. Clinic not added.")

    def update_clinic_info(self):
        # Implementation for updating clinic information
        # Check if the clinic exists in the database
        sql_check_clinic = 'SELECT * FROM Clinic WHERE clinic_id = %s'
        cursor.execute(sql_check_clinic, (self.clinic_id,))
        clinic_data = cursor.fetchone()

        if clinic_data:
            print("Choose the attribute you want to update:")
            print("1. Name")
            print("2. Address")
            print("3. Contact Info")
            choice = input("Enter the number of your choice: ")

            if choice == "1":
                new_name = input("Enter the new name: ")
                # Update clinic name in the database
                sql_update_name = 'UPDATE Clinic SET name = %s WHERE clinic_id = %s'
                cursor.execute(sql_update_name, (new_name, self.clinic_id))
                conn.commit()
                print("Clinic name updated successfully.")
            elif choice == "2":
                new_address = input("Enter the new address: ")
                # Validate the new address
                if self.validate_address():
                    # Update clinic address in the database
                    sql_update_address = 'UPDATE Clinic SET address = %s WHERE clinic_id = %s'
                    cursor.execute(sql_update_address, (new_address, self.clinic_id))
                    conn.commit()
                    print("Clinic address updated successfully.")
                else:
                    print("Invalid address format. Update canceled.")
            elif choice == "3":
                new_contact_info = input("Enter the new contact info: ")
                # Validate the new contact info
                if self.validate_contact_info():
                    # Update clinic contact info in the database
                    sql_update_contact_info = 'UPDATE Clinic SET contact_info = %s WHERE clinic_id = %s'
                    cursor.execute(sql_update_contact_info, (new_contact_info, self.clinic_id))
                    conn.commit()
                    print("Clinic contact info updated successfully.")
                else:
                    print("Invalid contact info format. Update canceled.")
            else:
                print("Invalid choice. Update canceled.")
        else:
            print("Clinic not found in the database. Update canceled.")

    def set_availability(self):
        # Implementation for setting clinic availability
        # Extract day and time from availability string
        day, time_slot = self.availability.split(', ')
        # Insert availability into the ClinicAvailability table
        sql = 'INSERT INTO ClinicAvailability (clinic_id, day, time_slot) VALUES (%s, %s, %s)'
        values = (self.clinic_id, day, time_slot)
        cursor.execute(sql, values)
        conn.commit()
        print(f"Clinic availability set successfully for {self.name}.")

    def view_appointments(self):
        # Implementation for viewing appointments for the clinic
        # Check if the clinic exists in the database
        sql_check_clinic = 'SELECT * FROM Clinic WHERE clinic_id = %s'
        cursor.execute(sql_check_clinic, (self.clinic_id,))
        clinic_data = cursor.fetchone()

        if clinic_data:
            # Fetch appointments for the clinic from the database
            sql = 'SELECT * FROM Appointment WHERE clinic_id = %s'
            cursor.execute(sql, (self.clinic_id,))
            appointments = cursor.fetchall()

            if appointments:
                print(f"Appointments for Clinic {self.name}:")
                for appointment in appointments:
                    print(f"Appointment ID: {appointment[0]}, User ID: {appointment[2]}, "
                          f"Date and Time: {appointment[3]}, Status: {appointment[4]}")
            else:
                print(f"No appointments found for Clinic {self.name}.")
        else:
            print("Clinic not found in the database. Unable to view appointments.")

class Appointment:
    def __init__(self, appointment_id, clinic_id, user_id, date_time, status):
        self.appointment_id = appointment_id
        self.clinic_id = clinic_id
        self.user_id = user_id
        self.date_time = date_time
        self.status = status

    def register_appointment(self, user, clinic, date_time):
        # Implementation for registering a new appointment
        # Check if the user and clinic are logged in
        if user.login() and clinic.login():
            # Check if the appointment slot is available
            if self.is_appointment_slot_available(clinic.clinic_id, date_time):
                # Insert appointment into the database
                sql = 'INSERT INTO Appointment (clinic_id, user_id, date_time, status) VALUES (%s, %s, %s, %s)'
                values = (clinic.clinic_id, user.user_id, date_time, 'Scheduled')
                cursor.execute(sql, values)
                conn.commit()
                print(f"Appointment scheduled successfully for {user.name} at {clinic.name}.")
            else:
                print("Appointment slot is not available. Please choose another time.")
        else:
            print("User or clinic not logged in. Appointment registration failed.")

    def cancel_appointment(self, user, appointment_id):
        # Implementation for canceling an appointment
        # Check if the user is logged in
        if user.login():
            # Check if the appointment exists and belongs to the logged-in user
            sql_check_appointment = 'SELECT * FROM Appointment WHERE appointment_id = %s AND user_id = %s'
            cursor.execute(sql_check_appointment, (appointment_id, user.user_id))
            appointment_data = cursor.fetchone()

            if appointment_data:
                # Update appointment status to 'Canceled' in the database
                sql_cancel_appointment = 'UPDATE Appointment SET status = %s WHERE appointment_id = %s'
                cursor.execute(sql_cancel_appointment, ('Canceled', appointment_id))
                conn.commit()
                print(f"Appointment {appointment_id} canceled successfully.")
            else:
                print("Appointment not found or does not belong to the logged-in user.")
        else:
            print("User not logged in. Appointment cancellation failed.")

    def reschedule_appointment(self, user, appointment_id, new_date_time):
        # Implementation for rescheduling an appointment
        # Check if the user is logged in
        if user.login():
            # Check if the appointment exists and belongs to the logged-in user
            sql_check_appointment = 'SELECT * FROM Appointment WHERE appointment_id = %s AND user_id = %s'
            cursor.execute(sql_check_appointment, (appointment_id, user.user_id))
            appointment_data = cursor.fetchone()

            if appointment_data:
                # Check if the new appointment slot is available
                if self.is_appointment_slot_available(appointment_data[1], new_date_time):
                    # Update appointment date_time in the database
                    sql_reschedule_appointment = 'UPDATE Appointment SET date_time = %s WHERE appointment_id = %s'
                    cursor.execute(sql_reschedule_appointment, (new_date_time, appointment_id))
                    conn.commit()
                    print(f"Appointment {appointment_id} rescheduled successfully.")
                else:
                    print("New appointment slot is not available. Please choose another time.")
            else:
                print("Appointment not found or does not belong to the logged-in user.")
        else:
            print("User not logged in. Appointment rescheduling failed.")

    def is_appointment_slot_available(self, clinic_id, date_time):
        # Check if the appointment slot is available for the specified clinic and date_time
        sql_check_availability = 'SELECT * FROM ClinicAvailability WHERE clinic_id = %s AND day = %s AND time_slot = %s'
        values = (clinic_id, date_time.strftime('%A'), date_time.strftime('%I:%M %p'))
        cursor.execute(sql_check_availability, values)
        availability_data = cursor.fetchone()

        return availability_data is not None

class Notification:
    def __init__(self, notification_id, user_id, message, date_time):
        self.notification_id = notification_id
        self.user_id = user_id
        self.message = message
        self.date_time = date_time

    def send_notification(self, user, message):
        # Implementation for sending a notification
        # Check if the user is logged in
        if user.login():
            # Insert notification into the database
            sql = 'INSERT INTO Notification (user_id, message, date_time) VALUES (%s, %s, %s)'
            values = (user.user_id, message, datetime.now())
            cursor.execute(sql, values)
            conn.commit()
            print(f"Notification sent to {user.name}: {message}")
            return True
        else:
            print("User not logged in. Notification sending failed.")
            return False