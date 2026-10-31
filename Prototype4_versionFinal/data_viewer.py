import tkinter
from tkinter import ttk
import mysql.connector

def db_connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="hello",
        database="project"
    )

def get_customers():
    connection = db_connect()
    cursor = connection.cursor()

    cursor.execute("SELECT customer_name FROM customer")
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [row[0] for row in results]



def get_customer_details():
    global customer_result, location_result, contact_result, system_result, selected_customer_id
    connection = db_connect()
    cursor = connection.cursor()

    # 1. Get customer ID from name
    cursor.execute("SELECT Customer_ID FROM customer WHERE customer_name = %s", (customer_name,))
    row = cursor.fetchone()

    if not row:
        print("Customer not found.")
        return

    customer_id = row[0]
    selected_customer_id = customer_id

    # 2. Retrieve all related tables
    cursor.execute("SELECT * FROM customer WHERE Customer_ID = %s", (customer_id,))
    customer_result = cursor.fetchall()

    cursor.execute("SELECT * FROM customerlocation WHERE Customer_ID = %s", (customer_id,))
    location_result = cursor.fetchall()

    cursor.execute("SELECT * FROM customer_contact WHERE Customer_ID = %s", (customer_id,))
    contact_result = cursor.fetchall()

    cursor.execute("SELECT * FROM system_instillation WHERE Customer_ID = %s", (customer_id,))
    system_result = cursor.fetchall()


    cursor.close()
    connection.close()
    



def build_customer_dropdown():
    selector = tkinter.Toplevel()
    selector.title("Customer Selector")
    selector.geometry("400x200")

    customers = get_customers()

    tkinter.Label(selector, text="Select Customer:", font=("Arial", 12)).pack()

    customer_var = tkinter.StringVar()

    dropdown = ttk.Combobox(
        selector,
        textvariable=customer_var,
        values=customers,
        state="readonly",
        width=30
    )
    dropdown.pack(pady=10)

    if customers:
        dropdown.current(0)

    def confirm_selection():
        global customer_name, selected_customer_id
        customer_name = customer_var.get()
        selected_customer_id = None
        if not customer_name:
            return
        print("Selected customer:", customer_name)
        get_customer_details()
        selector.destroy()

    tkinter.Button(selector, text="Confirm", command=confirm_selection).pack()

    return selector  
