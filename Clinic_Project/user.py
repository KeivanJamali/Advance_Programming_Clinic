from customer import Customer
from secretary import Secretary


class User(Customer, Secretary):
    def register(self):
        pass

    def login(self):
        pass


class Availability:
    def get_available_times(self):
        """search for available times"""
        pass

    def check_date_availability(self):
        """check if the date is available"""
        pass


class Notification:
    def send_notification_successful(self):
        """send notification"""
        pass

    def send_notification_unsuccessful(self):
        """send notification"""
        pass


class Appointment(Availability, Notification):
    def add_appointment(self):
        """get the proper date and schedule an appointment"""
        pass

    def cancel_appointment(self):
        """cancel the appointment"""
        pass

    def reschedule_appointment(self):
        """reschedule the appointment in another appropriate date"""
        pass


class Patient(Appointment):
    def add_patient(self):
        """get the name of the patient and required field to add the patient to database"""
        pass

    def update_patient_info(self):
        """update patient info"""
        pass

    def remove_patient(self):
        """remove the patient from database"""
        pass


class Doctor(Appointment):
    def add_doctor(self):
        pass

    def update_doctor_info(self):
        pass

    def view_doctor_schedule(self):
        pass

    def remove_doctor(self):
        pass

    def edit_appointments(self):
        """can add, remove or edit appointments"""
        pass


class Clinic(Doctor):

    def update_clinic_info(self):
        """admin can update the clinic info"""
        pass

    def set_availability(self):
        """admin can set the availability"""
        pass

    def view_appointment(self):
        """can see appointments"""
        pass

    def edit_doctors(self):
        """can add, remove, edit doctors"""
        pass
