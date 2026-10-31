from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from openpyxl import Workbook
from database_connection import create_connection


def get_first_customers(amount):
    # Reject negative or non-integer limits before passing them to the query.
    if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:
        raise ValueError("Customer amount must be a non-negative whole number.")

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT c.Customer_ID AS id, c.customer_name AS name, "
            "MAX(l.Address) AS address, MAX(ct.Email) AS email "
            "FROM customer c "
            "LEFT JOIN customerlocation l ON l.Customer_ID = c.Customer_ID "
            "LEFT JOIN customer_contact ct ON ct.Customer_ID = c.Customer_ID "
            "GROUP BY c.Customer_ID, c.customer_name "
            "ORDER BY c.Customer_ID LIMIT %s",
            (amount,),
        )
        return cursor.fetchall()
    finally:
        # Always release the resources used for this export query.
        cursor.close()
        connection.close()


def customer_amount_for_spreadsheet(parent=None):
    # Use a child window when called from the app; otherwise provide a root window.
    popup = tk.Toplevel(parent) if parent is not None else tk.Tk()
    popup.title("Export Customers")
    popup.geometry("420x420")
    popup.resizable(False, False)

    # The amount controls how many customer choices must be collected.
    tk.Label(popup, text="Number of customers to export:").pack(pady=(18, 6))
    amount_value = tk.StringVar()
    entry = tk.Entry(popup, textvariable=amount_value, font=("Arial", 14))
    entry.pack(pady=5)
    entry.focus_set()

    def confirm():
        try:
            amount = int(amount_value.get().strip())
            if amount < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid input",
                "Enter a non-negative whole number.",
                parent=popup,
            )
            return

        try:
            # Fetch available customer names and IDs before showing the picker.
            customers = get_first_customers(1_000_000)
        except Exception as error:
            messagebox.showerror("Export failed", str(error), parent=popup)
            return

        # Do not ask the user to select more records than actually exist.
        if amount > len(customers):
            messagebox.showerror(
                "Not enough customers",
                f"There are only {len(customers)} customers available.",
                parent=popup,
            )
            return

        # Replace the amount prompt with the requested number of customer pickers.
        for child in popup.winfo_children():
            child.destroy()
        popup.title("Select Customers")
        tk.Label(
            popup,
            text=f"Select {amount} customer(s). Each customer can be selected once.",
            wraplength=380,
        ).pack(pady=12)

        selected_customers = []
        customer_labels = [f"{row['name']} (ID {row['id']})" for row in customers]

        # Provide a dropdown for one customer at a time until the count is met.
        choice = tk.StringVar()
        picker = ttk.Combobox(
            popup,
            textvariable=choice,
            values=customer_labels,
            state="readonly",
            width=48,
        )
        picker.pack(padx=12, pady=(12, 4))
        if customer_labels:
            picker.current(0)
        #creates the different rows for the customers to be added
        selected_rows = []
        selected_ids = set()
        selected_names = tk.Listbox(popup, height=12, width=52)
        selected_names.pack(padx=12, pady=8, fill="both", expand=True)
        progress = tk.Label(popup, text=f"Selected 0 of {amount}")
        progress.pack(pady=4)

        def add_customer():
            index = picker.current()
            if index < 0:
                messagebox.showerror("Select a customer", "Choose a customer first.", parent=popup)
                return
            customer = customers[index]
            if customer["id"] in selected_ids:  #makes sure the user cannot select the same customer twice 
                messagebox.showinfo(
                    "Already selected", "Choose a different customer.", parent=popup 
                )
                return
            selected_rows.append(customer)
            selected_ids.add(customer["id"])
            selected_names.insert(tk.END, customer_labels[index])
            progress.config(text=f"Selected {len(selected_rows)} of {amount}")

            # Disable further customer additions once the requested amount is met.
            if len(selected_rows) >= amount:
                add_button.config(state="disabled")

        def export_selected():#exports the selected details once the amount of customers that is needed have been selected
            if len(selected_rows) != amount:
                messagebox.showerror(
                    "Select customers",
                    f"Add exactly {amount} customers before exporting.",
                    parent=popup,
                )
                return

            # Preserve the customer's dropdown selection order in the workbook.
            selected_customers[:] = selected_rows
            destination = filedialog.asksaveasfilename(
                parent=popup,
                title="Save customer spreadsheet",
                defaultextension=".xlsx",
                filetypes=[("Excel workbook", "*.xlsx")],
                initialfile="customer_export.xlsx",
            )
            try:
                saved_path = write_spreadsheet(
                    amount, output_path=destination, customers=selected_customers
                )
            except Exception as error:
                messagebox.showerror("Export failed", str(error), parent=popup)
                return

            messagebox.showinfo(
                "Export complete", f"Spreadsheet saved to:\n{saved_path}", parent=popup
            )
            popup.destroy()

        selected_customers = []
        add_button = tk.Button(popup, text="Add customer", command=add_customer)
        add_button.pack(pady=6)
        tk.Button(popup, text="Export selected customers", command=export_selected).pack(pady=8)

    # Button and Enter key both trigger the same validated export action.
    tk.Button(popup, text="Choose file and export", command=confirm).pack(pady=12)
    entry.bind("<Return>", lambda _event: confirm())
    return popup


def write_spreadsheet(amount, output_path=None, customers=None):
    """Write customer records to an Excel file and return its destination."""
    # Pull actual customer records instead of relying on an undefined helper.
    # Fetch rows.
    if customers is None:
        customers = get_first_customers(amount)
    if len(customers) != amount:
        raise ValueError(f"Expected {amount} selected customers, got {len(customers)}.")

    # Create a workbook
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Customers"
    worksheet.append(["Customer ID", "Name", "Address", "Email"])

    # Add one row per customer and preserve blank optional fields as empty cells.
    for customer in customers:
        worksheet.append(
            [
                customer.get("id"),
                customer.get("name"),
                customer.get("address"),
                customer.get("email"),
            ]
        )

    # Widen columns so stuff is readable when opened
    for column_cells in worksheet.columns:
        longest = max(len(str(cell.value or "")) for cell in column_cells)
        worksheet.column_dimensions[column_cells[0].column_letter].width = min(
            max(longest + 2, 12), 50
        )

    # Save in the project folder
    destination = Path(output_path) if output_path else Path(__file__).with_name(
        "customer_export.xlsx"
    )
    workbook.save(destination)
    return destination
