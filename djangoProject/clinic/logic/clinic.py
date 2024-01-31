from .DATABASE import establish_connection
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

    def save(self):
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
        return self

    def update_clinic_info(self, new_clinic_name: str = None, new_address: str = None) -> None:
        """
        Updates the clinic information in the database. You can change each parameter you like.

        Args:
            new_clinic_name (str): The new name of the clinic (default: None).
            new_address (str): The new address of the clinic (default: None).

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
