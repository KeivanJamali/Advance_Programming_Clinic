import re
from user import User
from secretary import Secretary
from customer import Customer
import Builder

Builder.main()


def get_phone_number():
    """
    Prompts the user to enter a phone number, validates the input according to a specific pattern, and returns the phone number if it is valid.
    """
    phone_number = input("Enter your phone number:")
    pattern = r"^\d{11}$"
    if re.match(pattern, phone_number):
        print("[REPLY] Valid phone number")
        return phone_number
    else:
        print("[REPLY] Invalid phone number")


def get_first_name():
    """
    Asks the user to enter their first name and returns the input as a string.
    """
    first_name = input("Enter your first number:")
    return first_name


def get_last_name():
    """
    Function to prompt the user to enter their last name and return the input as the last name.
    """
    last_name = input("Enter your last name:")
    return last_name


def get_password():
    """
    Takes user input for a password and checks if it meets the specified criteria.
    requires at least one lowercase letter
    requires at least one uppercase letter
    requires at least one digit
    requires at least one special character from the given set: @$!%*?&

    Parameters:
        None

    Returns:
        str: The valid password entered by the user.

    Raises:
        None
    """
    password = input("Enter your password:")
    if re.match(r"^(?=.*[a-zA-Z0-9]).{4,}$", password):
        print("[REPLY] Valid password")
        return password
    else:
        print("[REPLY] Invalid password")


def get_email():
    """
    Prompts the user to enter an email address, validates it, and returns it if valid.
    """
    email = input(
        "Enter your email address(if you don't want to enter one, please enter 'N'):"
    )
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, email) or email == "N":
        print("[REPLY] Valid email address")
        return email
    else:
        print("[REPLY] Invalid email address")


def choose_user_type():
    """
    Prompts the user to enter their user type and returns the user type if it is "Secretary" or "Customer".
    """
    user_type = input("Enter your user type:\n1. Secretary\n2. Customer\n")
    if user_type == "1" or user_type == "2":
        return user_type


def register_or_login(user):
    """
    This function allows a user to register or login. It takes a 'user' object as a parameter and returns the result of the registration or login attempt.
    """
    act = input("Register or login?")
    phone_number = None
    password = None
    if act == "Register" or act == "register":
        first_name = None
        last_name = None
        email = None
        user_type = None
        email_check = None
        while phone_number is None:
            phone_number = get_phone_number()
        while first_name is None:
            first_name = get_first_name()
        while last_name is None:
            last_name = get_last_name()
        while password is None:
            password = get_password()
        while email is None:
            email = get_email()
            email_check = email if email != "N" else None
        while user_type is None:
            user_type = choose_user_type()

        return user.register_user(
            first_name, last_name, password, phone_number, user_type, email_check
        )

    elif act == "Login" or act == "login":
        phone_number = get_phone_number()
        password = get_password()

        return user.login_user(password, phone_number)

    else:
        print("[REPLY] Invalid action. Try again!")


