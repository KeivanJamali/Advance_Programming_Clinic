import mysql.connector
import datetime


class Availability:
    def add_availability(self, doctor_phone_number, clinic, date, time):
        """
        Adds availability for a doctor at a specific clinic on a given date and time.

        Args:
            doctor_phone_number (str): The phone number of the doctor(11 digits).
            clinic (str): The name of the clinic.
            date (str): The date of availability(yyyy/mm/dd).
            time (str): The time of availability(hh:mm).

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

        # Step 1: Get the doctor_id using the doctor's phone_number
        query = "SELECT doctor_id FROM clinic_data.doctor_table WHERE phone_number = %s"
        params = (doctor_phone_number,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("Doctor not found")
            return
        doctor_id = result[0]

        # Step 2: Get the clinic_id using the clinic_name
        query = "SELECT clinic_id FROM clinic_data.clinic_table WHERE clinic_name = %s"
        params = (clinic,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("Clinic not found")
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
            print("[ERROR] Already exists for the input data")
            cursor.close()
            connection.close()
            return

        # Step 4: Insert a new row into the availability_table
        cursor.fetchall()
        query = "INSERT INTO availability_table (doctor_id, clinic_id, available_date,available_time, reserved) VALUES (%s, %s, %s, %s, %s)"
        params = (doctor_id, clinic_id, date, time, False)
        cursor.execute(query, params)
        connection.commit()

        cursor.close()
        connection.close()

    def get_available_times(self):
        """
        Retrieves the available times for appointments from the database.

        :return: A list of dictionaries containing the available dates, times, doctor names, clinic names, clinic addresses, and secretary phone numbers.
        :rtype: list[dict]
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
