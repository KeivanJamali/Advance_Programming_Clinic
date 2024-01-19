from DATABASE import establish_connection
import datetime


class Patient:
    def __init__(self, phone_number):
        # Initialize patient attributes
        self.patient_id = None
        self.first_name = None
        self.last_name = None
        self.phone_number = phone_number
        self.appointments = []

        connection = establish_connection()
        cursor = connection.cursor()

        # Check if the patient with the provided phone number already exists
        query = "SELECT * FROM patient_table WHERE phone_number = %s"
        cursor.execute(query, (self.phone_number,))
        existing_patient = cursor.fetchone()

        if existing_patient:
            # If patient exists, set attributes based on existing data
            self.patient_id, self.first_name, self.last_name, self.phone_number = existing_patient

    def add_patient(self, first_name, last_name, phone_number):
        """
        Add a new patient to the database.

        Parameters:
            first_name (str): The first name of the patient.
            last_name (str): The last name of the patient.
            phone_number (str): The phone number of the patient.

        Returns:
            None
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Check if the patient with the provided phone number already exists
        query = "SELECT * FROM patient_table WHERE phone_number = %s"
        cursor.execute(query, (phone_number,))
        existing_patient = cursor.fetchone()

        if existing_patient:
            # If patient exists, set attributes based on existing data
            print("[INFO] Patient with the provided phone number already exists.")
        else:
            # Insert new patient if not already exists
            insert_query = "INSERT INTO patient_table (first_name, last_name, phone_number) VALUES (%s, %s, %s)"
            values = (first_name, last_name, phone_number)
            cursor.execute(insert_query, values)

            # Get patient_id
            query = "SELECT patient_id FROM patient_table WHERE phone_number = %s"
            cursor.execute(query, (phone_number,))
            self.patient_id = cursor.fetchone()[0]

            connection.commit()
            print("[INFO] Patient added successfully.")

        cursor.close()
        connection.close()

    def update_patient_info(self, new_first_name=None, new_last_name=None, new_phone_number=None):
        """
        Update the patient's information in the database.

        Parameters:
            new_first_name (str): The new first name of the patient. Default is None.
            new_last_name (str): The new last name of the patient. Default is None.
            new_phone_number (str): The new phone number of the patient. Default is None.

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

        # headers = ["Date", "Time", "Doctor Name", "Clinic Name"]
        # print(tabulate(current_appointments, headers=headers, tablefmt="fancy_grid", numalign="center"))
        return current_appointments

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

            appointments_history.append({
                "Date": formatted_date,
                "Time": formatted_time,
                "Doctor Name": f"{doctor_first_name} {doctor_last_name}",
                "Clinic Name": clinic_name
            })

        cursor.close()
        connection.close()

        # headers = ["Date", "Time", "Doctor Name", "Clinic Name"]
        # print(tabulate(appointments_history, headers=headers, tablefmt="fancy_grid", numalign="center"))
        return appointments_history
