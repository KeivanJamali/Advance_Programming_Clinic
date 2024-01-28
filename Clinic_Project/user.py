from DATABASE import establish_connection


class User:
    def __init__(self):
        """
        Constructor for initializing the attributes: 
        first_name, last_name, password, phone_number, 
        user_type, and email.
        """
        self.first_name = None
        self.last_name = None
        self.password = None
        self.phone_number = None
        self.user_type = None
        self.email = None

    def register_user(self, first_name, last_name, password, phone_number, user_type, email=None):
        """
        Register a new user with the provided information.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            password (str): The password of the user.
            phone_number (str): The phone number of the user.
            user_type (str): The type of user.
            email (str, optional): The email of the user (default is None).

        Returns:
            User: The registered user object.
        """
        connection = establish_connection()
        cursor = connection.cursor()

        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.phone_number = phone_number
        self.user_type = user_type
        self.email = email

        # Check if user already exists
        query = "SELECT COUNT(*) FROM user_table WHERE phone_number = %s"
        cursor.execute(query, (self.phone_number,))
        result = cursor.fetchone()

        if result[0] > 0:
            print("[Wrong] User with the given phone number already exists.")
            return

        # Insert new user into the database
        query = "INSERT INTO user_table (first_name, last_name, phone_number, password, user_type, email) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query,
                       (self.first_name, self.last_name, self.phone_number, self.password, self.user_type, self.email))
        print("[INFO] Registered")
        query = """
        SELECT user_id 
        FROM user_table
        WHERE phone_number = %s
        """
        values = (self.phone_number,)
        cursor.execute(query, values)
        self.user_id = cursor.fetchone()[0]

        connection.commit()
        cursor.close()
        connection.close()
        return self

    def login_user(self, password, phone_number):
        """
        Logs in a user using the provided password and phone number.

        Parameters:
            password (str): The password of the user.
            phone_number (str): The phone number of the user.

        Returns:
            self: The updated user object.
        """
        connection = establish_connection()
        cursor = connection.cursor()

        # Check if user exists in the database
        query = "SELECT * FROM user_table WHERE phone_number = %s"
        cursor.execute(query, (phone_number,))
        result = cursor.fetchone()

        if result[5] != password:
            return

        self.password = password
        self.phone_number = phone_number

        if result:
            # User exists, assign database values to object attributes
            self.user_id = result[0]
            self.first_name = result[1]
            self.last_name = result[2]
            self.email = result[3] if result[3] else None
            self.user_type = result[6]

        else:
            print("[Wrong] User does not exist.")

        cursor.close()
        connection.close()
        return self
