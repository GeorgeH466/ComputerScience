import tkinter
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
    init_register()