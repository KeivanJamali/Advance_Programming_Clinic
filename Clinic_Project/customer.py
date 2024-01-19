from patient import Patient
from secretary import Secretary
from appointment import Appointment

class Customer:
    def __init__(self):
        # Initialize instances of Patient, Secretary, and Appointment classes
        self.patient = Patient()
        self.secretary = Secretary()
        self.appointment = Appointment()

    def add_patient(self, first_name, last_name, phone_number):
        # Delegate the add_patient functionality to the Patient class
        self.patient.add_patient(first_name, last_name, phone_number)

    def update_patient_info(self, patient_id, new_first_name=None, new_last_name=None, new_phone_number=None):
        # Delegate the update_patient_info functionality to the Patient class
        self.patient.update_patient_info(patient_id, new_first_name, new_last_name, new_phone_number)

    def remove_patient(self, patient_id):
        # Delegate the remove_patient functionality to the Patient class
        self.patient.remove_patient(patient_id)

    def view_current_appointments(self, patient_id):
        # Delegate the view_current_appointments functionality to the Patient class
        return self.patient.view_current_appointments(patient_id)

    def view_appointments_history(self, patient_id):
        # Delegate the view_appointments_history functionality to the Patient class
        return self.patient.view_appointments_history(patient_id)

    def add_appointment(self, doctor_phone_number, clinic_name, patient_phone_number, date, time):
        # Delegate the add_appointment functionality to the Appointment class
        self.appointment.add_appointment(doctor_phone_number, clinic_name, patient_phone_number, date, time)

    def cancel_appointment(self, patient_phone_number, date, time):
        # Delegate the cancel_appointment functionality to the Appointment class
        self.appointment.cancel_appointment(patient_phone_number, date, time)

    def reschedule_appointment(self, patient_phone_number, old_date, old_time, new_date, new_time):
        # Delegate the reschedule_appointment functionality to the Appointment class
        self.appointment.reschedule_appointment(patient_phone_number, old_date, old_time, new_date, new_time)

    # def edit_appointments(self, action, appointment_details):
    #     """
    #     Add, remove, or edit appointments.
    #
    #     Parameters:
    #         action (str): Action to perform ('add', 'remove', 'edit').
    #         appointment_details (dict): Details of the appointment.
    #
    #     Returns:
    #         None
    #     """
    #     if action == 'add':
    #         # Delegate the add_appointment functionality to the Appointment class
    #         self.appointment.add_appointment(**appointment_details)
    #
    #     elif action == 'remove':
    #         # Delegate the remove_appointment functionality to the Appointment class
    #         self.appointment.cancel_appointment(**appointment_details)
    #
    #     elif action == 'edit':
    #         # Delegate the edit_appointment functionality to the Appointment class
    #         self.appointment.reschedule_appointment(**appointment_details)
    #
    #     else:
    #         print("[Wrong] Invalid action. Please choose 'add', 'remove', or 'edit'.")
