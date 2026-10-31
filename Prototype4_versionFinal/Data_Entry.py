"""Customer data entry form backed by the project's existing MySQL tables."""

import tkinter as tk
from tkinter import messagebox

from database_connection import create_connection


def save_customer(customer, location, contact, installation):
    """Save one customer and its related records in a single transaction.

    The four dictionaries use the field names collected by the form below. A
    transaction keeps the related tables consistent if any insert fails.
    """
    connection = create_connection()
    if connection is None:
        raise RuntimeError("Could not connect to the project database.")

    cursor = connection.cursor()
    try:
        # Insert the primary customer record first so MySQL can assign its ID.
        cursor.execute(
            "INSERT INTO customer (customer_name) VALUES (%s)",
            (customer["name"],),
        )
        customer_id = cursor.lastrowid

        # Store the customer's address in the existing location table.
        cursor.execute(
            "INSERT INTO customerlocation (Customer_ID, Address) VALUES (%s, %s)",
            (customer_id, location["address"]),
        )

        # Store contact details separately, matching the data viewer schema.
        cursor.execute(
            "INSERT INTO customer_contact (Customer_ID, Email) VALUES (%s, %s)",
            (customer_id, contact["email"]),
        )

        # Add installation data only when the user supplied at least one value.
        if installation["details"]:
            cursor.execute(
                "INSERT INTO system_instillation (Customer_ID, Installation_Details) "
                "VALUES (%s, %s)",
                (customer_id, installation["details"]),
            )

        # Commit all related rows together and return the new database ID.
        connection.commit()
        return customer_id
    except Exception:
        # Roll back partial inserts so the customer is never half-created.
        connection.rollback()
        raise
    finally:
        # Always release database resources, including on an insertion error.
        cursor.close()
        connection.close()


def open_data_entry(parent=None):
    """Show a form for entering a customer and their related information."""
    window = tk.Toplevel(parent) if parent is not None else tk.Tk()
    window.title("Customer Data Entry")
    window.geometry("520x480")
    window.resizable(False, False)

    # Keep the form fields together so validation and persistence stay clear.
    fields = {}
    field_specs = [
        ("Customer name", "name"),
        ("Address", "address"),
        ("Email", "email"),
        ("Installation details (optional)", "installation"),
    ]

    # Create a label and editable input for every customer detail.
    for row, (label_text, key) in enumerate(field_specs):
        tk.Label(window, text=label_text, anchor="w").grid(
            row=row, column=0, padx=16, pady=10, sticky="w"
        )
        entry = tk.Entry(window, width=42)
        entry.grid(row=row, column=1, padx=16, pady=10, sticky="ew")
        fields[key] = entry

    # This label reports success or input/database errors to the user.
    status = tk.Label(window, text="", wraplength=460, justify="left")
    status.grid(row=len(field_specs), column=0, columnspan=2, padx=16, pady=10)

    def submit():
        """Validate the form and save the customer when all required values exist."""
        values = {key: widget.get().strip() for key, widget in fields.items()}

        # A customer name and a delivery/service address are required fields.
        if not values["name"] or not values["address"]:
            messagebox.showerror(
                "Missing information",
                "Enter at least a customer name and address.",
                parent=window,
            )
            return

        try:
            # Save the primary customer and its associated records atomically.
            customer_id = save_customer(
                {"name": values["name"]},
                {"address": values["address"]},
                {"email": values["email"]},
                {"details": values["installation"]},
            )
        except Exception as error:
            # Keep the form open so the user can correct data or retry.
            status.config(text=f"Could not save customer: {error}", fg="red")
            return

        # Confirm the assigned ID and clear the form for a possible next entry.
        status.config(text=f"Customer saved successfully (ID {customer_id}).", fg="green")
        for widget in fields.values():
            widget.delete(0, tk.END)

    # The submit button is the single entry point for validated persistence.
    tk.Button(window, text="Save Customer", command=submit).grid(
        row=len(field_specs) + 1, column=0, columnspan=2, pady=16
    )
    window.columnconfigure(1, weight=1)
    return window
