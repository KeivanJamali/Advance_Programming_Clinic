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

