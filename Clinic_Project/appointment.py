from availability import Availability
from notification import Notification


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
