import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook

def customer_amount_for_spreadsheet():#creates the spreadsheet popup box
    number_input_popup = tk.Toplevel()
    number_input_popup.title("customer_amount_for_spreadsheet")
    number_input_popup.geometry("300x150")  # small popup window

    tk.Label(number_input_popup, text="Enter customer amount:").pack(pady=10)

    amount_int = tk.StringVar()
    entry = tk.Entry(number_input_popup, textvariable=amount_int, font=("Arial", 14))
    entry.pack(pady=5)
    entry.focus()

    def confirm():#makes it so that the confirm button actually works
        value = amount_int.get()
        if value.isdigit():
            number_input_popup.result = int(value)
            number_input_popup.destroy()
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid number")

    tk.Button(number_input_popup, text="Confirm", command=confirm).pack(pady=10)#makes it so the confirm button is there to press




def write_spreadsheet(amount):
    # Get the first 'amount' customers from the database
    customers = get_first_customers(amount)

    # Create a new Excel spreadsheet
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Customers"

    # Add column headings
    worksheet.append([
        "Customer ID",
        "Name",
        "Address",
        "Email",
        "Phone"
    ])

    # Add each customer's data to the spreadsheet
    for customer in customers:
        worksheet.append([
            customer["id"],
            customer["name"],
            customer["address"],
            customer["email"],
            customer["phone"]
        ])

    # Save the spreadsheet
    workbook.save("customer_export.xlsx")
