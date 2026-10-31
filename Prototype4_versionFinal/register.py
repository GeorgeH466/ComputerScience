import tkinter
from tkinter import messagebox
from database_connection import create_connection
from password_hash import create_hash
from log import log_event
import random
import string

min_length = 6

def random_username_suggestion(username):
    base = username
    random_part = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    return base + random_part

def validate_reg_input(username, password):#validates the username and password against current rule
    if len(username) == 0:
        return False
    elif len(password) < min_length:
        return False
    return True # returns true if it follows the rules

def register():
    username = new_username_box.get()#gets the inputs from the boxes
    password = new_password_box.get()

    if not validate_reg_input(username, password): # shows an error box if it doesnt follow the requirements
        messagebox.showerror("Error", "Username or password does not meet requirements.")
        return

    connection = create_connection() #creates the connection
    cursor = connection.cursor()

    cursor.execute("SELECT username FROM user_account WHERE username=%s", (username,)) #checks if username exists
    result = cursor.fetchone()

    if result:#if username exists then it adds a string on the end in a message box and then logs it
        suggestion = random_username_suggestion(username)
        messagebox.showerror("Error",f"Username '{username}' is already taken.\nTry: {suggestion}")#using f"" so that i can have variables inside of the message box
        log_event(f"User attempted to register with existing username '{username}'")
        return

    #if the username is correct then it allows the rest to happen
    hashed, salt = create_hash(password)

    cursor.execute("""
        INSERT INTO user_account (username, password_hash, salt)
        VALUES (%s, %s, %s)
    """, (username, hashed, salt)) #inputs the new user record

    connection.commit()#saves the results
    cursor.close()#stops the cursor
    connection.close()#closes the connection

    messagebox.showinfo("Success", "Account created!")#shows the success of as new account creation
    log_event(f"New account created for username '{username}'")#logs the creation

def open_register_window():
    global new_username_box, new_password_box#makes the register function able to use these variables

    window = tkinter.Tk()#creates the initial window
    window.title("Register")#labels the initial window
    window.geometry('400x100')#controls the geometry of the window
    #create and positions the word username and the entry box
    register_label = tkinter.Label(window, text="New Username")
    register_label.grid(row=0, column=0)
    new_username_box = tkinter.Entry(window)
    new_username_box.grid(row=0, column=1)
    #create and positions the word password and the entry box
    new_password_label = tkinter.Label(window, text="New Password")
    new_password_label.grid(row=1, column=0)
    new_password_box = tkinter.Entry(window, show="*")#makes it so the password can't be seen when types, removing the ability to read over someone's shoulder
    new_password_box.grid(row=1, column=1)
    #creates and positions the button to confirm the registering
    register_button = tkinter.Button(window, text="Register", command=register)
    register_button.grid(row=2, column=1)

    password_rule_label = tkinter.Label(window, text="minimum length 6 characters")
    password_rule_label.grid(row=2, column=0)

    window.mainloop()

if __name__ == '__choice__':
    open_register_window()