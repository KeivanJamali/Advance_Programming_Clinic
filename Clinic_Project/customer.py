from patient import Patient
from secretary import Secretary
from appointment import Appointment

class Customer:
    def __init__(self, phone_number: str):
        # Initialize instances of Patient, Secretary, and Appointment classes
        self.patient = Patient(phone_number)
        # self.secretary = Secretary()
        self.appointment = Appointment()

    def add_patient(self, first_name, last_name, phone_number, birthdate, international_code, email):
        # Delegate the add_patient functionality to the Patient class
        self.patient.add_patient(first_name, last_name, phone_number, birthdate, international_code, email)

    def update_patient_info(self, new_phone_number=None, new_first_name=None, new_last_name=None,
                            new_email=None, new_birthday=None, new_international_code=None):
        # Delegate the update_patient_info functionality to the Patient class
        self.patient.update_patient_info(new_phone_number, new_first_name, new_last_name, new_email, new_birthday, new_international_code)

    def remove_patient(self, user_phone):
        # Check if the user_phone and phone_number exist in the user_patient table
        connection = establish_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM user_patient WHERE user_phone = %s AND phone_number = %s"
        cursor.execute(query, (user_phone, self.patient.phone_number))
        user_patient_entry = cursor.fetchone()

        if user_patient_entry:
            # If entry exists, delegate the remove_patient functionality to the Patient class
            self.patient.remove_patient()
        else:
            # If entry doesn't exist, print an error message
            print("[ERROR] User not authorized to remove the patient.")

        cursor.close()
        connection.close()
    def view_current_appointments(self):
        # Delegate the view_current_appointments functionality to the Patient class
        return self.patient.view_current_appointments()

    def view_appointments_history(self):
        # Delegate the view_appointments_history functionality to the Patient class
        return self.patient.view_appointments_history()

    def add_appointment(self, doctor_phone_number, clinic_name, patient_phone_number, date, time):
        # Delegate the add_appointment functionality to the Appointment class
        self.appointment.add_appointment(doctor_phone_number, clinic_name, patient_phone_number, date, time)

    def cancel_appointment(self, patient_phone_number, date, time):
        # Delegate the cancel_appointment functionality to the Appointment class
        self.appointment.cancel_appointment(patient_phone_number, date, time)

    def reschedule_appointment(self, patient_phone_number, old_date, old_time, new_date, new_time):
        # Delegate the reschedule_appointment functionality to the Appointment class
        self.appointment.reschedule_appointment(patient_phone_number, old_date, old_time, new_date, new_time)
