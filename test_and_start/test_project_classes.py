class Availability:
    def get_available_times(self):
        """Search for available times"""
        pass

    def check_date_availability(self):
        """Check if the date is available"""
        pass


class Notification:
    def send_notification_successful(self):
        """Send successful notification"""
        pass

    def send_notification_unsuccessful(self):
        """Send unsuccessful notification"""
        pass


class Appointment(Availability, Notification):
    def add_appointment(self):
        """Get the proper date and schedule an appointment"""
        pass

    def cancel_appointment(self):
        """Cancel the appointment"""
        pass

    def reschedule_appointment(self):
        """Reschedule the appointment for another appropriate date"""
        pass


class User:
    def register(self):
        pass

    def login(self):
        pass


class Clinic:
    def __init__(self):
        self.doctors = []

    def update_clinic_info(self):
        """Admin can update the clinic info"""
        pass

    def set_availability(self):
        """Admin can set the availability"""
        pass

    def view_appointments(self):
        """Can see appointments"""
        pass

    def add_doctor(self):
        pass

    def remove_doctor(self):
        pass


class Doctor:
    def __init__(self):
        self.shifts = []

    def update_doctor_info(self):
        pass

    def view_doctor_schedule(self):
        pass

    def edit_appointments(self):
        """Can add, remove, or edit appointments"""
        pass


class Patient:
    def __init__(self):
        self.appointments = []

    def add_patient(self):
        """Get the name of the patient and required fields to add the patient to the database"""
        pass

    def update_patient_info(self):
        """Update patient info"""
        pass

    def remove_patient(self):
        """Remove the patient from the database"""
        pass

    def view_current_appointments(self):
        """Show current appointments"""
        pass

    def view_appointments_history(self):
        """Show appointment history"""
        pass


class Secretary:
    def __init__(self):
        self.clinics = []

    def update_profile(self):
        """Update customer profile"""
        pass

    def add_clinic(self):
        """Add a new clinic (admin-only)"""
        pass

    def update_clinic(self):
        """Connect to a specific clinic and change its details (admin-only)"""
        pass


class Customer(Patient, Secretary):
    def edit_appointments(self):
        """Add, remove, or edit appointments"""
        pass


# Example usage
user = User()
user.register()

clinic = Clinic()
clinic.add_doctor()

patient = Patient()
patient.add_patient()
patient.add_appointment()

doctor = Doctor()
doctor.view_doctor_schedule()