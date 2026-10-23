import tkinter
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
    open_register_window()