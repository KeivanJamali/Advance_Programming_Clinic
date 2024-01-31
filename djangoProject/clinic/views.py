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
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            user_type = request.POST.get("user_type")
            email_check = email if email else None

            user = user.register_user(first_name, last_name, password, phone_number, user_type, email_check)

            if user:
                if user.user_type == "1":
                    return render(request, "secretary_register.html", {"phone_number": user.phone_number})
                elif user.user_type == "2":
                    try:
                        return render(request, "customer_page.html", {"phone_number": user.phone_number})
                    except Exception as e:
                        error_message = f"Registration failed: {str(e)}"
                        return render(request, "register_or_login.html", {"error_message": error_message})

            error_message = "Registration failed. Please check your inputs and try again."
            return render(request, "register_or_login.html", {"error_message": error_message})

        elif act == "login":
            user = user.login_user(password, phone_number)

            if user:
                if user.user_type == "1":
                    return render(request, "secretary_page.html", {"phone_number": user.phone_number})
                elif user.user_type == "2":
                    try:
                        return render(request, "customer_page.html", {"phone_number": user.phone_number})
                    except Exception as e:
                        error_message = f"Login failed: {str(e)}"
                        return render(request, "register_or_login.html", {"error_message": error_message})

            error_message = "Login failed. Please check your phone number and password and try again."
            return render(request, "register_or_login.html", {"error_message": error_message})

        else:
            error_message = "Invalid action. Please try again."
            return render(request, "register_or_login.html", {"error_message": error_message})

    return render(request, "register_or_login.html")


# views.py
def secretary_register(request):
    if request.method == "POST":
        clinic_name = request.POST.get("clinic_name")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")
        try:
            secretary = Secretary(phone_number=phone_number, clinic_name=clinic_name, address=address)
            if secretary.clinic is None:
                error_message = "Invalid clinic name or address. Please try again."
                return render(request, "secretary_register.html", {"error_message": error_message})
            else:
                return render(request, "secretary_page.html", {"phone_number": phone_number})
        except:
            error_message = "Invalid clinic name or address. Please try again."
            return render(request, "secretary_register.html", {"error_message": error_message})
    else:
        return render(request, "secretary_register.html")


def secretary_page(request):
    if request.method == 'POST':
        submitted = request.POST.get('submitted')
        if submitted:
            action = request.POST.get('action')
            phone_number = request.POST.get('phone_number')
            secretary = Secretary(phone_number=phone_number).pick_clinic()

            if action == '2':
                doctor_phone_number = request.POST.get('doctor_phone_number')
                doctor_first_name = request.POST.get('doctor_first_name')
                doctor_last_name = request.POST.get('doctor_last_name')
                try:
                    secretary.add_or_select_doctor(doctor_phone_number, doctor_first_name, doctor_last_name)
                    return render(request, 'doctor_page.html',
                                  {'phone_number': phone_number, "doctor_phone_number": doctor_phone_number,
                                   "doctor_first_name": doctor_first_name, "doctor_last_name": doctor_last_name})
                except:
                    error_message = "Invalid phone number or first name or last name. Try again!"
                    return render(request, 'secretary_page.html',
                                  {'error_message': error_message, 'phone_number': phone_number})

            elif action == '3':
                new_clinic_name = request.POST.get('new_clinic_name')
                new_address = request.POST.get('new_address')
                new_clinic_name = new_clinic_name if new_clinic_name else None
                new_address = new_address if new_address else None
                try:
                    secretary.update_clinic_profile(new_clinic_name, new_address)
                    success_message = "Clinic profile updated successfully."
                    return render(request, 'secretary_page.html',
                                  {'success_message': success_message, 'phone_number': phone_number})
                except:
                    error_message = "Invalid clinic name or address. Try again!"
                    return render(request, 'secretary_page.html',
                                  {'error_message': error_message, 'phone_number': phone_number})

            elif action == '4':
                appointments = secretary.view_appointments_for_clinic()
                if appointments:
                    success_message = "Here you are"
                    return render(request, 'secretary_page.html',
                                  {'success_message': success_message, 'appointments': appointments,
                                   'phone_number': phone_number})
                else:
                    success_message = "There are no appointments!"
                    return render(request, 'secretary_page.html',
                                  {'success_message': success_message, 'phone_number': phone_number})

            elif action == "1":
                success_message = f"Secretary phone number: {secretary.phone_number} | Clinic name: {secretary.clinic_name} | Clinic address: {secretary.address}"
                return render(request, 'secretary_page.html',
                              {'success_message': success_message, "phone_number": phone_number})

            elif action == "5":
                return render(request, 'register_or_login.html')


