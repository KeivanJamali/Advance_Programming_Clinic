from .DATABASE import establish_connection
import datetime
from .appointment import Appointment


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
                              new_phone_number: str = None):
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
            return False

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
            return False

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
        return True

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
