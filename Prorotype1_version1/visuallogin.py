import tkinter
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
    open_login_window()