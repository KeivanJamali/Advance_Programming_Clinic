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
        return phone_number
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
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if re.match(pattern, password):
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
    if user_type == "Secretary" or user_type == "Customer":
        return user_type


def register_or_login(user):
    """
    This function allows a user to register or login. It takes a 'user' object as a parameter and returns the result of the registration or login attempt.
    """
    act = input("Register or login?")
    if act == "Register":
        phone_number = None
        first_name = None
        last_name = None
        password = None
        email = None
        user_type = None
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

    elif act == "login":
        while phone_number is None:
            phone_number = get_phone_number()
        while password is None:
            password = get_password()

        return user.login_user(password, phone_number)

    else:
        print("[REPLY] Invalid action. Try again!")


def main():
    """
    Main function for handling user and secretary interactions in the clinic system.
    """
    user = User()
    user = register_or_login(user)
    if user.user_type == "Secretary":
        while exit == False:
            clinic_name = input("Enter clinic name:")
            address = input("Enter address:")
            secretary = Secretary(clinic_name, address, user.phone_number)
            print("1- Add or Select Doctor")
            print("2- Update Clinic Profile")
            print("3- View Appointments for Clinic")
            print("4- View Profile")
            print("5- Exit")
            act = input("Enter your action number:")

            if act == "1":
                while exit == False:
                    phone_number = input("Enter phone number:")
                    first_name = input("Enter first name")
                    last_name = input("Enter last name:")
                    secretary.add_doctor(phone_number, first_name, last_name)

                    print("1- Update Doctor Profile")
                    print("2- Edit appointments for Doctor")
                    print("3- View Schedule for Doctor")
                    print("4- Back")
                    print("5- Exit")
                    act_2 = input("Enter your action number:")

                    if act_2 == "1":
                        new_first_name = input(
                            "Enter new first name (if you don't want to enter one, please enter 'N'):")
                        new_last_name = input("Enter new last name (if you don't want to enter one, please enter 'N'):")
                        new_phone_number = input(
                            "Enter new phone number (if you don't want to enter one, please enter 'N'):")
                        new_phone_number = phone_number if phone_number != "N" else None
                        new_first_name = first_name if first_name != "N" else None
                        new_last_name = last_name if last_name != "N" else None

                        secretary.update_doctor_profile(new_first_name, new_last_name, new_phone_number)

                    elif act_2 == "2":
                        old_date = input("Enter old date:")
                        old_time = input("Enter old time:")
                        new_date = input("Enter new date:")
                        new_time = input("Enter new time:")
                        secretary.edit_appointments_for_doctor(old_date, old_time, new_date, new_time)
                    elif act_2 == "3":
                        secretary.view_schedule_for_doctor()

                    elif act_2 == "4":
                        break
                    elif act_2 == "5":
                        exit = True
                        break


            elif act == "2":
                new_clinic_name = input("Enter new clinic name  (if you don't want to enter one, please enter 'N'):")
                new_address = input("Enter new address (if you don't want to enter one, please enter 'N'):")
                new_clinic_name = new_clinic_name if new_clinic_name != "N" else None
                new_address = new_address if new_address != "N" else None
                secretary.update_clinic_profile(new_clinic_name, new_address)

            elif act == "3":
                secretary.view_appointments_for_clinic()
            elif act == "4":
                print(secretary)
            elif act == "5":
                exit = True
                break




    elif user.user_type == "Customer":
        customer = Customer(user.phone_number)
        while exit is False:
            print("1- Add Patient")
            print("2- Select Patient")
            print("3- Exit")
            act = input("Enter your action number:")

            if act == "1":
                input_ = input()
                customer.add_patient(input_)

            elif act == "2":
                while exit is False:
                    print("1- Current User as Patient")
                    print("2- Patient Other Than User")
                    print("3- Exit")
                    act_2 = input("Enter your action number:")
                    if act_2 == "1":
                        print("[REPLY] Current User as Patient")
                    elif act_2 == "2":
                        pass
                    elif act_2 == "3":
                        exit = True
                        break
                    print("1- Update Patient Info")
                    print("2- Remove Patient")
                    print("3- View Current Appointments for Patient")
                    print("4- View Appointments History for Patient")
                    print("5- Add Appointment")
                    print("6- Remove Appointment")
                    print("7- Reschedule Appointment")
                    print("8- Back")
                    print("9- Exit")
                    act_3 = input("Enter your action number:")
                    if act_3 == "1":
                        pass
                    elif act_3 == "2":
                        pass
                    elif act_3 == "3":
                        pass
                    elif act_3 == "4":
                        pass
                    elif act_3 == "5":
                        pass
                    elif act_3 == "6":
                        pass
                    elif act_3 == "7":
                        pass
                    elif act_3 == "8":
                        break
                    elif act_3 == "9":
                        exit = True
                        break

            elif act == "3":
                exit = True
                break
