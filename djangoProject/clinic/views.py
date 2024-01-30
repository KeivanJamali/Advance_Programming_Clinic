import json

from django.shortcuts import render, redirect
from .logic.user import User
from .logic.secretary import Secretary
from .logic.customer import Customer


def register_or_login(request):
    if request.method == "POST":
        act = request.POST.get("action")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")

        user = User()

        if act == "register":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            user_type = request.POST.get('user_type')
            email_check = email if email else None

            user = user.register_user(first_name, last_name, password, phone_number, user_type, email_check)

            if user:
                if user.user_type == "1":
                    return render(request, 'secretary_register.html', {'phone_number': user.phone_number})
                elif user.user_type == "2":
                    try:
                        return render(request, 'customer_page.html', {'phone_number': user.phone_number})
                    except Exception as e:
                        error_message = f"Login failed: {str(e)}"
                        return render(request, 'register_or_login.html', {'error_message': error_message})

            error_message = "Registration failed. Please check your inputs and try again."
            return render(request, 'register_or_login.html', {'error_message': error_message})

        elif act == "login":
            user = user.login_user(password, phone_number)

            if user:
                if user.user_type == "1":
                    return render(request, 'secretary_page.html', {'phone_number': user.phone_number})
                elif user.user_type == "2":
                    try:
                        return render(request, 'customer_page.html', {'phone_number': user.phone_number})
                    except Exception as e:
                        error_message = f"Login failed: {str(e)}"
                        return render(request, 'register_or_login.html', {'error_message': error_message})

            error_message = "Login failed. Please check your phone number and password and try again."
            return render(request, 'register_or_login.html', {'error_message': error_message})

        else:
            error_message = "Invalid action. Please try again."
            return render(request, 'register_or_login.html', {'error_message': error_message})

    return render(request, 'register_or_login.html')


