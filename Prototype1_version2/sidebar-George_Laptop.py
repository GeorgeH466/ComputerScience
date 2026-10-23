import tkinter
import time
import data_viewer
import calendar_creator

customer_result = None
location_result = None
contact_result = None
system_result = None
customer_name = None


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


def do_get_data_for_data_view():#runs the customer dropdown for the data viewer
    dropdown_window = data_viewer.build_customer_dropdown()
    root.wait_window(dropdown_window)
    data_viewer_creator()

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

def create_data_entry():
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
    global root, sidebar, topbar, schedule_button, invoice_button, spreadsheet_button, data_entry_button, data_viewer_button, exit_button

    root = tkinter.Tk()#makes the base screen
    root.title("Variable Monitor with Sidebar")
    root.geometry("4250x1000")

    # Sidebar
    sidebar = tkinter.Frame(root, bg="#222", width=300)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    #organises and populates the sidebar
    schedule_button = tkinter.Button(sidebar, text="schedule", font=("Arial", 20), command= open_the_calendar_window())
    schedule_button.pack(pady=30, fill="x")

    invoice_button = tkinter.Button(sidebar, text="invoice", font=("Arial", 20))
    invoice_button.pack(pady=30, fill="x")

    spreadsheet_button = tkinter.Button(sidebar, text="spreadsheet", font=("Arial", 20))
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

    topbar.grid_columnconfigure(0, weight=1)

    bell_button = tkinter.Button( topbar, text="🔔", font=("Arial", 20))
    bell_button.grid(row=0, column=0, padx=1500, pady=20, sticky="nw")

    home_view_builder()
    update_clock()
    root.mainloop()
create_sidebar()