def main():
    """
    Main function for handling user and secretary interactions in the clinic system.
    """
    exit_ = False
    while not exit_:
        user = User()
        user = register_or_login(user)
        if user.user_type == "1":
            clinic_name = input("Enter clinic name:")
            address = input("Enter address:")
            try:
                secretary = Secretary(clinic_name, address, user.phone_number)
                if secretary.clinic is None:
                    print("[REPLY] Invalid clinic name or address. Try again!")
                    continue
            except:
                print("[REPLY] Invalid clinic name or address. Try again!")
                continue
            while not exit_:
                print("1- Add or Select Doctor")
                print("2- Update Clinic Profile")
                print("3- View Appointments for Clinic")
                print("4- View Profile")
                print("5- Exit")

                act_home_page = input("Enter your action number:")

                if act_home_page == "1":
                    phone_number = input("Enter phone number: ")
                    first_name = input("Enter first name: ")
                    last_name = input("Enter last name: ")
                    try:
                        secretary.add_or_select_doctor(phone_number, first_name, last_name)
                    except:
                        print("[REPLY] Invalid phone number or first name or last name. Try again!")
                        continue
                    while not exit_:
                        print("1- Update Doctor Profile")
                        print("2- add availability")
                        print("3- Edit appointments for Doctor")
                        print("4- View Schedule for Doctor")
                        print("5- Back")
                        print("6- Exit")

                        act_doctor_page = input("Enter your action number: ")

                        if act_doctor_page == "1":
                            new_first_name = input(
                                "Enter new first name (if you don't want to enter one, please enter 'N'): ")
                            new_last_name = input(
                                "Enter new last name (if you don't want to enter one, please enter 'N'): ")
                            new_phone_number = input(
                                "Enter new phone number (if you don't want to enter one, please enter 'N'):")
                            new_first_name = new_first_name if new_first_name != "N" else None
                            new_last_name = new_last_name if new_last_name != "N" else None
                            new_phone_number = new_phone_number if new_phone_number != "N" else None
                            try:
                                secretary.update_doctor_profile(new_first_name, new_last_name, new_phone_number)
                            except:
                                print("[REPLY] Invalid first name or last name or phone number. Try again!")
                                continue

                        elif act_doctor_page == "2":
                            new_date = input("Enter new date(yyyy/mm/dd): ")
                            new_time = input("Enter new time(hh:mm): ")
                            try:
                                secretary.add_or_select_doctor(phone_number, first_name, last_name, new_date, new_time)
                                print("[REPLY] Availability added successfully!")
                            except:
                                print("[REPLY] Invalid date or time. Try again!")
                                continue

                        elif act_doctor_page == "3":
                            old_date = input("Enter old date(yyyy/mm/dd): ")
                            old_time = input("Enter old time(hh:mm): ")
                            new_date = input("Enter new date(yyyy/mm/dd): ")
                            new_time = input("Enter new time(hh:mm): ")
                            try:
                                secretary.edit_appointments_for_doctor(old_date, old_time, new_date, new_time)
                            except:
                                print("[REPLY] Invalid date or time. Try again!")
                                continue

                        elif act_doctor_page == "4":
                            secretary.view_schedule_for_doctor()

                        elif act_doctor_page == "5":
                            break

                        elif act_doctor_page == "6":
                            exit_ = True
                            break

                        else:
                            print("[REPLY] Invalid action. Try again!")
                            continue

                elif act_home_page == "2":
                    new_clinic_name = input(
                        "Enter new clinic name (if you don't want to enter one, please enter 'N'): ")
                    new_address = input(
                        "Enter new address (if you don't want to enter one, please enter 'N'): ")
                    new_clinic_name = new_clinic_name if new_clinic_name != "N" else None
                    new_address = new_address if new_address != "N" else None
                    try:
                        secretary.update_clinic_profile(new_clinic_name, new_address)
                    except:
                        print("[REPLY] Invalid clinic name or address. Try again!")
                        continue

                elif act_home_page == "3":
                    secretary.view_appointments_for_clinic()

                elif act_home_page == "4":
                    print(secretary)

                elif act_home_page == "5":
                    exit_ = True
                    break

                else:
                    print("[REPLY] Invalid action. Try again!")
                    continue

        elif user.user_type == "2":
            customer = Customer(user.phone_number)
            while not exit_:
                print("1- Add Patient")
                print("2- Select Patient")
                print("3- Exit")
                act_home_page = input("Enter your action number: ")

                if act_home_page == "1":
                    first_name = input("Enter first name: ")
                    last_name = input("Enter last name: ")
                    phone_number = input("Enter phone number: ")
                    birthdate = input("Enter birth date(yyyy-mm-dd): ")
                    national_code = input("Enter national code: ")
                    email = input("Enter email (if you don't want to enter one, please enter 'N'): ")
                    email = email if email != "N" else None
                    try:
                        customer.add_patient(first_name, last_name, phone_number, birthdate, national_code, email)
                    except:
                        print(
                            "[REPLY] Invalid first name or last name or phone number or birth date or national code. Try again!")
                        continue

                elif act_home_page == "2":
                    while not exit_:
                        print("1- Current User as Patient")
                        print("2- Patient Other Than User")
                        print("3- Back")
                        print("3- Exit")
                        act_doctor_page = input("Enter your action number: ")

                        if act_doctor_page == "1":
                            customer.select_patient(user.phone_number)
                            print("[REPLY] Current User as Patient")

                        elif act_doctor_page == "2":
                            try:
                                phone_number_patient = input("Enter patient phone number: ")
                                customer.select_patient(phone_number_patient)
                            except:
                                print("[REPLY] Invalid patient phone number. Try again!")
                                continue

                        elif act_doctor_page == "3":
                            break

                        elif act_doctor_page == "4":
                            exit_ = True
                            break

                        else:
                            print("[REPLY] Invalid action. Try again!")
                            continue

                        while not exit_:
                            print("1- Update Patient Info")
                            print("2- Remove Patient")
                            print("3- View Current Appointments for Patient")
                            print("4- View Appointments History for Patient")
                            print("5- Add Appointment")
                            print("6- Remove Appointment")
                            print("7- Reschedule Appointment")
                            print("8- Back")
                            print("9- Exit")
                            act_patient_page = input("Enter your action number: ")

                            if act_patient_page == "1":
                                new_phone_number = input(
                                    "Enter new phone number (if you don't want to enter one, please enter 'N'):")
                                new_first_name = input(
                                    "Enter new first name (if you don't want to enter one, please enter 'N'): ")
                                new_last_name = input(
                                    "Enter new last name (if you don't want to enter one, please enter 'N'): ")
                                new_email = input(
                                    "Enter new phone number (if you don't want to enter one, please enter 'N'):")
                                new_birthday = input(
                                    "Enter new first name (if you don't want to enter one, please enter 'N'): ")
                                new_national = input(
                                    "Enter new last name (if you don't want to enter one, please enter 'N'): ")

                                new_phone_number = new_phone_number if new_phone_number != "N" else None
                                new_first_name = new_first_name if new_first_name != "N" else None
                                new_last_name = new_last_name if new_last_name != "N" else None
                                new_email = new_email if new_email != "N" else None
                                new_birthday = new_birthday if new_birthday != "N" else None
                                new_national = new_national if new_national != "N" else None

                                try:
                                    customer.update_patient_info(new_phone_number, new_first_name, new_last_name,
                                                                 new_email,
                                                                 new_birthday, new_national)
                                except:
                                    print(
                                        "[REPLY] Invalid phone number or first name or last name or email or birthday or national code. Try again!")
                                    continue
                                print("[REPLY] Patient Info Updated")

                            elif act_patient_page == "2":
                                customer.remove_patient()
                                print("[REPLY] Patient Removed")

                            elif act_patient_page == "3":
                                customer.view_current_appointments()
                                print("[REPLY] Current Appointments")

                            elif act_patient_page == "4":
                                customer.view_appointments_history()
                                print("[REPLY] Appointments History")

                            elif act_patient_page == "5":
                                doctor_phone_number = input("Enter phone number for doctor: ")
                                clinic_name = input("Enter clinic name: ")
                                date = input("Enter date(yyyy-mm-dd): ")
                                time = input("Enter time(hh-mm): ")
                                try:
                                    customer.add_appointment(doctor_phone_number, clinic_name, date, time)
                                except:
                                    print(
                                        "[REPLY] Invalid doctor phone number or clinic name or date or time. Try again!")
                                    continue

                            elif act_patient_page == "6":
                                date = input("Enter date(yyyy-mm-dd): ")
                                time = input("Enter time(hh-mm): ")
                                try:
                                    customer.cancel_appointment(date, time)
                                except:
                                    print("[REPLY] Invalid date or time. Try again!")
                                    continue

                            elif act_patient_page == "7":
                                old_date = input("Enter old date(yyyy-mm-dd): ")
                                old_time = input("Enter old time(hh-mm): ")
                                new_date = input("Enter new date(yyyy-mm-dd): ")
                                new_time = input("Enter new time(hh-mm): ")
                                try:
                                    customer.reschedule_appointment(old_date, old_time, new_date, new_time)
                                except:
                                    print("[REPLY] Invalid old date or old time or new date or new time. Try again!")
                                    continue

                            elif act_patient_page == "8":
                                break

                            elif act_patient_page == "9":
                                exit_ = True
                                break

                elif act_home_page == "3":
                    exit_ = True
                    break


main()

from DATABASE import establish_connection


class User:
    def __init__(self):
        """
        Constructor for initializing the attributes:
        first_name, last_name, password, phone_number,
        user_type, and email.
        """
        self.first_name = None
        self.last_name = None
        self.password = None
        self.phone_number = None
        self.user_type = None
        self.email = None

    def register_user(self, first_name, last_name, password, phone_number, user_type, email=None):
        """
        Register a new user with the provided information.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            password (str): The password of the user.
            phone_number (str): The phone number of the user.
            user_type (str): The type of user.
            email (str, optional): The email of the user (default is None).

        Returns:
            User: The registered user object.
        """
        connection = establish_connection()
        cursor = connection.cursor()

        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.phone_number = phone_number
        self.user_type = user_type
        self.email = email

        # Check if user already exists
        query = "SELECT COUNT(*) FROM user_table WHERE phone_number = %s"
        cursor.execute(query, (self.phone_number,))
        result = cursor.fetchone()

        if result[0] > 0:
            print("[Wrong] User with the given phone number already exists.")
            return

        # Insert new user into the database
        query = "INSERT INTO user_table (first_name, last_name, phone_number, password, user_type, email) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query,
                       (self.first_name, self.last_name, self.phone_number, self.password, self.user_type, self.email))
        print("[INFO] Registered")
        query = """
        SELECT user_id 
        FROM user_table
        WHERE phone_number = %s
        """
        values = (self.phone_number,)
        cursor.execute(query, values)
        self.user_id = cursor.fetchone()[0]

        connection.commit()
        cursor.close()
        connection.close()
        return self

    def login_user(self, password, phone_number):
        """
        Logs in a user using the provided password and phone number.

        Parameters:
            password (str): The password of the user.
            phone_number (str): The phone number of the user.

        Returns:
            self: The updated user object.
        """
        connection = establish_connection()
        cursor = connection.cursor()

        self.password = password
        self.phone_number = phone_number

        # Check if user exists in the database
        query = "SELECT * FROM user_table WHERE phone_number = %s"
        cursor.execute(query, (self.phone_number,))
        result = cursor.fetchone()

        if result:
            # User exists, assign database values to object attributes
            self.user_id = result[0]
            self.first_name = result[1]
            self.last_name = result[2]
            self.email = result[3] if result[3] else None
            self.user_type = result[6]

        else:
            print("[Wrong] User does not exist.")

        cursor.close()
        connection.close()
        return self

from DATABASE import establish_connection
import datetime
from notification import Notification


