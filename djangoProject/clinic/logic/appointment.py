from .availability import Availability
from .notification import Notification
from .DATABASE import establish_connection


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
