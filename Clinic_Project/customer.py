from patient import Patient
from secretary import Secretary


class Customer(Patient, Secretary):
    def edit_appointments(self):
        """Add, remove, or edit appointments"""
        pass