# views.py
def secretary_register(request):
    if request.method == 'POST':
        clinic_name = request.POST.get('clinic_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        try:
            secretary = Secretary(clinic_name=clinic_name, address=address, phone_number=phone_number)
            if secretary.clinic is None:
                error_message = "Invalid clinic name or address. Please try again."
                return render(request, 'secretary_register.html', {'error_message': error_message})
            else:
                return render(request, 'secretary_page.html', {'phone_number': phone_number})
        except:
            error_message = "Invalid clinic name or address. Please try again."
            return render(request, 'secretary_register.html', {'error_message': error_message})
    else:
        return render(request, 'secretary_register.html')

def secretary_page():
    pass


def customer_page(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        customer = Customer()  # I want to use customer phone number from last page
        if action == 'add_patient':

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            birth_date = request.POST.get('birth_date')
            national_code = request.POST.get('national_code')
            email = request.POST.get('email')
            email_check = email if email else None

            add = customer.add_patient(first_name, last_name, phone_number, birth_date, national_code, email_check)

            if customer:
                if add:  ##raise error
                    return render(request, 'successful_add_patient.html', {'customer': phone_number})
                else:
                    return render(request, 'failed_add_patient.html', {'customer': "failed_add_patient"})

        elif action == "select_patient":
            select_patient = request.POST.get('select_patient')
            if select_patient == "current_user":
                ##use customer phone_number as phone number
                customer = Customer() ##get phone number
                act = request.POST.get('act')
                if act == "update_patient_info":
                    phone_number = request.POST.get('phone_number')  # Assuming you get the patient's phone_number
                    new_first_name = request.POST.get('new_first_name')
                    new_last_name = request.POST.get('new_last_name')
                    new_phone_number = request.POST.get('new_phone_number')
                    new_email = request.POST.get('new_email')
                    new_national_code = request.POST.get('new_national_code')
                    new_birthdate = request.POST.get('new_birthdate')

                    # Call the update_patient_info method
                    customer.update_patient_info(
                        new_phone_number=new_phone_number,
                        new_first_name=new_first_name,
                        new_last_name=new_last_name,
                        new_email=new_email,
                        new_birthdate=new_birthdate,
                        new_national_code=new_national_code
                    )
                    if customer.update_patient_info(
                            new_phone_number=new_phone_number,
                            new_first_name=new_first_name,
                            new_last_name=new_last_name,
                            new_email=new_email,
                            new_birthdate=new_birthdate,
                            new_national_code=new_national_code
                    ):
                        return render(request, 'update_patient.html')
                    else:
                        return render(request, 'update_patient_failed.html')

                elif act == "remove_patient_info":
                    customer_phone_number = request.POST.get(
                        'customer_phone_number')  # Assuming you pass the customer's phone number
                    customer = Customer(customer_phone_number)

                    # Check if the user_phone and phone_number exist in the user_patient table
                    customer.remove_patient()

                    return render(request, 'remove_patient.html')

                elif act == "view_current_appointment":
                    customer_phone_number = request.POST.get(
                        'customer_phone_number')  # Assuming you pass the customer's phone number
                    customer = Customer(customer_phone_number)

                    # Delegate the view_current_appointments functionality to the Patient class
                    appointments = customer.view_current_appointments()

                    return render(request, 'view_current_appointments.html', {'appointments': appointments})

                elif act == "view_appointment_history":
                    customer_phone_number = request.POST.get(
                        'customer_phone_number')  # Assuming you pass the customer's phone number
                    customer = Customer(customer_phone_number)

                    # Delegate the view_appointments_history functionality to the Patient class
                    appointments_history = customer.view_appointments_history()

                    return render(request, 'view_appointments_history.html',
                                  {'appointments_history': appointments_history})

                elif act == "add_appointment.html":
                    customer_phone_number = request.POST.get(
                        'customer_phone_number')  # Assuming you pass the customer's phone number
                    doctor_phone_number = request.POST.get('doctor_phone_number')
                    clinic_name = request.POST.get('clinic_name')
                    date = request.POST.get('date')
                    time = request.POST.get('time')

                    customer = Customer(customer_phone_number)

                    # Delegate the add_appointment.html functionality to the Appointment class
                    customer.add_appointment(doctor_phone_number, clinic_name, date, time)

                    return render(request, 'add_appointment.html')
                elif act == "cancel_appointment":
                    customer_phone_number = request.POST.get(
                        'customer_phone_number')  # Assuming you pass the customer's phone number
                    date = request.POST.get('date')
                    time = request.POST.get('time')

                    customer = Customer(customer_phone_number)

                    # Delegate the cancel_appointment functionality to the Appointment class
                    customer.cancel_appointment(date, time)

                    return render(request, 'cancel_appointment.html')

                elif act == "reschedule_appointment":
                    customer_phone_number = request.POST.get(
                        'customer_phone_number')  # Assuming you pass the customer's phone number
                    old_date = request.POST.get('old_date')
                    old_time = request.POST.get('old_time')
                    new_date = request.POST.get('new_date')
                    new_time = request.POST.get('new_time')

                    customer = Customer(customer_phone_number)

                    # Delegate the reschedule_appointment functionality to the Appointment class
                    customer.reschedule_appointment(old_date, old_time, new_date, new_time)

                    return render(request, 'reschedule_appointment.html')

            elif select_patient == "another_patient":
                phone_number = request.POST.get('phone_number')
                customer = Customer(phone_number)
                act = request.POST.get('act')

                if act == "update_patient_info":
                    new_first_name = request.POST.get('new_first_name')
                    new_last_name = request.POST.get('new_last_name')
                    new_phone_number = request.POST.get('new_phone_number')
                    new_email = request.POST.get('new_email')
                    new_national_code = request.POST.get('new_national_code')
                    new_birthdate = request.POST.get('new_birthdate')

                    # Call the update_patient_info method
                    customer.update_patient_info(
                        new_phone_number=new_phone_number,
                        new_first_name=new_first_name,
                        new_last_name=new_last_name,
                        new_email=new_email,
                        new_birthdate=new_birthdate,
                        new_national_code=new_national_code
                    )

                    return render(request, 'update_patient.html')

                elif act == "remove_patient_info":

                    # Check if the user_phone and phone_number exist in the user_patient table
                    customer.remove_patient()

                    return render(request, 'remove_patient.html')

                elif act == "view_current_appointment":

                    # Delegate the view_current_appointments functionality to the Patient class
                    appointments = customer.view_current_appointments()

                    return render(request, 'view_current_appointments.html', {'appointments': appointments})

                elif act == "view_appointment_history":

                    # Delegate the view_appointments_history functionality to the Patient class
                    appointments_history = customer.view_appointments_history()

                    return render(request, 'view_appointments_history.html',
                                  {'appointments_history': appointments_history})

                elif act == "add_appointment":
                    doctor_phone_number = request.POST.get('doctor_phone_number')
                    clinic_name = request.POST.get('clinic_name')
                    date = request.POST.get('date')
                    time = request.POST.get('time')

                    # Delegate the add_appointment functionality to the Appointment class
                    customer.add_appointment(doctor_phone_number, clinic_name, date, time)

                    return render(request, 'add_appointment.html')

                elif act == "cancel_appointment":

                    date = request.POST.get('date')
                    time = request.POST.get('time')

                    # Delegate the cancel_appointment functionality to the Appointment class
                    customer.cancel_appointment(date, time)

                    return render(request, 'cancel_appointment.html')

                elif act == "reschedule_appointment":

                    old_date = request.POST.get('old_date')
                    old_time = request.POST.get('old_time')
                    new_date = request.POST.get('new_date')
                    new_time = request.POST.get('new_time')

                    # Delegate the reschedule_appointment functionality to the Appointment class
                    customer.reschedule_appointment(old_date, old_time, new_date, new_time)

                    return render(request, 'reschedule_appointment.html')

    else:
        return render(request, 'customer_page.html')