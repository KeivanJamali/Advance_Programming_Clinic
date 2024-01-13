from availability import Availability
from notification import Notification


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
