from .patient import Patient
from .appointment import Appointment
from .DATABASE import establish_connection


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
