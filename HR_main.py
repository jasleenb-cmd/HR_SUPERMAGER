import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

employee_data_file = "employee_data.csv"
employee_data = []
event_data_file = "event_data.csv"
scheduled_events = []
schedule_data_file = "schedule_data.csv"
employee_schedules = []
employee_code = []


def read_employee_data():
    if os.path.exists(employee_data_file):
        with open(employee_data_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                employee_data.append(row)


def write_employee_data():
    with open(employee_data_file, "w", newline='') as f:
        writer = csv.writer(f)
        for row in employee_data:
            writer.writerow(row)


def read_schedule_data():
    if os.path.exists(schedule_data_file):
        with open(schedule_data_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                employee_schedules.append(row)


def write_schedule_data():
    with open(schedule_data_file, "w", newline='') as f:
        writer = csv.writer(f)
        for row in employee_schedules:
            writer.writerow(row)


read_schedule_data()


def add_employee():
    global entry_employee_id, entry_employee_name, combobox_employee_type, entry_employee_salary, employee_list, employee_code
    employee_id = entry_employee_id.get()
    employee_name = entry_employee_name.get()
    employee_type = combobox_employee_type.get()
    employee_salary = entry_employee_salary.get()

    if employee_id and employee_name and employee_type and employee_salary:
        if len(employee_id) == 3 and employee_id.isdigit():
            for employee in employee_data:
                if employee[0] == employee_id:
                    messagebox.showerror("Error",
                                         "Employee with this ID already exists.")
                    return

            employee_data.append(
                (employee_id, employee_name, employee_type, employee_salary))
            update_employee_list()
            write_employee_data()
            entry_employee_id.delete(0, 'end')
            entry_employee_name.delete(0, 'end')
            entry_employee_salary.delete(0, 'end')
            update_employee_id_combobox()  # Add this line

        else:
            messagebox.showwarning("Invalid ID",
                                   "Please enter a unique 3-digit ID.")
    else:
        messagebox.showwarning("Missing Information",
                               "Please enter all required fields.")


def delete_employee():
    global employee_data, payroll_tree, employee_code
    selected_employee_index = payroll_tree.focus()
    selected_employee_index = selected_employee_index[3:4]
    selected_employee_index = int(selected_employee_index)

    if selected_employee_index:
        new_list = []
        new_code = []
        count = 1
        for row in employee_data:
            if count != selected_employee_index:
                new_list.append(row)
                new_code.append(row[0])
            else:
                selected_item = payroll_tree.selection()[0]
                payroll_tree.delete(selected_item)
            count += 1
        employee_data = new_list
        employee_code = new_code
        update_employee_list()
        write_employee_data()
        update_employee_id_combobox()
    else:
        messagebox.showwarning("No Selection",
                               "Please select an employee to delete.")


def update_employee_list():
    global payroll_tree, employee_code, employee_data
    for employee in employee_data:
        if employee[0] not in employee_code:
            employee_code.append(employee[0])
            payroll_tree.insert("", "end", values=(
            employee[0], employee[1], employee[2], employee[3], ""))


def update_employee_id_combobox():
    global combobox_employee_id
    combobox_employee_id["values"] = [emp[0] for emp in employee_data]


read_employee_data()


def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "hr_manager" and password == "utmcct211":
        messagebox.showinfo("Login Success", "Welcome to the HR Application!")
        root.destroy()
        create_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def add_schedule():
    global combobox_employee_id, combobox_event_name, entry_event_date, employee_data
    employee_id = combobox_employee_id.get()
    event_name = combobox_event_name.get()
    event_date = entry_event_date.get()

    if employee_id and event_name and event_date:
        for i, employee in enumerate(employee_data):
            if employee[0] == employee_id:
                employee_data[i].extend([event_name, event_date])
                write_employee_data()
                messagebox.showinfo("Success", "Schedule added successfully.")
                return
        messagebox.showerror("Error", "Employee not found.")
    else:
        messagebox.showwarning("Missing Information",
                               "Please enter all required fields.")


def add_event():
    global entry_event_name, entry_event_date, entry_event_time, event_list
    event_name = entry_event_name.get()
    event_date = entry_event_date.get()
    event_time = entry_event_time.get()

    if event_name and event_date and event_time:
        scheduled_events.append((event_name, event_date, event_time))
        update_event_list()
        write_event_data()
        entry_event_name.delete(0, 'end')
        entry_event_date.delete(0, 'end')
        entry_event_time.delete(0, 'end')
    else:
        messagebox.showwarning("Missing Information",
                               "Please enter all required fields.")


def update_event_list():
    global event_list
    event_list.delete(0, 'end')
    for event in scheduled_events:
        event_list.insert('end', f"{event[0]} - {event[1]} - {event[2]}")


def delete_event():
    global event_list, scheduled_events
    selected_event_index = event_list.curselection()

    if selected_event_index:
        scheduled_events.pop(selected_event_index[0])
        update_event_list()
        write_event_data()
    else:
        messagebox.showwarning("No Selection",
                               "Please select an event to delete.")


def update_schedule_list():
    global schedule_list
    schedule_list.delete(0, 'end')
    for schedule in employee_schedules:
        schedule_list.insert('end',
                             f"{schedule[0]} - {schedule[1]} - {schedule[2]} - {schedule[3]}")


def read_event_data():
    if os.path.exists(event_data_file):
        with open(event_data_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                scheduled_events.append(row)


read_event_data()


def write_event_data():
    with open(event_data_file, "w", newline='') as f:
        writer = csv.writer(f)
        for row in scheduled_events:
            writer.writerow(row)


def on_tab_changed(event):
    selected_tab = event.widget.tab(event.widget.select(), "text")
    if selected_tab == "Schedule":
        update_employee_id_combobox()
        # update_schedule_tree()  # Add this line


def update_schedule(employee_id, day_vars):
    if employee_id:
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                        "Saturday", "Sunday"]

        # Create a schedule string
        schedule = ','.join([day for idx, day in enumerate(days_of_week) if
                             day_vars[idx].get()])

        # Find the employee in employee_schedules and update their schedule
        for row in employee_schedules:
            if row[0] == employee_id:
                row[1] = schedule
                break
        else:
            employee_schedules.append([employee_id, schedule])

        write_schedule_data()
        messagebox.showinfo("Success", "Schedule updated successfully.")
        update_schedule_tree()  # Add this line here
    else:
        messagebox.showwarning("Missing Information",
                               "Please select an employee.")


def update_schedule_tree():
    global schedule_tree, employee_data, employee_schedules
    schedule_tree.delete(*schedule_tree.get_children())  # clear the tree
    for employee in employee_data:
        employee_id = employee[0]
        employee_name = employee[1]
        schedule = ''
        for row in employee_schedules:
            if row[0] == employee_id:
                schedule = row[1]
                break
        schedule_tree.insert("", "end", values=(employee_id, employee_name, schedule))
    write_schedule_data()


def create_dashboard():
    global entry_employee_id, entry_employee_name, combobox_employee_type, entry_employee_salary, employee_list, entry_event_name, entry_event_date, entry_event_time, event_list, combobox_employee_id, schedule_list, payroll_tree, schedule_tree

    dashboard = tk.Tk()
    dashboard.title("HR Dashboard")

    notebook = ttk.Notebook(dashboard)
    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    # Payroll tab
    payroll_frame = ttk.Frame(notebook)
    notebook.add(payroll_frame, text="Payroll")

    ttk.Label(payroll_frame, text="Employee ID (3 digits):").grid(row=0,
                                                                  column=0,
                                                                  sticky="e")
    entry_employee_id = tk.Entry(payroll_frame)
    entry_employee_id.grid(row=0, column=1)

    ttk.Label(payroll_frame, text="Employee Name:").grid(row=1, column=0,
                                                         sticky="e")
    entry_employee_name = tk.Entry(payroll_frame)
    entry_employee_name.grid(row=1, column=1)

    ttk.Label(payroll_frame, text="Employee Type:").grid(row=2, column=0,
                                                         sticky="e")
    combobox_employee_type = ttk.Combobox(payroll_frame,
                                          values=["Part-time", "Contract",
                                                  "Salary"], state="readonly")
    combobox_employee_type.grid(row=2, column=1)
    combobox_employee_type.current(0)

    ttk.Label(payroll_frame, text="Employee Salary:").grid(row=3, column=0,
                                                           sticky="e")
    entry_employee_salary = tk.Entry(payroll_frame)
    entry_employee_salary.grid(row=3, column=1)

    button_add_employee = tk.Button(payroll_frame, text="Add Employee",
                                    command=add_employee)
    button_add_employee.grid(row=4, column=0, columnspan=2, pady=10)

    button_delete_employee = tk.Button(payroll_frame, text="Delete Employee",
                                       command=delete_employee)
    button_delete_employee.grid(row=5, column=0, columnspan=2, pady=10)

    payroll_tree = ttk.Treeview(payroll_frame, columns=(
        "eid", "employee_name", "contract_type", "unit_pay"), show="headings",
                                height=15)

    payroll_tree.column('#0', minwidth=0,
                        width=0)  # remove this line will have a big blank first column
    payroll_tree.column('#1', minwidth=0, width=50)
    payroll_tree.column('#2', minwidth=0, width=200)
    payroll_tree.column('#3', minwidth=0, width=100)
    payroll_tree.column('#4', minwidth=0, width=100)

    payroll_tree.heading('eid', text="EID")
    payroll_tree.heading('employee_name', text="Employee Name")
    payroll_tree.heading('contract_type', text="Contract Type")
    payroll_tree.heading('unit_pay', text="Unit Pay")

    payroll_tree.grid(row=6, column=0, columnspan=2, pady=10)

    update_employee_list()

    # Training tab
    scheduling_frame = ttk.Frame(notebook)
    notebook.add(scheduling_frame, text="Training")
    button_delete_event = tk.Button(scheduling_frame, text="Delete Event",
                                    command=delete_event)
    button_delete_event.grid(row=5, column=0, columnspan=2, pady=10)

    ttk.Label(scheduling_frame, text="Training:").grid(row=0, column=0,
                                                       sticky="e")
    entry_event_name = tk.Entry(scheduling_frame)
    entry_event_name.grid(row=0, column=1)

    ttk.Label(scheduling_frame, text="Training Date (YYYY-MM-DD):").grid(row=1,
                                                                         column=0,
                                                                         sticky="e")
    entry_event_date = tk.Entry(scheduling_frame)
    entry_event_date.grid(row=1, column=1)

    ttk.Label(scheduling_frame, text="Employee ID (3 digits)").grid(row=2,
                                                                    column=0,
                                                                    sticky="e")
    entry_event_time = tk.Entry(scheduling_frame)
    entry_event_time.grid(row=2, column=1)

    button_add_event = tk.Button(scheduling_frame, text="Add Event",
                                 command=add_event)
    button_add_event.grid(row=3, column=0, columnspan=2, pady=10)

    event_list = tk.Listbox(scheduling_frame, height=10, width=50)
    event_list.grid(row=4, column=0, columnspan=2)
    update_event_list()

    # Schedule tab
    training_frame = ttk.Frame(notebook)
    notebook.add(training_frame, text="Schedule")

    ttk.Label(training_frame, text="Employee ID:").grid(row=0, column=0,
                                                        sticky="e")
    combobox_employee_id = ttk.Combobox(training_frame, state="readonly")
    combobox_employee_id.grid(row=0, column=1)

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                    "Saturday", "Sunday"]
    day_vars = []
    for idx, day in enumerate(days_of_week):
        day_var = tk.BooleanVar()
        day_checkbox = tk.Checkbutton(training_frame, text=day,
                                      variable=day_var)
        day_checkbox.grid(row=1, column=idx)
        day_vars.append(day_var)

    button_update_schedule = tk.Button(training_frame, text="Update Schedule",
                                       command=lambda: update_schedule(
                                           combobox_employee_id.get(),
                                           day_vars))
    button_update_schedule.grid(row=2, column=0, columnspan=7, pady=10)
    schedule_tree = ttk.Treeview(training_frame,
                                 columns=("eid", "employee_name", "schedule"),
                                 show="headings", height=15)
    schedule_tree.column('#0', minwidth=0, width=0)
    schedule_tree.column('#1', minwidth=0, width=50)
    schedule_tree.column('#2', minwidth=0, width=200)
    schedule_tree.column('#3', minwidth=0, width=400)

    schedule_tree.heading('eid', text="EID")
    schedule_tree.heading('employee_name', text="Employee Name")
    schedule_tree.heading('schedule', text="Schedule")

    schedule_tree.grid(row=3, column=0, columnspan=7, pady=10)

    notebook.pack(expand=True, fill="both")
    dashboard.mainloop()


root = tk.Tk()
root.title("HR Application Login")

tk.Label(root, text="Username:").grid(row=0, column=0, sticky="e")
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1)

tk.Label(root, text="Password:").grid(row=1, column=0, sticky="e")
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1)

button_login = tk.Button(root, text="Login", command=login)
button_login.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
