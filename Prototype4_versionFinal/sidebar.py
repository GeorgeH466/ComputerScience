import tkinter
import time
import data_viewer
from calendar_creator import open_the_calendar_window
import spreadsheet
from notifications import scan_for_notifications
from datetime import datetime


#makes it so that the results variables exist before anything is done to make them able to be used but are all null.
customer_result = None
location_result = None
contact_result = None
system_result = None
customer_name = None

#it creates the main home area that opens when the home screen first opens
def home_view_builder():
    clear_right_side()#clears the main before opening home

    global clock_label, main_frame1#makes needed variables available everywhere
    main_frame1 = tkinter.Frame(root, bg="#555")
    main_frame1.pack(side="right", fill="both", expand=True)

    main_frame1.columnconfigure(0, weight=1)
    main_frame1.rowconfigure(0, weight=1)

    invoice_label = tkinter.Label(main_frame1, text="invoice section", bg="#777", font=("Arial", 20))
    invoice_label.grid(row=0, column=0, padx=40, pady=40, sticky="nw")

    clock_label = tkinter.Label(main_frame1, font=("Arial", 25), bg="#111", fg="white")
    clock_label.grid(row=1, column=0, sticky="nw")


def update_clock():#makes the clock update every second to be a live 24 hour format clock
    try:
        if clock_label and clock_label.winfo_exists():#only trys to update if the clock is actually open on the current tab
            current_time = time.strftime("%H:%M:%S")
            clock_label.config(text=current_time)
        root.after(1000, update_clock)#updates clock every second (1000 ms)
    except:#makes it so the code doesnt stop if the clock fails
        pass

def notification_check():
    global notifications
    notifications = scan_for_notifications()
    update_bell()
    root.after(10000, notification_check)  # every 10 seconds

    
def update_bell():
    unread = sum(1 for n in notifications if not n["is_read"])  #only shows notifications that have not been read

    if unread > 0:
        bell_button.config(text=f"🔔 {unread}", fg="yellow")  #changes the colour of the bell if there is unread notifications
    else:
        bell_button.config(text="🔔", fg="white")




def do_get_data_for_data_view():#runs the customer dropdown for the data viewer
    dropdown_window = data_viewer.build_customer_dropdown()
    root.wait_window(dropdown_window)
    data_viewer_creator()

def do_get_data_for_invoice():#runs the customer dropdown for the data viewer
    dropdown_window = data_viewer.build_customer_dropdown()
    root.wait_window(dropdown_window)
    customer_id = getattr(data_viewer, "selected_customer_id", None)
    if customer_id is None:
        return

    # Generate the invoice for the ID selected in the shared customer picker.
    from Invoice_generation import generate_invoice
    from tkinter import messagebox
    try:
        invoice_path = generate_invoice(customer_id)
    except Exception as error:
        messagebox.showerror("Invoice generation failed", str(error), parent=root)
        return
    messagebox.showinfo(
        "Invoice generated", f"Invoice saved to:\n{invoice_path}", parent=root
    )

def clear_right_side():#clears the main area so that the next menu can be opened but keeps the sidebar and topbar there
    safe_sidebar = globals().get("sidebar")
    safe_topbar = globals().get("topbar")

    for widget in root.winfo_children():
        if isinstance(widget, tkinter.Frame) and widget not in (safe_sidebar, safe_topbar):
            widget.destroy()

def data_viewer_creator():#opens the data viewer sections
    clear_right_side()

    global main_frame2
    main_frame2 = tkinter.Frame(root, bg="#343434")
    main_frame2.pack(side="right", fill="both", expand=True)

    main_frame2.columnconfigure(0, weight=1)
    main_frame2.columnconfigure(1, weight=1)
    main_frame2.rowconfigure(0, weight=1)
    main_frame2.rowconfigure(1, weight=1)
