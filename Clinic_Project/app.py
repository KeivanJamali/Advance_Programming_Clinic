import re
from user import User
from secretary import Secretary
from customer import Customer


def get_phone_number():
    """
    Prompts the user to enter a phone number, validates the input according to a specific pattern, and returns the phone number if it is valid.
    """
    phone_number = input("Enter your phone number:")
    pattern = r"^\d{11}$"
    if re.match(pattern, phone_number):
        print("[REPLY] Valid phone number")
        return int(phone_number)
    else:
        print("[REPLY] Invalid phone number")


def get_first_name():
    """
    Asks the user to enter their first name and returns the input as a string.
    """
    first_name = input("Enter your first number:")
    return first_name


def get_last_name():
    """
    Function to prompt the user to enter their last name and return the input as the last name.
    """
    last_name = input("Enter your last name:")
    return last_name


def get_password():
    """
    Takes user input for a password and checks if it meets the specified criteria.
    requires at least one lowercase letter
    requires at least one uppercase letter
    requires at least one digit
    requires at least one special character from the given set: @$!%*?&

    Parameters:
        None

    Returns:
        str: The valid password entered by the user.

    Raises:
        None
    """
    password = input("Enter your password:")
    if re.match(r"^(?=.*[a-zA-Z0-9]).{4,}$", password):
        print("[REPLY] Valid password")
        return password
    else:
        print("[REPLY] Invalid password")


def get_email():
    """
    Prompts the user to enter an email address, validates it, and returns it if valid.
    """
    email = input(
        "Enter your email address(if you don't want to enter one, please enter 'N'):"
    )
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, email) or email == "N":
        print("[REPLY] Valid email address")
        return email
    else:
        print("[REPLY] Invalid email address")


def choose_user_type():
    """
    Prompts the user to enter their user type and returns the user type if it is "Secretary" or "Customer".
    """
    user_type = input("Enter your user type:\n1. Secretary\n2. Customer\n")
    if user_type == "1" or user_type == "2":
        return user_type


def register_or_login(user):
    """
    This function allows a user to register or login. It takes a 'user' object as a parameter and returns the result of the registration or login attempt.
    """
    act = input("Register or login?")
    phone_number = None
    password = None
    if act == "Register" or act == "register":
        first_name = None
        last_name = None
        email = None
        user_type = None
        email_check = None
        while phone_number is None:
            phone_number = get_phone_number()
        while first_name is None:
            first_name = get_first_name()
        while last_name is None:
            last_name = get_last_name()
        while password is None:
            password = get_password()
        while email is None:
            email = get_email()
            email_check = email if email != "N" else None
        while user_type is None:
            user_type = choose_user_type()

        return user.register_user(
            first_name, last_name, password, phone_number, user_type, email_check
        )

    elif act == "Login" or act == "login":
        phone_number = get_phone_number()
        password = get_password()

        return user.login_user(password, phone_number)

    else:
        print("[REPLY] Invalid action. Try again!")


