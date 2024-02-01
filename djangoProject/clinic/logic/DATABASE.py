import mysql.connector

database = ["localhost", "3306", "root", "@Erfan1229", "clinic_data"]


def establish_connection():
    """
    Establishes a connection to the MySQL database.

    :return: The established database connection.
    :rtype: mysql.connector.connection.MySQLConnection
    """
    connection = mysql.connector.connect(
        host=f"{database[0]}",
        port=f"{database[1]}",
        user=f"{database[2]}",
        password=f"{database[3]}",
        database=f"{database[4]}",
        buffered=True
    )
    return connection
