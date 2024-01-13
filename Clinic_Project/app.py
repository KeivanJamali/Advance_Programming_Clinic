from appointment import Appointment
from availability import Availability
from clinic import Clinic
from customer import Customer
from doctor import Doctor
from notification import Notification
from patient import Patient
from secretary import Secretary
from user import User

# just and simple example... has many problems.

user = User()
user.register()

clinic = Clinic()
clinic.add_doctor()

patient = Patient()
patient.add_patient()
patient.add_appointment()

doctor = Doctor()
doctor.view_doctor_schedule()