def main():
    """
    Main function for handling user and secretary interactions in the clinic system.
    """
    exit_ = False
    while not exit_:
        user = User()
        user = register_or_login(user)
        if user.user_type == "1":
            while not exit_:
                clinic_name = input("Enter clinic name:")
                address = input("Enter address:")
                try:
                    secretary = Secretary(clinic_name, address, user.phone_number)
                    if secretary.clinic is None:
                        print("[REPLY] Invalid clinic name or address. Try again!")
                        continue
                except:
                    print("[REPLY] Invalid clinic name or address. Try again!")
                    continue
                while not exit_:
                    print("1- Add or Select Doctor")
                    print("2- Update Clinic Profile")
                    print("3- View Appointments for Clinic")
                    print("4- View Profile")
                    print("5- Exit")

                    act_home_page = input("Enter your action number:")

                    if act_home_page == "1":
                        while not exit_:
                            phone_number = input("Enter phone number: ")
                            first_name = input("Enter first name: ")
                            last_name = input("Enter last name: ")
                            try:
                                secretary.add_or_select_doctor(phone_number, first_name, last_name)
                            except:
                                print("[REPLY] Invalid phone number or first name or last name. Try again!")
                                continue
                            while not exit_:
                                print("1- Update Doctor Profile")
                                print("2- Edit appointments for Doctor")
                                print("3- View Schedule for Doctor")
                                print("4- Back")
                                print("5- Exit")

                                act_doctor_page = input("Enter your action number: ")

                                if act_doctor_page == "1":
                                    new_first_name = input(
                                        "Enter new first name (if you don't want to enter one, please enter 'N'): ")
                                    new_last_name = input(
                                        "Enter new last name (if you don't want to enter one, please enter 'N'): ")
                                    new_phone_number = input(
                                        "Enter new phone number (if you don't want to enter one, please enter 'N'):")
                                    new_first_name = new_first_name if new_first_name != "N" else None
                                    new_last_name = new_last_name if new_last_name != "N" else None
                                    new_phone_number = new_phone_number if new_phone_number != "N" else None
                                    try:
                                        secretary.update_doctor_profile(new_first_name, new_last_name, new_phone_number)
                                    except:
                                        print("[REPLY] Invalid first name or last name or phone number. Try again!")
                                        continue

                                elif act_doctor_page == "2":
                                    old_date = input("Enter old date(yyyy/mm/dd): ")
                                    old_time = input("Enter old time(hh:mm): ")
                                    new_date = input("Enter new date(yyyy/mm/dd): ")
                                    new_time = input("Enter new time(hh:mm): ")
                                    try:
                                        secretary.edit_appointments_for_doctor(old_date, old_time, new_date, new_time)
                                    except:
                                        print("[REPLY] Invalid date or time. Try again!")
                                        continue

                                elif act_doctor_page == "3":
                                    secretary.view_schedule_for_doctor()

                                elif act_doctor_page == "4":
                                    break

                                elif act_doctor_page == "5":
                                    exit_ = True
                                    break

                                else:
                                    print("[REPLY] Invalid action. Try again!")
                                    continue

                    elif act_home_page == "2":
                        new_clinic_name = input(
                            "Enter new clinic name (if you don't want to enter one, please enter 'N'): ")
                        new_address = input("Enter new address (if you don't want to enter one, please enter 'N'): ")
                        new_clinic_name = new_clinic_name if new_clinic_name != "N" else None
                        new_address = new_address if new_address != "N" else None
                        try:
                            secretary.update_clinic_profile(new_clinic_name, new_address)
                        except:
                            print("[REPLY] Invalid clinic name or address. Try again!")
                            continue

                    elif act_home_page == "3":
                        secretary.view_appointments_for_clinic()

                    elif act_home_page == "4":
                        print(secretary)

                    elif act_home_page == "5":
                        exit_ = True
                        break

                    else:
                        print("[REPLY] Invalid action. Try again!")
                        continue

        elif user.user_type == "2":
            customer = Customer(user.phone_number)
            while exit_ is False:
                print("1- Add Patient")
                print("2- Select Patient")
                print("3- Exit")
                act_home_page = input("Enter your action number: ")

                if act_home_page == "1":
                    first_name = input("Enter first name: ")
                    last_name = input("Enter last name: ")
                    phone_number = input("Enter phone number: ")
                    birthdate = input("Enter birth date(yyyy-mm-dd): ")
                    national_code = input("Enter national code: ")
                    email = input("Enter email (if you don't want to enter one, please enter 'N'): ")
                    email = email if email != "N" else None
                    try:
                        customer.add_patient(first_name, last_name, phone_number, birthdate, national_code, email)
                    except:
                        print(
                            "[REPLY] Invalid first name or last name or phone number or birth date or national code. Try again!")
                        continue

                elif act_home_page == "2":
                    while exit_ is False:
                        print("1- Current User as Patient")
                        print("2- Patient Other Than User")
                        print("3- Exit")
                        act_doctor_page = input("Enter your action number: ")

                        if act_doctor_page == "1":
                            customer.select_patient(user.phone_number)
                            print("[REPLY] Current User as Patient")

                        elif act_doctor_page == "2":
                            try:
                                phone_number_patient = input("Enter patient phone number: ")
                            except:
                                print("[REPLY] Invalid patient phone number. Try again!")
                                continue
                            customer.select_patient(phone_number_patient)

                        elif act_doctor_page == "3":
                            exit_ = True
                            break

                        while not exit_:
                            print("1- Update Patient Info")
                            print("2- Remove Patient")
                            print("3- View Current Appointments for Patient")
                            print("4- View Appointments History for Patient")
                            print("5- Add Appointment")
                            print("6- Remove Appointment")
                            print("7- Reschedule Appointment")
                            print("8- Back")
                            print("9- Exit")
                            act_patient_page = input("Enter your action number: ")

                            if act_patient_page == "1":
                                new_phone_number = input(
                                    "Enter new phone number (if you don't want to enter one, please enter 'N'):")
                                new_first_name = input(
                                    "Enter new first name (if you don't want to enter one, please enter 'N'): ")
                                new_last_name = input(
                                    "Enter new last name (if you don't want to enter one, please enter 'N'): ")
                                new_email = input(
                                    "Enter new phone number (if you don't want to enter one, please enter 'N'):")
                                new_birthday = input(
                                    "Enter new first name (if you don't want to enter one, please enter 'N'): ")
                                new_national = input(
                                    "Enter new last name (if you don't want to enter one, please enter 'N'): ")

                                new_phone_number = new_phone_number if new_phone_number != "N" else None
                                new_first_name = new_first_name if new_first_name != "N" else None
                                new_last_name = new_last_name if new_last_name != "N" else None
                                new_email = new_email if new_email != "N" else None
                                new_birthday = new_birthday if new_birthday != "N" else None
                                new_national = new_national if new_national != "N" else None

                                try:
                                    customer.update_patient_info(new_phone_number, new_first_name, new_last_name, new_email,
                                                                 new_birthday, new_national)
                                except:
                                    print(
                                        "[REPLY] Invalid phone number or first name or last name or email or birthday or national code. Try again!")
                                    continue
                                print("[REPLY] Patient Info Updated")

                            elif act_patient_page == "2":
                                customer.remove_patient()
                                print("[REPLY] Patient Removed")

                            elif act_patient_page == "3":
                                customer.view_current_appointments()
                                print("[REPLY] Current Appointments")

                            elif act_patient_page == "4":
                                customer.view_appointments_history()
                                print("[REPLY] Appointments History")

                            elif act_patient_page == "5":
                                doctor_phone_number = input("Enter phone number for doctor: ")
                                clinic_name = input("Enter clinic name: ")
                                date = input("Enter date(yyyy-mm-dd): ")
                                time = input("Enter time(hh-mm): ")
                                try:
                                    customer.add_appointment(doctor_phone_number, clinic_name, date, time)
                                except:
                                    print("[REPLY] Invalid doctor phone number or clinic name or date or time. Try again!")
                                    continue

                            elif act_patient_page == "6":
                                date = input("Enter date(yyyy-mm-dd): ")
                                time = input("Enter time(hh-mm): ")
                                try:
                                    customer.cancel_appointment(date, time)
                                except:
                                    print("[REPLY] Invalid date or time. Try again!")
                                    continue

                            elif act_patient_page == "7":
                                old_date = input("Enter old date(yyyy-mm-dd): ")
                                old_time = input("Enter old time(hh-mm): ")
                                new_date = input("Enter new date(yyyy-mm-dd): ")
                                new_time = input("Enter new time(hh-mm): ")
                                try:
                                    customer.reschedule_appointment(old_date, old_time, new_date, new_time)
                                except:
                                    print("[REPLY] Invalid old date or old time or new date or new time. Try again!")
                                    continue

                            elif act_patient_page == "8":
                                break

                            elif act_patient_page == "9":
                                exit_ = True
                                break

                elif act_home_page == "3":
                    exit_ = True
                    break


main()
