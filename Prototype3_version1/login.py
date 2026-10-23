import tkinter
from tkinter import messagebox
from database_connection import create_connection
from password_hash import check_password
from log import log_event
from sidebar import create_sidebar
def login():
    username = username_box.get()
    password = password_box.get()

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT password_hash, failed_attempts, lockoutstatus FROM user_account WHERE username=%s", (username,))
    result = cursor.fetchone()

    if not result:
        messagebox.showerror("Error", "User not found")
        return

    stored_hash, lockout_attempts, lockout_status = result

    if lockout_attempts >= 5 or lockout_status:
        messagebox.showerror("Error", "Account locked due to too many failed attempts.")
        cursor.execute("UPDATE user_account SET lockoutstatus=%s WHERE username=%s", (True, username))
        connection.commit()
        log_event("User attempted to access locked account")
        return

    if check_password(password, stored_hash):
        messagebox.showinfo("Success", "Login successful!")
        log_event(f"User '{username}' logged in successfully")

        cursor.execute("UPDATE user_account SET failed_attempts=%s WHERE username=%s", (0, username))
        connection.commit()

        cursor.close()
        connection.close()

        window.destroy()      
        create_sidebar()     
        return

    # incorrect password
    messagebox.showerror("Error", "Incorrect password")
    cursor.execute("UPDATE user_account SET failed_attempts=%s WHERE username=%s", (lockout_attempts + 1, username))
    connection.commit()

    cursor.close()
    connection.close()


def open_login_window():
    global username_box, password_box, window

    window = tkinter.Tk()#creates the initial window
    window.title("Login")#labels the initial window
    window.geometry('200x100')#controls the geometry of the window
    #create and positions the word username and the entry box
    username_label = tkinter.Label(window, text="Username")
    username_label.grid(row=0, column=0)
    username_box = tkinter.Entry(window)
    username_box.grid(row=0, column=1)
    #create and positions the word password and the entry box
    password_label = tkinter.Label(window, text="Password")
    password_label.grid(row=1, column=0)
    password_box = tkinter.Entry(window, show="*")
    password_box.grid(row=1, column=1)
    #creates and positions the button to confirm the login
    login_button = tkinter.Button(window, text="Login", command=login)
    login_button.grid(row=2, column=1)

    window.mainloop()

if __name__ == '__choice__':
    open_login_window()