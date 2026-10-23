"""import mysql.connector
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
    create_connection()"""
"""import mysql.connector#importing the whole module
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
    get_user_account_fields()"""
"""import databaselink
from databaselink import create_connection
import Databselinktester
from Databselinktester import get_user_account_fields
import passwordhash
from passwordhash import check_password
from passwordhash import create_hash
import visualchoice
from visualchoice import open_choice_window

"""
"""import bcrypt

def create_hash():
    password = b"testing123"
    salt = bcrypt.gensalt()
    store_salt=str(salt)
    hashed = bcrypt.hashpw(password, salt)
    print(store_salt)
    entered = b"testing123"
def check_password(entered, hashed):
    if bcrypt.checkpw(entered, hashed):
        print("Password correct")
        print(hashed)
    else:
        print("Wrong password")

if __name__ == "__main__":
    create_hash()
    check_password()"""

"""import tkinter
import visuallogin
from visuallogin import open_login_window
import visualregister
from visualregister import open_register_window


def init_login():
    choice_window.destroy()
    open_login_window()
    
def init_register():
    choice_window.destroy
    open_register_window()
    

def open_choice_window():#turns this into an easily runable funciton that can be used more than once easily
    global choice_window
    #creates the initial window
    choice_window = tkinter.Tk()
    choice_window.title("choice box")
    choice_window.geometry('200x200')
#controls what the pieces do and have in them
    choice_label = tkinter.Label(choice_window, text='do you want to register or login')
    login_button = tkinter.Button(choice_window, text="login", command=init_login)
    register_button = tkinter.Button(choice_window, text="register", command=init_register)
    close_button = tkinter.Button(choice_window, text="exit", command = exit)
#controls the position of the pieces

    choice_label.grid(row=0, column=0, columnspan=2)
    login_button.grid(row=1, column=0)
    register_button.grid(row=2, column=0)
    close_button.grid(row=3, column=2)
    choice_window.mainloop()

#makes it so it doesn't automatically run
if __name__ == '__main__':
    open_choice_window()
    init_login()
    init_register()"""

"""import tkinter
from tkinter import messagebox
import visualchoice
def login():
    username="testing123"
    password="testing234"
    if (username_box_Label.get() == username) and (password_box_Label.get() == password):
        messagebox.showinfo(title="login successful", message="You got the credentials right and will now be allowed in")
    else:
        messagebox.showinfo(title="login unsuccessful", message="either the username or password was incorrect")

def open_login_window():#turns this into an easily runable funciton that can be used more than once easily
    global username_box_Label, password_box_Label
    login_window = tkinter.Tk()#creates the initial window
    login_window.title("login box")
    login_window.geometry('200x100')
#controls what the pieces do and have in them
    login_Label = tkinter.Label(login_window, text="Input login details")
    username_Label = tkinter.Label(login_window, text="Username")
    username_box_Label = tkinter.Entry(login_window)
    password_Label = tkinter.Label(login_window, text="password")
    password_box_Label= tkinter.Entry(login_window, show="*")
    login_button= tkinter.Button(login_window, text="confirm", command=login)
    back_button= tkinter.Button(login_window, text="back")
#controls the position of the pieces
    login_Label.grid(row=0, column=0, columnspan=2)
    username_Label.grid(row=1, column=0)
    username_box_Label.grid(row=1, column=1)
    password_Label.grid(row=2, column=0)
    password_box_Label.grid(row=2, column=1)
    login_button.grid(row=3, column=1, columnspan=2,)
    back_button.grid(row=0, column=5, columnspan=2)
    login_window.mainloop()
    
#makes it so it doesn't automatically run
if __name__ == '__main__':
    open_login_window()"""

"""import tkinter
from tkinter import messagebox

def register():
    username=new_username_box_Label.get()
    password=new_password_box_Label.get()
    messagebox.showinfo(title='registration successful', message='you have successfuly created a new user profile')

def open_register_window():
    global new_username_box_Label, new_password_box_Label
        #creates the initial window
    register_window = tkinter.Tk()
    register_window.title("register box")
    register_window.geometry('250x100')
        #controls what the pieces do and have in them
    register_Label = tkinter.Label(register_window, text="Input login details")
    new_username_Label = tkinter.Label(register_window, text="New Username")
    new_username_box_Label = tkinter.Entry(register_window)
    new_password_Label = tkinter.Label(register_window, text="New Password")
    new_password_box_Label= tkinter.Entry(register_window, show="*")
    register_button= tkinter.Button(register_window, text="confirm", command=register)
        #controls the position of the pieces
    register_Label.grid(row=0, column=0, columnspan=2)
    new_username_Label.grid(row=1, column=0)
    new_username_box_Label.grid(row=1, column=1)
    new_password_Label.grid(row=2, column=0)
    new_password_box_Label.grid(row=2, column=1)
    register_button.grid(row=3, column=1, columnspan=2,)
    
    register_window.mainloop()

if __name__ == '__main__':
    open_register_window()"""