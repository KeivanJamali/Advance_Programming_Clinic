from availability import Availability
from notification import Notification
import mysql.connector


class Appointment(Availability, Notification):
    def add_appointment(self, doctor_phone_number, clinic_name, patient_phone_number, date):
        """
        Adds an appointment to the calendar_table.

        Args:
            doctor_phone_number (str): The phone number of the doctor(11 digits).
            clinic_name (str): The name of the clinic.
            patient_phone_number (str): The phone number of the patient(11 digits).
            date (str): The date of the appointment(yyyy/mm/dd).

        Returns:
            None

        Raises:
            None
        """
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="1234",
            database="clinic_data",
            buffered=True
        )

        cursor = connection.cursor()

        # Step 1: Find the patient_id based on the patient's phone number
        query = "SELECT patient_id FROM patient_table WHERE phone_number = %s"
        params = (patient_phone_number,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[ERROR] Patient not found")
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
            print("[ERROR] Doctor not found")
            cursor.close()
            connection.close()
            return
        doctor_id = result[0]

        # Step 3: Check if the doctor is available on the given date
        query = """
        SELECT availability_id, reserved
        FROM availability_table
        WHERE available_date = %s
        AND doctor_id = %s
        """
        params = (date, doctor_id)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[ERROR] Doctor is not available on the given date")
            cursor.close()
            connection.close()
            return

        availability_id, reserved = result

        if reserved:
            print("[ERROR] This date is already reserved")
            cursor.close()
            connection.close()
            return

        # Step 4: Find the clinic_id based on the clinic name
        query = "SELECT clinic_id FROM clinic_table WHERE clinic_name = %s"
        params = (clinic_name,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[ERROR] Clinic not found")
            cursor.close()
            connection.close()
            return
        clinic_id = result[0]

        # Step 5: Check if the clinic is available on the given date
        query = """
        SELECT availability_id
        FROM availability_table
        WHERE available_date = %s
        AND clinic_id = %s
        """
        params = (date, clinic_id)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[ERROR] Clinic is not available on the given date")
            cursor.close()
            connection.close()
            return

        # Step 6: Check if the date is in the availability_table
        query = "SELECT availability_id FROM availability_table WHERE available_date = %s"
        params = (date,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[ERROR] Invalid date")
            cursor.close()
            connection.close()
            return
        availability_id = result[0]

        # Step 7: Insert a new row into the appointment_table
        query = "INSERT INTO calendar_table (doctor_id, clinic_id, patient_id, appointment_date) VALUES (%s, %s, %s, %s)"
        params = (doctor_id, clinic_id, patient_id, date)
        cursor.execute(query, params)

        # Step 8: Update the history column in the availability_table
        query = "UPDATE availability_table SET reserved = True WHERE availability_id = %s"
        params = (availability_id,)
        cursor.execute(query, params)

        connection.commit()

        print("[INFO] Appointment added successfully!")

        cursor.close()
        connection.close()

    def cancel_appointment(self, patient_phone_number, date):
        """Cancel the appointment"""
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="1234",
            database="clinic_data",
            buffered=True
        )

        cursor = connection.cursor()

        # Step 1: Find the patient_id based on the phone number
        query = "SELECT patient_id FROM patient_table WHERE phone_number = %s"
        params = (patient_phone_number,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[ERROR] Patient not found")
            cursor.close()
            connection.close()
            return
        patient_id = result[0]

        # Step 2: Find the appointment_id based on the patient_id and date
        query = """
        SELECT calendar_id, canceled, doctor_id
        FROM calendar_table
        WHERE patient_id = %s
        AND appointment_date = %s
        """
        params = (patient_id, date)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[ERROR] Appointment not found")
            cursor.close()
            connection.close()
            return

        calendar_id, canceled, doctor_id = result

        if canceled:
            print("[ERROR] Appointment already canceled")
            cursor.close()
            connection.close()
            return

        # Step 3: Update the cancel column in the appointment_table
        query = "UPDATE calendar_table SET canceled = TRUE WHERE calendar_id = %s"
        params = (calendar_id,)
        cursor.execute(query, params)
        connection.commit()

        # Step 4: Update the availability_table for the cancellation date
        query = "UPDATE availability_table SET reserved = FALSE WHERE available_date = %s and doctor_id = %s"
        params = (date, doctor_id)
        try:
            cursor.execute(query, params)
            connection.commit()
            print("[INFO] Appointment canceled successfully!")
        except Exception as e:
            print("[ERROR] Failed to update availability_table:", str(e))

        cursor.close()
        connection.close()

    def reschedule_appointment(self, patient_phone_number, old_date, new_date):
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="1234",
            database="clinic_data",
            buffered=True
        )

        cursor = connection.cursor()

        # Step 1: Find the patient_id based on the phone number
        query = "SELECT patient_id FROM patient_table WHERE phone_number = %s"
        params = (patient_phone_number,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[ERROR] Patient not found")
            cursor.close()
            connection.close()
            return
        patient_id = result[0]

        # Step 2: Find the appointment_id based on the patient_id and current date
        query = """
        SELECT calendar_id, appointment_date, doctor_id
        FROM calendar_table
        WHERE patient_id = %s
        AND appointment_date = %s
        """
        params = (patient_id, old_date)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("Appointment not found")
            cursor.close()
            connection.close()
            return

        calendar_id, appointment_date, doctor_id = result

        # Step 3: Check the availability of the new date in the availability_table
        query = "SELECT availability_id, reserved FROM availability_table WHERE available_date = %s and doctor_id = %s"
        params = (new_date, doctor_id)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("[ERROR] Date not available")
            cursor.close()
            connection.close()
            return

        availability_id, reserved = result

        if reserved:
            print("[ERROR] The new date is already reserved")
            cursor.close()
            connection.close()
            return

        # Step 4: Update the availability_table for the current appointment date
        query = "UPDATE availability_table SET reserved = False WHERE available_date = %s"
        params = (old_date,)
        cursor.execute(query, params)

        # Step 5: Update the availability_table for the new appointment date
        query = "UPDATE availability_table SET reserved = True WHERE available_date = %s and doctor_id = %s"
        params = (new_date, doctor_id)
        cursor.execute(query, params)

        # Step 6: Update the appointment_table with the new date
        query = "UPDATE appointment_table SET appointment_date = %s WHERE calendar_id = %s"
        params = (new_date, calendar_id)
        cursor.execute(query, params)
        connection.commit()

        print("Appointment rescheduled successfully!")

        cursor.close()
        connection.close()
