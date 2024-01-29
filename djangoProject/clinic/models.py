from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=50)

    class Meta:
        db_table = "user_table"


class Clinic(models.Model):
    clinic_id = models.AutoField(primary_key=True)
    clinic_name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    secretary_phone_number = models.CharField(max_length=11)

    class Meta:
        db_table = "clinic_table"


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        db_table = "doctor_table"


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.DateField()
    national_code = models.CharField(max_length=10)
    email = models.EmailField(blank=True)

    class Meta:
        db_table = "patient_table"


class Calendar(models.Model):
    calendar_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    canceled = models.BooleanField(default=False)

    class Meta:
        db_table = "calendar_table"


class Availability(models.Model):
    availability_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    available_date = models.DateField()
    available_time = models.TimeField()
    reserved = models.BooleanField(default=False)

    class Meta:
        db_table = "availability_table"


class DoctorClinic(models.Model):
    doctor = models.OneToOneField('Doctor', on_delete=models.CASCADE, primary_key=True)
    clinic = models.OneToOneField('Clinic', on_delete=models.CASCADE)

    class Meta:
        db_table = "doctor_clinic"


class CustomerPatient(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    patient = models.OneToOneField('Patient', on_delete=models.CASCADE)

    class Meta:
        db_table = "customer_patient"