#all of the next bit shows how the boxes are separate and the sections each have their own thing
    customer_section = tkinter.LabelFrame(main_frame2,  text="Customer Details",  bg="#343434",  fg="white",  font=("Arial", 16))
    customer_section.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    tkinter.Label(customer_section, text="\n".join([str(row) for row in data_viewer.customer_result]), bg="#343434", fg="white", font=("Arial", 12), justify="left", wraplength=400).pack(anchor="w", padx=10, pady=10)

    location_section = tkinter.LabelFrame( main_frame2,  text="Location Details",  bg="#343434",  fg="white",  font=("Arial", 16))
    location_section.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    tkinter.Label( location_section, text="\n".join([str(row) for row in data_viewer.location_result]), bg="#343434", fg="white", font=("Arial", 12), justify="left", wraplength=400).pack(anchor="w", padx=10, pady=10)


    contact_section = tkinter.LabelFrame( main_frame2,  text="Contact Details",  bg="#343434",  fg="white",  font=("Arial", 16))
    contact_section.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    tkinter.Label( contact_section, text="\n".join([str(row) for row in data_viewer.contact_result]), bg="#343434", fg="white", font=("Arial", 12), justify="left", wraplength=400).pack(anchor="w", padx=10, pady=10)

  
    system_section = tkinter.LabelFrame( main_frame2,  text="System Installation",  bg="#343434",  fg="white",  font=("Arial", 16))
    system_section.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    tkinter.Label( system_section, text="\n".join([str(row) for row in data_viewer.system_result]), bg="#343434", fg="white", font=("Arial", 12), justify="left", wraplength=400).pack(anchor="w", padx=10, pady=10)

def open_schedule():
    # Open the existing calendar
    open_the_calendar_window()

    # Create a window for adding an event
    add_window = tkinter.Toplevel(root)
    add_window.title("Add Schedule Event")
    add_window.geometry("400x520")
    add_window.resizable(False, False)

    # Title
    tkinter.Label(add_window,text="Add New Event",font=("Arial", 20, "bold")).pack(pady=20)

    # Customer ID
    tkinter.Label(add_window,text="Customer ID:",font=("Arial", 14)).pack(pady=(10, 5))

    customer_entry = tkinter.Entry(add_window,font=("Arial", 14))
    customer_entry.pack()

    # Date
    tkinter.Label(add_window,text="Date (YYYY-MM-DD):",font=("Arial", 14)).pack(pady=(10, 5))

    date_entry = tkinter.Entry(add_window,font=("Arial", 14))
    date_entry.pack()

    # Time
    tkinter.Label(add_window,text="Time (HH:MM:SS):",font=("Arial", 14)).pack(pady=(10, 5))

    time_entry = tkinter.Entry(add_window,font=("Arial", 14))
    time_entry.pack()

    # Event type
    tkinter.Label(add_window,text="Event Type:", font=("Arial", 14)).pack(pady=(10, 5))

    type_entry = tkinter.Entry(add_window, font=("Arial", 14))
    type_entry.pack()

    # Result message
    result_label = tkinter.Label(add_window, text="", font=("Arial", 12))
    result_label.pack(pady=10)

    def save_schedule_event():
        from scheduling_algorithm import add_event
        try:
            customer = int(customer_entry.get())

            event_date = datetime.strptime(date_entry.get(),"%Y-%m-%d").date()

            event_time = datetime.strptime(time_entry.get(),"%H:%M:%S").time()

            event_type = type_entry.get()

            new_event = {
                "customer": customer,
                "date": event_date,
                "time": event_time,
                "type": event_type}

            result = add_event(new_event)

            if result["status"] == "saved":
                result_label.config(
                    text="Event successfully added!", fg="green")

            elif result["status"] == "clash":
                clashing_event = result["clashing_event"]

                result_label.config(
                    text=("CLASH!\n" f"Existing event: {clashing_event['Event_type']}\n" f"Date: {clashing_event['Event_Date']}\n" f"Time: {clashing_event['Event_Time']}"),fg="red")

        except ValueError:
            result_label.config(text="Please check your date, time and customer ID.", fg="red")

    # Save button
    tkinter.Button(add_window, text="Add Event", font=("Arial", 14), command=save_schedule_event).pack(pady=10)


def open_notification_center():
    win = tkinter.Toplevel(root)
    win.title("Notifications")
    win.geometry("400x400")

    # Offer an explicit send action so urgent emails are never sent repeatedly
    # by the background notification refresh loop.
    from tkinter import messagebox

    def send_urgent_emails():
        """Send pending urgent event notifications when SMTP is configured."""
        from Email_notifications import check_email_notifications
        try:
            result = check_email_notifications(True)
        except Exception as error:
            messagebox.showerror("Email notifications", str(error), parent=win)
            return
        messagebox.showinfo(
            "Email notifications",
            f"Sent: {result['sent']}\nFailed: {result['failed']}",
            parent=win,
        )

    tkinter.Button(
        win, text="Send urgent event emails", command=send_urgent_emails
    ).pack(fill="x", pady=8)

    for n in notifications:
        btn = tkinter.Button(
            win,
            text=n["message"],
            font=("Arial", 14),
            command=lambda notif=n: open_notification(notif)
        )
        btn.pack(fill="x", pady=5)


