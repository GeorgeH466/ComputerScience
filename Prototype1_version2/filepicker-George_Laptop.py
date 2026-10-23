import tkinter as tk
from tkinter import filedialog

def open_a_file():
    file_object = filedialog.askopenfile(mode='r', title="Select a file to open")
    if file_object:
        print(f"File selected: {file_object.name}")
        first_line = file_object.readline().strip()
        print(f"First line content: {first_line}")
        file_object.close()
    else:
        print("No file selected or dialog canceled.")

root = tk.Tk()
root.title("File Box")
root.geometry("300x100")
button = tk.Button(root, text="Open File", command=open_a_file)
button.pack(padx=20, pady=20)
root.mainloop()