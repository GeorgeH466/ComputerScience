import mysql.connector#importing the whole module
from mysql.connector import Error#importing a specific part of the module

def get_user_account_fields():#the function name that makes sense and describes what it is doign
    try:#try except so that i can track errors easier and make it so the code doesnt just break
        connection = mysql.connector.connect(#connecting to the database initially
            host="localhost",
            user="root",
            password="hello",
            database="project"
        )

        if connection.is_connected():#only does things if the databse is connected
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM USER_ACCOUNT LIMIT 1")#selects every piece of data inside the user_account table including field names and data entries.

            columns = [column[0] for column in cursor.description]#gets all the columns in the field that has the column name bcause if it has another type of rule attached to it then it would be a piece of data.

            print("Fields in USER_ACCOUNT table:")#printing all of the fields of the table
            for field in columns:
                print("-", field)#prints the fields of the table on a line each.

    except Error as e:#stops when an error is detected and then says the error
        print("Error:", e)

    finally:#is done whether the try fails or not
        if connection.is_connected():#closes the connection if it hasnt already closed so that it doesnt stay open when it doesnt need to be, which mitigates accidental editing
            connection.close()

if __name__ == '__main__':
    get_user_account_fields()