def open_notification(notification):
    notification["is_read"] = True

    if notification["type"] == "invoice":
        do_get_data_for_invoice()

    elif notification["type"] == "event":
        open_the_calendar_window()

    elif notification["type"] == "payment":
        do_get_data_for_data_view()

    update_bell()




def create_data_entry():
    # Open the complete entry form implemented in the dedicated module.
    from Data_Entry import open_data_entry
    open_data_entry(root)
    return

    clear_right_side()

    global main_frame2
    main_frame2 = tkinter.Frame(root, bg="#343434")
    main_frame2.pack(side="right", fill="both", expand=True)

    main_frame2.columnconfigure(0, weight=1)
    main_frame2.columnconfigure(1, weight=1)
    main_frame2.rowconfigure(0, weight=1)
    main_frame2.rowconfigure(1, weight=1)
#all of the next bit shows how the boxes are separate and the sections each have their own thing
    customer_section = tkinter.LabelFrame(main_frame2,  text="Customer Details",  bg="#343434",  fg="white",  font=("Arial", 16))
    customer_section.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

    tkinter.Label(customer_section, bg="#343434", fg="white", font=("Arial", 12), wraplength=40).pack(anchor="w", padx=10, pady=10)

    location_section = tkinter.LabelFrame( main_frame2,  text="Location Details",  bg="#343434",  fg="white",  font=("Arial", 16))
    location_section.grid(row=0, column=1, padx=20, pady=20, sticky="nw")

    tkinter.Label( location_section, bg="#343434", fg="white", font=("Arial", 12), wraplength=40).pack(anchor="w", padx=10, pady=10)


    contact_section = tkinter.LabelFrame( main_frame2,  text="Contact Details",  bg="#343434",  fg="white",  font=("Arial", 16))
    contact_section.grid(row=1, column=0, padx=20, pady=20, sticky="nw")

    tkinter.Label( contact_section, bg="#343434", fg="white", font=("Arial", 12), wraplength=40).pack(anchor="w", padx=10, pady=10)

  
    system_section = tkinter.LabelFrame( main_frame2,  text="System Installation",  bg="#343434",  fg="white",  font=("Arial", 16))
    system_section.grid(row=1, column=1, padx=20, pady=20, sticky="nw")

    tkinter.Label( system_section, bg="#343434", fg="white", font=("Arial", 12), wraplength=40).pack(anchor="w", padx=10, pady=10)



def create_sidebar():
    global root, sidebar, bell_button, topbar, schedule_button, invoice_button, spreadsheet_button, data_entry_button, data_viewer_button, exit_button

    root = tkinter.Tk()#makes the base screen
    root.title("Variable Monitor with Sidebar")
    root.geometry("4250x1000")

    # Sidebar
    sidebar = tkinter.Frame(root, bg="#222", width=300)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    #organises and populates the sidebar
    schedule_button = tkinter.Button(sidebar, text="schedule", font=("Arial", 20), command = open_schedule)
    schedule_button.pack(pady=30, fill="x")

    invoice_button = tkinter.Button(sidebar, text="invoice", font=("Arial", 20), command = do_get_data_for_invoice)
    invoice_button.pack(pady=30, fill="x")

    spreadsheet_button = tkinter.Button(sidebar, text="spreadsheet", font=("Arial", 20), command=lambda: spreadsheet.customer_amount_for_spreadsheet(root))
    spreadsheet_button.pack(pady=30, fill="x")

    data_entry_button = tkinter.Button(sidebar, text="data entry", font=("Arial", 20), command= create_data_entry)
    data_entry_button.pack(pady=30, fill="x")

    data_viewer_button = tkinter.Button(sidebar, text="data viewer", font=("Arial", 20), command=do_get_data_for_data_view)
    data_viewer_button.pack(pady=30, fill="x")

    home_button = tkinter.Button(sidebar, text="home", font=("Arial", 20), command=home_view_builder)
    home_button.pack(pady=30, fill="x")

    exit_button = tkinter.Button(sidebar, text="Exit", font=("Arial", 20), command=root.quit)
    exit_button.pack(pady=100, fill="x")

    # Top bar
    topbar = tkinter.Frame(root, bg="#534", height=20)
    topbar.pack(side="top", fill="x")

    topbar.grid_columnconfigure(0, weight=1)  # <-- NEW: makes grid behave

    bell_button = tkinter.Button( topbar, text="🔔", font=("Arial", 20), command= open_notification_center)
    bell_button.grid(row=0, column=0, padx=450, pady=20, sticky="nw")

    home_view_builder()
    notification_check()
    update_clock()
    root.mainloop()
