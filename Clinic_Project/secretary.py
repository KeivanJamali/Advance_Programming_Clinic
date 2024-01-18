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

    def add_doctor(self, phone_number: str, first_name: str, last_name: str, date: str = None,
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