def doctor_page(request):
    if request.method == 'POST':
        submitted = request.POST.get('submitted')
        if submitted:
            action = request.POST.get('action')
            phone_number = request.POST.get('phone_number')
            doctor_phone_number = request.POST.get('doctor_phone_number')
            doctor_first_name = request.POST.get('doctor_first_name')
            doctor_last_name = request.POST.get('doctor_last_name')
            secretary = Secretary(phone_number=phone_number).pick_clinic()
            secretary.add_or_select_doctor(doctor_phone_number, doctor_first_name, doctor_last_name)

            if action == '2':
                new_phone_number = request.POST.get('new_phone_number')
                new_first_name = request.POST.get('new_first_name')
                new_last_name = request.POST.get('new_last_name')
                new_first_name = new_first_name if new_first_name else doctor_first_name
                new_last_name = new_last_name if new_last_name else doctor_last_name
                new_phone_number = new_phone_number if new_phone_number else doctor_phone_number
                try:
                    result = secretary.update_doctor_profile(new_first_name, new_last_name, new_phone_number)

                    if result:
                        success_message = f"Doctor phone number: {new_phone_number} | First name: {new_first_name} | Last name: {new_last_name} updated."
                        return render(request, "doctor_page.html",
                                      {"success_message": success_message, "phone_number": phone_number,
                                       "doctor_phone_number": new_phone_number, "doctor_first_name": new_first_name,
                                       "doctor_last_name": new_last_name})
                    else:
                        error_message = f"Already exist!"
                        return render(request, "doctor_page.html",
                                      {"error_message": error_message, "phone_number": phone_number,
                                       "doctor_phone_number": new_phone_number, "doctor_first_name": new_first_name,
                                       "doctor_last_name": new_last_name})
                except:
                    error_message = "Invalid phone number or first name or last name. Try again!"
                    return render(request, 'doctor_page.html',
                                  {'error_message': error_message, 'phone_number': phone_number,
                                   "doctor_phone_number": doctor_phone_number, "doctor_first_name": doctor_first_name,
                                   "doctor_last_name": doctor_last_name})

            elif action == '3':
                new_date = request.POST.get('new1_date')
                new_time = request.POST.get('new1_time')
                try:
                    result = secretary.add_or_select_doctor(doctor_phone_number, doctor_first_name, doctor_last_name,
                                                            new_date, new_time)
                    if result:
                        success_message = f"Successfully added {new_date} {new_time}."
                        return render(request, 'doctor_page.html',
                                      {"success_message": success_message, "phone_number": phone_number,
                                       "doctor_phone_number": doctor_phone_number,
                                       "doctor_first_name": doctor_first_name, "doctor_last_name": doctor_last_name})
                    else:
                        error_message = "Something went Wrong. Try again!"
                        return render(request, 'doctor_page.html',
                                      {'error_message': error_message, 'phone_number': phone_number,
                                       "doctor_phone_number": doctor_phone_number,
                                       "doctor_first_name": doctor_first_name,
                                       "doctor_last_name": doctor_last_name})
                except:
                    error_message = "Invalid date or time. Try again!"
                    return render(request, 'doctor_page.html',
                                  {'error_message': error_message, 'phone_number': phone_number,
                                   "doctor_phone_number": doctor_phone_number, "doctor_first_name": doctor_first_name,
                                   "doctor_last_name": doctor_last_name})

            elif action == '4':
                new_date = request.POST.get('new2_date')
                new_time = request.POST.get('new2_time')
                old_date = request.POST.get('old_date')
                old_time = request.POST.get('old_time')
                try:
                    secretary.edit_appointments_for_doctor(old_date, old_time, new_date, new_time)
                    success_message = f"Successfully changed to {new_date} {new_time}."
                    return render(request, 'doctor_page.html',
                                  {"success_message": success_message, "phone_number": phone_number,
                                   "doctor_phone_number": doctor_phone_number, "doctor_first_name": doctor_first_name,
                                   "doctor_last_name": doctor_last_name})

                except:
                    error_message = "Invalid date or time. Try again!"
                    return render(request, 'doctor_page.html',
                                  {'error_message': error_message, 'phone_number': phone_number,
                                   "doctor_phone_number": doctor_phone_number, "doctor_first_name": doctor_first_name,
                                   "doctor_last_name": doctor_last_name})

            elif action == "1":
                try:
                    success_message = f"Successfully rendered schedule."
                    schedule = secretary.view_schedule_for_doctor()
                    return render(request, 'doctor_page.html',
                                  {"success_message": success_message, "schedule": schedule,
                                   "phone_number": phone_number, "doctor_phone_number": doctor_phone_number,
                                   "doctor_first_name": doctor_first_name, "doctor_last_name": doctor_last_name})
                except:
                    error_message = f"Something went wrong"
                    return render(request, 'secretary_page.html',
                                  {'error_message': error_message, 'phone_number': phone_number,
                                   "doctor_phone_number": doctor_phone_number, "doctor_first_name": doctor_first_name,
                                   "doctor_last_name": doctor_last_name})

            elif action == "5":
                return render(request, 'secretary_page.html', {'phone_number': phone_number})

            elif action == "6":
                return render(request, 'register_or_login.html')

            return render(request, 'doctor_page.html',
                          {'phone_number': phone_number, "doctor_phone_number": doctor_phone_number,
                           "doctor_first_name": doctor_first_name, "doctor_last_name": doctor_last_name})
