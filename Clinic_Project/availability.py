import mysql.connector

class Availability:
    def add_availability(self, doctor_phone_number, clinic, date):
        """Add availability"""
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
        """
        params = (doctor_id, clinic_id, date)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is not None:
            print("[ERROR] Already exists for the input data")
            cursor.close()
            connection.close()
            return

        # Step 4: Insert a new row into the availability_table
        cursor.fetchall()
        query = "INSERT INTO availability_table (doctor_id, clinic_id, available_date, reserved) VALUES (%s, %s, %s, %s)"
        params = (doctor_id, clinic_id, date, False)
        cursor.execute(query, params)
        connection.commit()

        cursor.close()
        connection.close()

    def get_available_times(self):
        """Search for available times"""
        pass

    def check_date_availability(self):
        """Check if the date is available"""
        pass