class Patient(Notification):
    def __init__(self):
        # Initialize patient attributes
        super().__init__()
        self.patient_id = None
        self.first_name = None
        self.last_name = None
        self.phone_number = None
        self.birth_date = None
        self.national_code = None
        self.email = None

    def select_patient(self, phone_number):
        connection = establish_connection()
        cursor = connection.cursor()

        try:
            # Check if the patient with the provided phone number already exists
            query_patient = "SELECT * FROM patient_table WHERE phone_number = %s"
            cursor.execute(query_patient, (phone_number,))
            existing_patient = cursor.fetchone()

            if existing_patient:
                # If patient exists, set attributes based on existing data
                self.patient_id, self.phone_number, self.first_name, self.last_name, self.birth_date, self.national_code, self.email = existing_patient
                print("[INFO] Successfully selected patient")
        except Exception:
            print("[ERROR] Invalid phone number.")

    def add_patient(self, first_name, last_name, phone_number, birthdate, national_code, email, user_phone):
        """
        Add a new patient to the database.

        Parameters:
            first_name (str): The first name of the patient.
            last_name (str): The last name of the patient.
            phone_number (str): The phone number of the patient.
            birthdate (str): The birthdate of the patient.
            national_code (str): The national code of the patient.
            email (str): The email address of the patient.
            user_phone (str): The user's phone number.

        Returns:
            None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Check if the patient with the provided phone number already exists
        query_patient = "SELECT * FROM patient_table WHERE phone_number = %s"
        cursor.execute(query_patient, (phone_number,))
        existing_patient = cursor.fetchone()

        if existing_patient:
            # If patient exists, set attributes based on existing data
            self.patient_id, self.phone_number, self.first_name, self.last_name, self.birth_date, self.national_code, self.email = existing_patient
            print("[INFO] Patient with the provided phone number already exists.")
        else:
            # Insert new patient if not already exists
            insert_patient_query = """
                INSERT INTO patient_table (first_name, last_name, phone_number, birthdate, national_code, email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            patient_values = (first_name, last_name, phone_number, birthdate, national_code, email)
            cursor.execute(insert_patient_query, patient_values)

            # Get patient_id
            try:
                query_patient_id = "SELECT * FROM patient_table WHERE phone_number = %s"
                cursor.execute(query_patient_id, (phone_number,))
                # self.patient_id = cursor.fetchone()[0]
                self.patient_id, self.phone_number, self.first_name, self.last_name, self.birth_date, self.national_code, self.email = cursor.fetchone()
                query = """SELECT user_id FROM user_table WHERE phone_number = %s"""
                values = (user_phone,)
                cursor.execute(query, values)
                user_id = cursor.fetchone()[0]
            except:
                print("[ERROR] user does not exist.")
                return

            # Insert into user_patient table
            insert_user_patient_query = """
                INSERT INTO customer_patient (user_id, patient_id)
                VALUES (%s, %s)
            """
            user_patient_values = (user_id, self.patient_id)
            cursor.execute(insert_user_patient_query, user_patient_values)

            connection.commit()
            print("[INFO] Patient added successfully.")

        cursor.close()
        connection.close()

    def update_patient_info(self, new_phone_number=None, new_first_name=None, new_last_name=None, new_birthdate=None,
                            new_email=None, new_national_code=None):
        """
        Update the patient's information in the database.

        Parameters:
            new_first_name (str): The new first name of the patient. Default is None.
            new_last_name (str): The new last name of the patient. Default is None.
            new_phone_number (str): The new phone number of the patient. Default is None.
            new_email (str): The new email of the patient. Default is None.
            new_national_code (str): The new national code of the patient. Default is None.
            new_birthdate (str): The new birthdate of the patient
        Returns:
            None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Check if a patient with the new phone number already exists
        existing_patient_query = "SELECT * FROM patient_table WHERE phone_number = %s"
        cursor.execute(existing_patient_query, (new_phone_number,))
        existing_patient = cursor.fetchone()

        if existing_patient:
            # If patient with the new phone number already exists, do not update
            print("[INFO] A patient with the provided phone number already exists.")
            return

        update_fields = []
        values = []

        # Build the update query based on provided new information
        if new_phone_number:
            update_fields.append("phone_number = %s")
            values.append(new_phone_number)
        if new_first_name:
            update_fields.append("first_name = %s")
            values.append(new_first_name)
        if new_last_name:
            update_fields.append("last_name = %s")
            values.append(new_last_name)
        if new_birthdate:
            update_fields.append("birthdate = %s")
        if new_national_code:
            update_fields.append("national_code = %s")
            values.append(new_national_code)
        if new_email:
            update_fields.append("email = %s")
            values.append(new_email)

        if not update_fields:
            # If no fields provided for update, print info and return
            print("[INFO] No fields provided for update.")
            return

        values.append(self.phone_number)

        set_clause = ", ".join(update_fields)
        query = f"UPDATE patient_table SET {set_clause} WHERE phone_number = %s"

        # Execute the update query
        cursor.execute(query, values)
        rows_affected = cursor.rowcount
        connection.commit()

        cursor.close()
        connection.close()

        if rows_affected == 0:
            # If no patient with the provided phone number exists, print info
            print("[INFO] No patient with the provided phone number exists.")
        else:
            # If update successful, print info and update attributes
            print("[INFO] Patient profile updated successfully.")
            if new_first_name:
                self.first_name = new_first_name
            if new_last_name:
                self.last_name = new_last_name
            if new_phone_number:
                self.phone_number = new_phone_number

    def remove_patient(self):
        """
        Remove the patient from the database.

        Returns:
            None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Execute the delete query
        delete_query = "DELETE FROM patient_table WHERE patient_id = %s"
        cursor.execute(delete_query, (self.patient_id,))

        connection.commit()

        cursor.close()
        connection.close()

        print("[INFO] Patient removed from the database.")

    def view_current_appointments(self):
        """
        Show the current appointments for the patient.

        Returns:
            None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Query to retrieve current appointments for the patient
        query = """
            SELECT a.appointment_date, a.appointment_time, d.first_name, d.last_name, c.clinic_name
            FROM calendar_table a
            JOIN doctor_table d ON a.doctor_id = d.doctor_id
            JOIN clinic_table c ON a.clinic_id = c.clinic_id
            WHERE a.patient_id = %s AND a.appointment_date >= %s
            ORDER BY a.appointment_date, a.appointment_time
        """
        current_date = datetime.date.today()
        cursor.execute(query, (self.patient_id, current_date))
        appointments = cursor.fetchall()

        if not appointments:
            # If no current appointments, print info and return
            print("[INFO] No current appointments for the patient.")
            return

        current_appointments = []
        for appointment in appointments:
            # Format appointment data and append to current_appointments list
            date, time, doctor_first_name, doctor_last_name, clinic_name = appointment
            formatted_date = date.strftime("%Y/%m/%d")
            formatted_time = datetime.datetime(1, 1, 1) + time
            formatted_time = formatted_time.strftime("%H:%M")

            current_appointments.append({
                "Date": formatted_date,
                "Time": formatted_time,
                "Doctor Name": f"{doctor_first_name} {doctor_last_name}",
                "Clinic Name": clinic_name
            })
        cursor.close()
        connection.close()
        self.make_table_current_appointment(self, current_appointments)

    def view_appointments_history(self):
        """
        Show the appointment history for the patient.

        Returns:
            None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Query to retrieve appointment history for the patient
        query = """
        SELECT a.appointment_date, a.appointment_time, d.first_name, d.last_name, c.clinic_name
        FROM calendar_table a
        JOIN doctor_table d ON a.doctor_id = d.doctor_id
        JOIN clinic_table c ON a.clinic_id = c.clinic_id
        WHERE a.patient_id = %s AND a.appointment_date < %s
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """
        current_date = datetime.date.today()
        cursor.execute(query, (self.patient_id, current_date))
        appointments = cursor.fetchall()

        if not appointments:
            # If no appointment history, print info and return
            print("[INFO] No appointment history for the patient.")
            return

        appointments_history = []
        for appointment in appointments:
            # Format appointment data and append to appointments_history list
            date, time, doctor_first_name, doctor_last_name, clinic_name = appointment
            formatted_date = date.strftime("%Y/%m/%d")
            formatted_time = datetime.datetime(1, 1, 1) + time
            formatted_time = formatted_time.strftime("%H:%M")

            appointments_history.append([
                formatted_date,
                formatted_time,
                f"{doctor_first_name} {doctor_last_name}",
                clinic_name
            ])

        cursor.close()
        connection.close()

        # Print the appointment history using tabulate
        self.make_table_appointment(appointments_history)

from patient import Patient
from appointment import Appointment
from DATABASE import establish_connection


class Customer:
    def __init__(self, phone_number: str):
        # Initialize instances of Patient, Secretary, and Appointment classes
        self.phone_number = phone_number
        self.patient = Patient()
        # self.secretary = Secretary()
        self.appointment = Appointment()

        connection = establish_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM user_table WHERE phone_number = %s "
        values = [self.phone_number]
        cursor.execute(query, values)
        self.user_id, self.first_name, self.last_name, self.email, self.phone_number, self.password, self.user_type = cursor.fetchone()

    def select_patient(self, phone_number: str):
        try:
            connection = establish_connection()
            cursor = connection.cursor()
            query = """SELECT user_id FROM user_table WHERE phone_number = %s"""
            values = (self.phone_number,)
            cursor.execute(query, values)
            user_id = cursor.fetchone()[0]
        except:
            print("[ERROR] There is no user with that phone]")
            return None

        self.patient.select_patient(phone_number)

        query = "SELECT * FROM customer_patient WHERE user_id = %s AND patient_id = %s"
        cursor.execute(query, (user_id, self.patient.patient_id))
        user_patient_entry = cursor.fetchone()
        if user_patient_entry:
            print("[INFO] Successfully selected patient")
        else:
            self.patient = None
            print("[ERROR] Who are you bitch?")

    def add_patient(self, first_name, last_name, phone_number, birthdate, national_code, email):
        # Delegate the add_patient functionality to the Patient class
        self.patient.add_patient(first_name, last_name, phone_number, birthdate, national_code, email,
                                 self.phone_number)

    def update_patient_info(self, new_phone_number=None, new_first_name=None, new_last_name=None,
                            new_email=None, new_birthday=None, new_national_code=None):
        # Delegate the update_patient_info functionality to the Patient class
        self.patient.update_patient_info(new_phone_number, new_first_name, new_last_name, new_email, new_birthday,
                                         new_national_code)

    def remove_patient(self):
        # Check if the user_phone and phone_number exist in the user_patient table
        self.patient.remove_patient()

    def view_current_appointments(self):
        # Delegate the view_current_appointments functionality to the Patient class
        return self.patient.view_current_appointments()

    def view_appointments_history(self):
        # Delegate the view_appointments_history functionality to the Patient class
        return self.patient.view_appointments_history()

    def add_appointment(self, doctor_phone_number, clinic_name, date, time):
        # Delegate the add_appointment functionality to the Appointment class
        self.appointment.add_appointment(doctor_phone_number, clinic_name, self.patient.phone_number, date, time)

    def cancel_appointment(self, date, time):
        # Delegate the cancel_appointment functionality to the Appointment class
        self.appointment.cancel_appointment(self.patient.phone_number, date, time)

    def reschedule_appointment(self, old_date, old_time, new_date, new_time):
        # Delegate the reschedule_appointment functionality to the Appointment class
        self.appointment.reschedule_appointment(self.patient.phone_number, old_date, old_time, new_date, new_time)

from DATABASE import establish_connection
import datetime
from appointment import Appointment


class Doctor:
    def __init__(self, phone_number: str, first_name: str, last_name: str) -> None:
        """
        Initializes a new instance of the class.

        Parameters:
            phone_number (str): The phone number of the Doctor.
            first_name (str): The first name of the Doctor.
            last_name (str): The last name of the Doctor.

        Returns:
            None
        """
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.doctor_id = None

    def save(self) -> None:
        """
        Saves the current Doctor to the database(doctor_table).

        Parameters:
            None

        Returns:
            None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Check if doctor with the provided phone number already exists
        query = """
        SELECT doctor_id, first_name, last_name FROM doctor_table
        WHERE phone_number = %s
        """

        cursor.execute(query, (self.phone_number,))
        existing_doctor = cursor.fetchone()

        if existing_doctor:
            self.doctor_id, self.first_name, self.last_name = existing_doctor
            print("[Wrong] Doctor with the provided phone number already exists.")
            print(
                f"[INFO] Doctor with phone number: {self.phone_number} and name: {self.first_name} {self.last_name} SELECTED!")
        else:
            # Insert new doctor if not already exists
            insert_query = """
            INSERT INTO doctor_table (first_name, last_name, phone_number)
            VALUES (%s, %s, %s)
            """
            values = (self.first_name, self.last_name, self.phone_number)

            cursor.execute(insert_query, values)

            # Get doctor_id
            query = """
            SELECT doctor_id FROM doctor_table
            WHERE phone_number = %s
            """

            cursor.execute(query, (self.phone_number,))
            self.doctor_id = cursor.fetchone()[0]

            connection.commit()
            print("[INFO] Doctor added successfully.")

        cursor.close()
        connection.close()

    def update_doctor_profile(self, new_first_name: str = None, new_last_name: str = None,
                              new_phone_number: str = None) -> None:
        """
        Updates the profile of the doctor in the database(doctor_table). You can change each one of them you like to change.

        :param new_first_name: (str) The new first name of the doctor. Default is None.
        :param new_last_name: (str) The new last name of the doctor. Default is None.
        :param new_phone_number: (str) The new phone number of the doctor. Default is None.

        :return: None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        existing_doctor_query = """
        SELECT * FROM doctor_table WHERE phone_number = %s
        """
        cursor.execute(existing_doctor_query, (new_phone_number,))
        existing_doctor = cursor.fetchone()

        if existing_doctor:
            print("[Wrong] A doctor with the provided phone number already exists.")
            return

        update_fields = []
        values = []

        if new_first_name:
            update_fields.append("first_name = %s")
            values.append(new_first_name)
        if new_last_name:
            update_fields.append("last_name = %s")
            values.append(new_last_name)
        if new_phone_number:
            update_fields.append("phone_number = %s")
            values.append(new_phone_number)

        if not update_fields:
            print("[Wrong] No fields provided for update.")
            return

        values.append(self.phone_number)

        set_clause = ", ".join(update_fields)
        query = f"""
        UPDATE doctor_table
        SET {set_clause}
        WHERE phone_number = %s
        """

        cursor.execute(query, values)
        rows_affected = cursor.rowcount
        connection.commit()

        cursor.close()
        connection.close()

        if rows_affected == 0:
            print("[Wrong] No doctor with the provided phone number exists.")
        else:
            print("[INFO] Doctor profile updated successfully.")
            if new_phone_number:
                self.phone_number = new_phone_number
            if new_first_name:
                self.first_name = new_first_name
            if new_last_name:
                self.last_name = new_last_name

    def view_doctor_schedule(self) -> list:
        """
        Retrieves the schedule of appointments for a specific doctor.

        Returns:
            list: A list of dictionaries containing the details of each appointment. Each dictionary has the following keys:
                - date (str): The formatted date of the appointment(YYYY/MM/DD).
                - time (str): The formatted time of the appointment(HH:MM).
                - clinic (str): The name of the clinic where the appointment is scheduled.
                - patient_name (str): The full name of the patient.
                - patient_phone_number (str): The phone number of the patient.
        """
        connection = establish_connection()
        cursor = connection.cursor()

        query = """
        SELECT appointment_date, appointment_time, clinic_id, patient_id
        FROM calendar_table
        WHERE doctor_id = %s
        AND canceled = %s
        """

        cursor.execute(query, (self.doctor_id, False))
        appointments = cursor.fetchall()

        if not appointments:
            print("[INFO] No appointments scheduled for this doctor.")
            return

        doctor_schedule = []
        for appointment in appointments:
            date, time, clinic_id, patient_id = appointment
            formatted_date = date.strftime("%Y/%m/%d")
            formatted_time = datetime.datetime(1, 1, 1) + time
            formatted_time = formatted_time.strftime("%H:%M")

            query = """
            SELECT clinic_name
            FROM clinic_table
            WHERE clinic_id = %s
            """
            cursor.execute(query, (clinic_id,))
            clinic_name = cursor.fetchone()[0]

            query = """
            SELECT phone_number, first_name, last_name
            FROM patient_table
            WHERE patient_id = %s
            """
            cursor.execute(query, (patient_id,))
            patient_phone_number, patient_first_name, patient_last_name = cursor.fetchone()

            doctor_schedule.append({"date": formatted_date, "time": formatted_time, "clinic": clinic_name,
                                    "patient_name": patient_first_name + " " + patient_last_name,
                                    "patient_phone_number": patient_phone_number})

        cursor.close()
        connection.close()

        return doctor_schedule

    def edit_appointments(self, old_date: str, old_time: str, new_date: str, new_time: str, clinic_name: str) -> None:
        """
        Edit appointments by rescheduling them to a new date and time.

        Parameters:
            - old_date (str): The original date of the appointment(yyyy/mm/dd).
            - old_time (str): The original time of the appointment(hh:mm).
            - new_date (str): The new date for rescheduling the appointment(yyyy/mm/dd).
            - new_time (str): The new time for rescheduling the appointment(hh:mm).
            - clinic_name (str): The name of the clinic where the appointment is scheduled.

        Returns:
            None

        Raises:
            None
        """
        schedule = self.view_doctor_schedule()
        if not schedule:
            return
        schedule = [x for x in schedule if
                    x["date"] == old_date and x["time"] == old_time and x["clinic"] == clinic_name]
        if not schedule:
            print("[Wrong] Appointment not found.")
            return
        patient_phone_number = schedule[0]["patient_phone_number"]
        appointment = Appointment()
        appointment.reschedule_appointment(patient_phone_number=patient_phone_number, old_date=old_date,
                                           old_time=old_time, new_date=new_date, new_time=new_time)

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        Returns:
            str: The string representation of the object.
        """
        return f"{self.first_name} {self.last_name} {self.phone_number}"

from DATABASE import establish_connection
import datetime


class Clinic:
    def __init__(self, clinic_name: str, address: str, secretary_phone_number: str) -> None:
        """
        Initialize the Clinic object with the given clinic name, address, and secretary phone number.

        Parameters:
            clinic_name (str): The name of the clinic.
            address (str): The address of the clinic.
            secretary_phone_number (str): The phone number of the clinic's secretary(11 digits).

        Returns:
            None
        """
        self.clinic_name = clinic_name
        self.address = address
        self.secretary_phone_number = secretary_phone_number
        self.clinic_id = None

    def save(self) -> None:
        """
        Saves the current clinic instance to the database.

        Parameters:
            None

        Returns:
            None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Check if doctor with the provided phone number already exists
        query = """
                SELECT clinic_id, clinic_name, address, secretary_phone_number
                FROM clinic_table
                WHERE clinic_name = %s
                """

        cursor.execute(query, (self.clinic_name,))
        existing_clinic = cursor.fetchone()

        if existing_clinic:
            self.clinic_id, self.clinic_name, self.address, self.secretary_phone_number = existing_clinic
            print("[INFO] Clinic with the provided phone number already exists.")
            print(
                f"[INFO] Clinic with name: {self.clinic_name} and address {self.address} and secretary: {self.secretary_phone_number} SELECTED!")
        else:
            # Insert new clinic if not already exists
            insert_query = """
                    INSERT INTO clinic_table (clinic_name, address, secretary_phone_number)
                    VALUES (%s, %s, %s)
                    """
            values = (self.clinic_name, self.address, self.secretary_phone_number)

            cursor.execute(insert_query, values)

            # Get clinic_id
            query = """
                    SELECT clinic_id FROM clinic_table
                    WHERE clinic_name = %s
                    """

            cursor.execute(query, (self.clinic_name,))
            self.clinic_id = cursor.fetchone()[0]

            connection.commit()
            print("[INFO] Clinic added successfully.")

        cursor.close()
        connection.close()

    def update_clinic_info(self, new_clinic_name: str = None, new_address: str = None,
                           new_secretary_phone_number: str = None) -> None:
        """
        Updates the clinic information in the database. You can change each parameter you like.

        Args:
            new_clinic_name (str): The new name of the clinic (default: None).
            new_address (str): The new address of the clinic (default: None).
            new_secretary_phone_number (str): The new phone number of the clinic secretary (default: None).

        Returns:
            None

        Raises:
            None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        existing_doctor_query = """
        SELECT * FROM clinic_table WHERE clinic_name = %s
        """
        cursor.execute(existing_doctor_query, (new_clinic_name,))
        existing_doctor = cursor.fetchone()

        if existing_doctor:
            print("[Wrong] A clinic with the provided name already exists.")
            return

        update_fields = []
        values = []

        if new_clinic_name:
            update_fields.append("clinic_name = %s")
            values.append(new_clinic_name)
        if new_address:
            update_fields.append("address = %s")
            values.append(new_address)
        if new_secretary_phone_number:
            update_fields.append("secretary_phone_number = %s")
            values.append(new_secretary_phone_number)

        if not update_fields:
            print("[Wrong] No fields provided for update.")
            return

        values.append(self.clinic_name)

        set_clause = ", ".join(update_fields)
        query = f"""
        UPDATE clinic_table
        SET {set_clause}
        WHERE clinic_name = %s
        """

        cursor.execute(query, values)
        rows_affected = cursor.rowcount
        connection.commit()

        cursor.close()
        connection.close()

        if rows_affected == 0:
            print("[Wrong] No clinic with the provided name exists.")
        else:
            print("[INFO] Clinic profile updated successfully.")
            if new_address:
                self.address = new_address
            if new_clinic_name:
                self.clinic_name = new_clinic_name
            if new_secretary_phone_number:
                self.secretary_phone_number = new_secretary_phone_number

    def view_appointments(self) -> list:
        """
        Retrieves the appointments for the current clinic from the database.

        :return: A list of dictionaries representing the appointments scheduled for the clinic.
                 Each dictionary contains the following information:
                 - 'date': The formatted date of the appointment (YYYY/MM/DD).
                 - 'time': The formatted time of the appointment (HH:MM).
                 - 'doctor_name': The full name of the doctor associated with the appointment.
                 - 'doctor_phone_number': The phone number of the doctor associated with the appointment.
                 - 'patient_name': The full name of the patient associated with the appointment.
                 - 'patient_phone_number': The phone number of the patient associated with the appointment.
        """
        connection = establish_connection()
        cursor = connection.cursor()

        query = """
                SELECT appointment_date, appointment_time, doctor_id, patient_id
                FROM calendar_table
                WHERE clinic_id = %s
                AND canceled = %s
                """

        cursor.execute(query, (self.clinic_id, False))
        appointments = cursor.fetchall()

        if not appointments:
            print("[INFO] No appointments scheduled for this clinic.")
            return

        clinic_schedule = []
        for appointment in appointments:
            date, time, doctor_id, patient_id = appointment
            formatted_date = date.strftime("%Y/%m/%d")
            formatted_time = datetime.datetime(1, 1, 1) + time
            formatted_time = formatted_time.strftime("%H:%M")

            query = """
                    SELECT first_name, last_name, phone_number
                    FROM doctor_table
                    WHERE doctor_id = %s
                    """
            cursor.execute(query, (doctor_id,))
            doctor_first_name, doctor_last_name, doctor_phone_number = cursor.fetchone()

            query = """
                    SELECT phone_number, first_name, last_name
                    FROM patient_table
                    WHERE patient_id = %s
                    """
            cursor.execute(query, (patient_id,))
            patient_phone_number, patient_first_name, patient_last_name = cursor.fetchone()

            clinic_schedule.append({"date": formatted_date, "time": formatted_time,
                                    "doctor_name": doctor_first_name + " " + doctor_last_name,
                                    "doctor_phone_number": doctor_phone_number,
                                    "patient_name": patient_first_name + " " + patient_last_name,
                                    "patient_phone_number": patient_phone_number})

        cursor.close()
        connection.close()

        return clinic_schedule

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        Returns:
            str: The string representation of the object.
        """
        return f"clinic_name: {self.clinic_name}, address: {self.address}, secretary_phone_number: {self.secretary_phone_number}"

from clinic import Clinic
from doctor import Doctor
from DATABASE import establish_connection
from availability import Availability
from notification import Notification


class Secretary(Notification):
    def __init__(self, clinic_name: str, address: str, phone_number: str) -> None:
        """
        Initializes a new instance of the class with the specified clinic name, address, and phone number.

        Args:
            clinic_name (str): The name of the clinic.
            address (str): The address of the clinic.
            phone_number (str): The phone number of the clinic.
        """
        super().__init__()
        self.clinic_id = None
        self.clinic_name = clinic_name
        self.address = address
        self.phone_number = phone_number
        self.doctor = None
        self.clinic = None
        self._add_clinic()

    def add_or_select_doctor(self, phone_number: str, first_name: str, last_name: str, date: str = None,
                             time: str = None) -> None:
        """
        Adds a doctor to the clinic. If the date is available it will set availability for that doctor
        in that date and time.

        Parameters:
            phone_number (str): The phone number of the doctor.
            first_name (str): The first name of the doctor.
            last_name (str): The last name of the doctor.
            date (str): Optional. The date of the appointment.
            time (str): Optional. The time of the appointment.

        Returns:
            Doctor: The newly created Doctor object.

        Raises:
            ValueError: If the clinic is not set.
        """
        doctor = Doctor(phone_number=phone_number, first_name=first_name, last_name=last_name)
        doctor.save()

        if not self.clinic_id:
            print("[ERROR] Clinic not set. Please add_clinic first.")
            return

        connection = establish_connection()
        cursor = connection.cursor()

        # Check if the row already exists
        cursor.execute("SELECT * FROM doctor_clinic WHERE doctor_id = %s AND clinic_id = %s",
                       (doctor.doctor_id, self.clinic_id))
        if cursor.fetchone():
            print("[INFO] Doctor already associated with the clinic.")
        else:
            cursor.execute("INSERT INTO doctor_clinic (doctor_id, clinic_id) VALUES (%s, %s)",
                           (doctor.doctor_id, self.clinic_id))
            connection.commit()
            print("[INFO] Doctor added to the clinic.")

        cursor.close()
        connection.close()

        if date and time:
            self._add_date(doctor.phone_number, date, time)

        self.doctor = doctor

    def _add_clinic(self) -> None:
        """
        Creates a new clinic and saves it to the database.

        Parameters:
            None

        Returns:
            None
        """
        clinic = Clinic(clinic_name=self.clinic_name, address=self.address, secretary_phone_number=self.phone_number)
        clinic.save()
        if clinic.secretary_phone_number == self.phone_number:
            self.clinic_id = clinic.clinic_id
            self.clinic = clinic
        else:
            print("[Wrong] Secretary is not valid to this clinic.")
            self.clinic_id = None
            self.clinic = None

    def _add_date(self, doctor_phone_number: str, date: str, time: str) -> None:
        """
        Add a new date and time to the availability schedule for a specific doctor.

        Parameters:
            doctor_phone_number (str): The phone number of the doctor.
            date (str): The date to add to the availability schedule.
            time (str): The time to add to the availability schedule.

        Returns:
            None
        """
        availability = Availability()
        availability.add_availability(doctor_phone_number=doctor_phone_number, clinic_name=self.clinic_name, date=date,
                                      time=time)

    def update_doctor_profile(self, new_first_name: str = None, new_last_name: str = None,
                              new_phone_number: str = None) -> None:
        """
        Update the doctor's profile with the given information.

        Args:
            new_first_name (str): The new first name of the doctor. Default is None.
            new_last_name (str): The new last name of the doctor. Default is None.
            new_phone_number (str): The new phone number of the doctor. Default is None.
        """
        self.doctor.update_doctor_profile(new_first_name=new_first_name, new_last_name=new_last_name,
                                          new_phone_number=new_phone_number)

    def view_schedule_for_doctor(self) -> None:
        """
        Retrieves the schedule for the doctor and displays it in a table format.

        Parameters:
        - None

        Returns:
        - None
        """
        schedule = self.doctor.view_doctor_schedule()
        if schedule:
            self.make_table_doctor(doctor=self.doctor, doctor_schedule=schedule)

    def edit_appointments_for_doctor(self, old_date, old_time, new_date, new_time) -> None:
        """
        Edit appointments for a doctor.

        Args:
            old_date (str): The old date of the appointment.
            old_time (str): The old time of the appointment.
            new_date (str): The new date for the appointment.
            new_time (str): The new time for the appointment.

        Returns:
            None
        """
        self.doctor.edit_appointments(old_date=old_date, old_time=old_time, new_date=new_date, new_time=new_time,
                                      clinic_name=self.clinic_name)

    def update_clinic_profile(self, new_clinic_name=None, new_address=None, new_secretary_phone_number=None) -> None:
        """
        Updates the clinic profile with new information.

        :param new_clinic_name: The new name of the clinic (default: None)
        :type new_clinic_name: str or None
        :param new_address: The new address of the clinic (default: None)
        :type new_address: str or None
        :param new_secretary_phone_number: The new phone number of the clinic's secretary (default: None)
        :type new_secretary_phone_number: str or None
        :return: None
        """
        self.clinic.update_clinic_info(new_clinic_name=new_clinic_name, new_address=new_address,
                                       new_secretary_phone_number=new_secretary_phone_number)

    def view_appointments_for_clinic(self) -> None:
        """
        Retrieve and display the appointments for the clinic.

        Returns:
            None
        """
        appointments = self.clinic.view_appointments()
        if appointments:
            self.make_table_clinic(clinic=self.clinic, clinic_appointment=appointments)

    def __str__(self) -> str:
        """
        Return a string representation of the object.

        Returns:
            str: The string representation of the object.
        """
        return f"clinic_name: {self.clinic_name}, phone_number: {self.phone_number}"

from availability import Availability
from notification import Notification
from DATABASE import establish_connection


class Appointment(Availability, Notification):
    def add_appointment(self, doctor_phone_number: str, clinic_name: str, patient_phone_number: str, date: str,
                        time: str) -> None:
        """
        Adds an appointment to the clinic's calendar.

        Parameters:
            doctor_phone_number (str): The phone number of the doctor(11 digits).
            clinic_name (str): The name of the clinic.
            patient_phone_number (str): The phone number of the patient(11 digits).
            date (str): The date of the appointment(yyyy/mm/dd).
            time (str): The time of the appointment(hh:mm).

        Returns:
            None

        Raises:
            None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Step 1: Find the patient_id based on the patient's phone number
        query = "SELECT patient_id FROM patient_table WHERE phone_number = %s"
        params = (patient_phone_number,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] Patient not found")
            cursor.close()
            connection.close()
            return
        patient_id = result[0]

        # Step 2: Find the doctor_id based on the doctor's phone number
        query = "SELECT doctor_id FROM doctor_table WHERE phone_number = %s"
        params = (doctor_phone_number,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] Doctor not found")
            cursor.close()
            connection.close()
            return
        doctor_id = result[0]

        # Step 3: Check if the doctor is available on the given date
        query = """
        SELECT availability_id
        FROM availability_table
        WHERE available_date = %s
        And available_time = %s
        AND doctor_id = %s
        AND reserved = %s
        """
        params = (date, time, doctor_id, False)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] Doctor is not available on the given date")
            cursor.close()
            connection.close()
            return

        availability_id = result

        # Step 4: Find the clinic_id based on the clinic name
        query = "SELECT clinic_id FROM clinic_table WHERE clinic_name = %s"
        params = (clinic_name,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] Clinic not found")
            cursor.close()
            connection.close()
            return
        clinic_id = result[0]

        # Step 5: Check if the clinic is available on the given date
        query = """
        SELECT availability_id
        FROM availability_table
        WHERE available_date = %s
        AND available_time = %s
        AND clinic_id = %s
        """
        params = (date, time, clinic_id)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] Clinic is not available on the given date")
            cursor.close()
            connection.close()
            return

        # Step 6: Insert a new row into the appointment_table
        query = "INSERT INTO calendar_table (doctor_id, clinic_id, patient_id, appointment_date, appointment_time, canceled) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (doctor_id, clinic_id, patient_id, date, time, False)
        cursor.execute(query, params)

        # Step 7: Update the history column in the availability_table
        query = "UPDATE availability_table SET reserved = True WHERE availability_id = %s"
        params = (availability_id)
        cursor.execute(query, params)

        connection.commit()

        print("[INFO] Appointment added successfully!")

        cursor.close()
        connection.close()

    def cancel_appointment(self, patient_phone_number: str, date: str, time: str) -> None:
        """
        Cancels an appointment based on the patient's phone number, date, and time.

        Args:
            patient_phone_number (str): The phone number of the patient(11 digits).
            date (str): The date of the appointment(yyyy/mm/dd).
            time (str): The time of the appointment(hh:mm).

        Returns:
            None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Step 1: Find the patient_id based on the phone number
        query = "SELECT patient_id FROM patient_table WHERE phone_number = %s"
        params = (patient_phone_number,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] Patient not found")
            cursor.close()
            connection.close()
            return
        patient_id = result[0]

        # Step 2: Find the appointment_id based on the patient_id and date and time
        query = """
        SELECT calendar_id, doctor_id, clinic_id
        FROM calendar_table
        WHERE patient_id = %s
        AND appointment_date = %s
        AND appointment_time = %s
        AND canceled = %s
        """
        params = (patient_id, date, time, False)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] Appointment not found")
            cursor.close()
            connection.close()
            return

        calendar_id, doctor_id, clinic_id = result

        # Step 3: Update the cancel column in the appointment_table
        query = "UPDATE calendar_table SET canceled = TRUE WHERE calendar_id = %s"
        params = (calendar_id,)
        cursor.execute(query, params)
        connection.commit()

        # step 5: find the availability_id
        query = """
        SELECT availability_id
        FROM availability_table
        WHERE doctor_id = %s
        AND clinic_id = %s
        AND available_date = %s
        AND available_time = %s
        AND reserved = %s
        """
        params = (doctor_id, clinic_id, date, time, True)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] something unusual happened")
            cursor.close()
            connection.close()
            return
        availability_id = result

        # Step 4: Update the availability_table for the cancellation date
        query = "UPDATE availability_table SET reserved = FALSE WHERE availability_id = %s"
        params = (availability_id)
        cursor.execute(query, params)
        connection.commit()
        print("[INFO] Appointment canceled successfully!")

        cursor.close()
        connection.close()

    def reschedule_appointment(self, patient_phone_number: str, old_date: str, old_time: str, new_date: str,
                               new_time: str) -> None:
        """
        Reschedules an appointment for a patient.

        Args:
            patient_phone_number (str): The phone number of the patient(11 digits).
            old_date (str): The old date of the appointment(yyyy/mm/dd).
            old_time (str): The old time of the appointment(hh:mm).
            new_date (str): The new date of the appointment(yyyy/mm/dd).
            new_time (str): The new time of the appointment(hh:mm).

        Returns:
            None
        Raises:
            None.
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Step 1: Find the patient_id based on the phone number
        query = "SELECT patient_id FROM patient_table WHERE phone_number = %s"
        params = (patient_phone_number,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] Patient not found")
            cursor.close()
            connection.close()
            return
        patient_id = result[0]

        # Step 2: Find the appointment_id based on the patient_id and old date and time
        query = """
        SELECT calendar_id, doctor_id, clinic_id
        FROM calendar_table
        WHERE patient_id = %s
        AND appointment_date = %s
        AND appointment_time = %s
        AND canceled = %s
        """
        params = (patient_id, old_date, old_time, False)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] Appointment not found")
            cursor.close()
            connection.close()
            return

        calendar_id, doctor_id, clinic_id = result

        # Step 3: Check the availability of the new date in the availability_table
        query = """
        SELECT availability_id
        FROM availability_table 
        WHERE available_date = %s 
        AND available_time = %s
        AND doctor_id = %s
        AND clinic_id = %s 
        AND reserved = %s 
        """
        params = (new_date, new_time, doctor_id, clinic_id, False)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[INFO] New date not available with the same doctor and clinic")
            cursor.close()
            connection.close()
            return

        availability_id_new = result

        # Step 4: Check the availability of the old date in the availability_table
        query = """
        SELECT availability_id
        FROM availability_table 
        WHERE available_date = %s 
        AND available_time = %s
        AND doctor_id = %s
        AND clinic_id = %s 
        AND reserved = %s 
        """
        params = (old_date, old_time, doctor_id, clinic_id, True)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] Old date not available")
            cursor.close()
            connection.close()
            return

        availability_id_old = result

        # Step 4: Update the availability_table for the old appointment date
        query = "UPDATE availability_table SET reserved = False WHERE availability_id = %s"
        params = (availability_id_old)
        cursor.execute(query, params)

        # Step 5: Update the availability_table for the new appointment date
        query = "UPDATE availability_table SET reserved = True WHERE availability_id = %s"
        params = (availability_id_new)
        cursor.execute(query, params)

        # Step 6: Update the appointment_table with the new date
        query = "UPDATE calendar_table SET appointment_date = %s WHERE calendar_id = %s"
        params = (new_date, calendar_id)
        cursor.execute(query, params)

        query = "UPDATE calendar_table SET appointment_time = %s WHERE calendar_id = %s"
        params = (new_time, calendar_id)
        cursor.execute(query, params)
        connection.commit()

        print("[INFO] Appointment rescheduled successfully!")

        cursor.close()
        connection.close()

from DATABASE import establish_connection
import datetime


class Availability:
    def add_availability(self, doctor_phone_number: str, clinic_name: str, date: str, time: str) -> None:
        """
        Adds availability for a doctor at a specific clinic on a given date and time.

        Args:
            doctor_phone_number (str): The phone number of the doctor(11 digits).
            clinic_name (str): The name of the clinic.
            date (str): The date of availability(yyyy/mm/dd).
            time (str): The time of availability(hh:mm).

        Returns:
            None

        Raises:
            None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Step 1: Get the doctor_id using the doctor's phone_number
        query = "SELECT doctor_id FROM clinic_data.doctor_table WHERE phone_number = %s"
        params = (doctor_phone_number,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] Doctor not found")
            return
        doctor_id = result[0]

        # Step 2: Get the clinic_id using the clinic_name
        query = "SELECT clinic_id FROM clinic_data.clinic_table WHERE clinic_name = %s"
        params = (clinic_name,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[Wrong] Clinic not found")
            return
        clinic_id = result[0]

        # Step 3: Check if the availability already exists for the doctor and date
        query = """
        SELECT availability_id
        FROM availability_table
        WHERE doctor_id = %s
        AND clinic_id = %s
        AND available_date = %s
        AND available_time = %s
        """
        params = (doctor_id, clinic_id, date, time)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is not None:
            print("[Wrong] Already exists for the input data")
            cursor.close()
            connection.close()
            return

        # Step 4: Insert a new row into the availability_table
        cursor.fetchall()
        query = "INSERT INTO availability_table (doctor_id, clinic_id, available_date,available_time, reserved) VALUES (%s, %s, %s, %s, %s)"
        params = (doctor_id, clinic_id, date, time, False)
        cursor.execute(query, params)
        connection.commit()

        print(f"[INFO] {date} {time} added to the list")

        cursor.close()
        connection.close()

    def get_available_times(self) -> list:
        """
        Retrieves the available times for appointments from the database.

        :return: A list of dictionaries containing the available dates, times, doctor names, clinic names, clinic addresses, and secretary phone numbers.
        :rtype: list[dict]
        """
        connection = establish_connection()

        cursor = connection.cursor()

        query = """
        SELECT a.available_date, a.available_time, d.first_name, d.last_name, c.clinic_name, c.address, c.secretary_phone_number
        FROM availability_table a
        JOIN doctor_table d ON a.doctor_id = d.doctor_id
        JOIN clinic_table c ON a.clinic_id = c.clinic_id
        WHERE a.reserved = FALSE
        """

        cursor.execute(query)
        results = cursor.fetchall()

        available_times = []
        for result in results:
            available_date, available_time, first_name, last_name, clinic_name, address, secretary_phone_number = result
            formatted_date = available_date.strftime("%Y/%m/%d")
            formatted_time = datetime.datetime(1, 1, 1) + available_time
            formatted_time = formatted_time.strftime("%H:%M")
            available_times.append({
                "Available Date": formatted_date,
                "Available Time": formatted_time,
                "Doctor Name": first_name + " " + last_name,
                "Clinic Name": clinic_name,
                "Clinic Address": address,
                "Secretary Phone Number": secretary_phone_number
            })

        cursor.close()
        connection.close()

        return available_times

from tabulate import tabulate


class Notification:
    def send_notification_successful(self):
        """Send successful notification"""
        pass

    def send_notification_unsuccessful(self):
        """Send unsuccessful notification"""
        pass

    def make_table_doctor(self, doctor, doctor_schedule: list) -> None:
        """
        Generate a table for a given doctor and their schedule.

        Parameters:
            doctor (Doctor): The doctor object containing the doctor's information.
            doctor_schedule (list): A list of dictionaries representing the doctor's schedule. Each dictionary contains
            the date, time, clinic, patient name, and patient phone number.

        Returns:
            None

        This function takes a doctor object and their schedule, and generates a table to display the schedule.
        The schedule is converted to a 2D list, with each row representing a schedule entry. The table is then displayed
        using the tabulate function from the tabulate library, with the specified headers and formatting options.
        """
        data = []
        for row in doctor_schedule:
            sub = [row["date"], row["time"], row["clinic"], row["patient_name"], row["patient_phone_number"]]
            data.append(sub)

        headers = ["Date", "Time", "Clinic", "Patient Name", "Patient Phone Number"]

        print(f"### Doctor {doctor.first_name} {doctor.last_name}" + f" Phone number: {doctor.phone_number} ###")
        print(tabulate(data, headers=headers, tablefmt="fancy_grid", showindex="always", numalign="center"))

    def make_table_clinic(self, clinic, clinic_appointment: list) -> None:
        """
        Generates a table for a given clinic and clinic appointment data.

        Parameters:
            clinic (Clinic): The clinic object containing information about the clinic.
            clinic_appointment (list): A list of appointment data for the clinic.

        Returns:
            None

        This function takes a clinic object and a list of clinic appointment data and generates a table. The table is
        printed to the console using the tabulate library. Each row of the table represents an appointment and contains
        the following columns:
        - Date: The date of the appointment
        - Time: The time of the appointment
        - Doctor Name: The name of the doctor for the appointment
        - Doctor Phone Number: The phone number of the doctor for the appointment
        - Patient Name: The name of the patient for the appointment
        - Patient Phone Number: The phone number of the patient for the appointment

        The table is generated by iterating over the clinic appointment data and constructing a list of sublists, where
        each sublist represents a row in the table. The sublists are then added to the 'data' list. The headers for
        the table are defined in the 'headers' list.

        After the table is generated, additional information about the clinic is printed to the console, including
        the clinic name, address, and secretary phone number.
        """
        data = []
        for row in clinic_appointment:
            sub = [row["date"], row["time"], row["doctor_name"], row["doctor_phone_number"], row["patient_name"],
                   row["patient_phone_number"]]
            data.append(sub)
        headers = ["Date", "Time", "Doctor Name", "Doctor Phone Number", "Patient Name", "Patient Phone Number"]
        print(
            f"Clinic {clinic.clinic_name}" + f"Address: {clinic.address}" + f"Secretary Phone Number: {clinic.secretary_phone_number}")
        print(tabulate(data, headers=headers, tablefmt="fancy_grid", showindex="always", numalign="center"))

    def make_table_current_appointment(self,patient ,current_appointments):
        data = []
        for row in current_appointments:
            sub = [row["Date"], row["Time"], row["Doctor Name"], row["Clinic Name"]]
            data.append(sub)

        headers = ["Date", "Time", "Doctor Name", "Clinic Name"]
        print(f"Patient: {patient.first_name} {patient.last_name} | phone number: {patient.phone_number}")
        print(tabulate(data, headers=headers, tablefmt="fancy_grid", numalign="center"))

    def make_table_appointment(self,patient ,appointments_history):
        headers = ["Date", "Time", "Doctor Name", "Clinic Name"]
        print(f"Patient: {patient.first_name} {patient.last_name} | phone number: {patient.phone_number}")
        print(tabulate(appointments_history, headers=headers, tablefmt="fancy_grid", numalign="center"))


import mysql.connector

database = ["localhost", "3306", "root", "1234", "clinic_data"]


def establish_connection():
    """
    Establishes a connection to the MySQL database.

    :return: The established database connection.
    :rtype: mysql.connector.connection.MySQLConnection
    """
    connection = mysql.connector.connect(
        host=f"{database[0]}",
        port=f"{database[1]}",
        user=f"{database[2]}",
        password=f"{database[3]}",
        database=f"{database[4]}",
        buffered=True
    )
    return connection
