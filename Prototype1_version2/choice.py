import tkinter
from login import open_login_window
from register import open_register_window

def open_choice_window():
    window = tkinter.Tk()
    window.title("Choose")
    window.geometry('200x100')

    choice_label = tkinter.Label(window, text="Login or Register?")
    choice_label.grid(row=0, column=0, columnspan=2)

    login_button = tkinter.Button(window, text="Login", command=lambda: (window.destroy(), open_login_window()))
    login_button.grid(row=1, column=0)
    register_button = tkinter.Button(window, text="Register", command=lambda: (window.destroy(), open_register_window()))
    register_button.grid(row=1, column=1)

    window.mainloop()

