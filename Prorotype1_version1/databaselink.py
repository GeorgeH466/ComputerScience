import mysql.connector
from mysql.connector import Error

def create_connection():#function for connecting to database initially
    try:
        connection = mysql.connector.connect(
            host="localhost",        # whether the server is hosted locally or on an IP
            user="root",             # the username of the user of the database being used
            password="hello",        # password of the database made when the msqlserver was setup
            database="project"       # name of the database schema being used 
        )

        if connection.is_connected():#tells the user that he database is successfully connected
            print("You are Connected to The MySQL database sever")
            return connection #returns the value of the connection to see if it is null or not

    except Error:
        print("Error while connecting to MySQL:", Error)
    
    finally:#is done whether the try fails or not
        if connection.is_connected():#closes the connection if it hasnt already closed so that it doesnt stay open when it doesnt need to be, which mitigates accidental editing
            connection.close()

if __name__ == '__main__':
    create_connection()