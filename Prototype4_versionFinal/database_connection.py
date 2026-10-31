import mysql.connector
from mysql.connector import Error

def create_connection():#creates the connection to the database
    try:
        connection = mysql.connector.connect(
            host="localhost",#wether local host or online hosting
            user="root",#username of the user being used to access database
            password="hello",#password to database
            database="project"#database name
        )
        return connection#returns the result of the connection and allows futher things to be done

    except Error as e:#outputs errors if they appear
        print("Database error:", e)
        return None

if __name__ == '__main__':
    create_connection()
