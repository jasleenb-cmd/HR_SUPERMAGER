import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd

scheduled_events = []
schedule_list = []
pre_payroll_list = []

def login():
    global entry_username, entry_password
    username = entry_username.get()
    password = entry_password.get()

    if username == "hr" and password == "17":
        messagebox.showinfo("Login Success", "Welcome to the HR Application!")
        root.destroy() #destroy the login window
        create_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def add_event():
    '''
    this defines the functionality of the memo tab
    '''
    global entry_event_name, entry_event_date, entry_event_time, event_list
    event_name = entry_event_name.get() #get emtry for memo
    event_date = entry_event_date.get()
    event_time = entry_event_time.get()

    if event_name and event_date and event_time: #if enter all fields
        scheduled_events.append((event_name, event_date, event_time)) #add the event record to the main list
        update_event_list()
        entry_event_name.delete(0, 'end') #clear the respective list, allow new addition
        entry_event_date.delete(0, 'end') #clear the respective list, allow new addition
        entry_event_time.delete(0, 'end') #clear the respective list, allow new addition
    else:
        messagebox.showwarning("Missing Information",
                               "Please enter all required fields.")


def update_event_list():
    global event_list
    event_list.delete(0, 'end') #clear the respective list, allow new addition
    for event in scheduled_events:
        event_list.insert('end', f"{event[0]} - {event[1]} - {event[2]}") # add the event record, following the format: event name - event date - event time

def show_schedule():
    global schedule_list, schedule_tree
    df = pd.read_csv('schedule.csv')
    #print(df)
    for i in range(len(df.index)):
        schedule_list.append([df.loc[i][1], df.loc[i][2], df.loc[i][3], df.loc[i][4], df.loc[i][5], df.loc[i][6], df.loc[i][7], df.loc[i][8]])
    for row in schedule_list:
        for i in range(8):
            if row[i] == False:
                row[i] = "--"
        schedule_tree.insert("", "end", iid=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))


def show_payroll():
    global pre_payroll_list, payroll_list, payroll_tree
    df = pd.read_csv('payroll.csv')
    #print(df)
    for i in range(len(df.index)):
        pre_payroll_list.append([df.loc[i][1], df.loc[i][2], df.loc[i][3], df.loc[i][4], df.loc[i][5]])
    for row in pre_payroll_list:
        #payroll_list.insert("end", f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4] }")
        payroll_tree.insert("", "end", iid=row[0], values=(row[0], row[1], row[2], row[3], row[4]))
        


def create_dashboard():
    global entry_event_name, entry_event_date, entry_event_time, event_list, payroll_list, payroll_tree, schedule_tree

    dashboard = tk.Tk() #create new frame
    dashboard.title("HR Dashboard")

    notebook = ttk.Notebook(dashboard)

    # Memo tab
    memo_frame = ttk.Frame(notebook)
    notebook.add(memo_frame, text="Memo")

    ttk.Label(memo_frame, text="Event Name:").grid(row=0, column=0,
                                                         sticky="e")
    entry_event_name = tk.Entry(memo_frame)
    entry_event_name.grid(row=0, column=1)

    ttk.Label(memo_frame, text="Event Date (YYYY-MM-DD):").grid(row=1,
                                                                      column=0,
                                                                      sticky="e")
    entry_event_date = tk.Entry(memo_frame)
    entry_event_date.grid(row=1, column=1)

    ttk.Label(memo_frame, text="Event Time (HH:MM):").grid(row=2,
                                                                 column=0,
                                                                 sticky="e")
    entry_event_time = tk.Entry(memo_frame)
    entry_event_time.grid(row=2, column=1)

    button_add_event = tk.Button(memo_frame, text="Add Event",
                                 command=add_event)
    button_add_event.grid(row=3, column=0, columnspan=2, pady=10)

    event_list = tk.Listbox(memo_frame, height=10, width=50)
    event_list.grid(row=4, column=0, columnspan=2)
    update_event_list()

    # Schedule tab
    schedule_frame = ttk.Frame(notebook)
    notebook.add(schedule_frame, text="Schedule")
    #ttk.Label(schedule_frame, text="Schedule Content").grid(row=0, column=0)
    
    schedule_tree = ttk.Treeview(schedule_frame, columns=("eid", "mon", "tue", "wed", "thu", "fri", "sat", "sun"), show="headings", height=15)
    
    button_update_schedule = tk.Button(schedule_frame, text="Update Schedule", command=show_schedule)
    button_update_schedule.grid(row=0, column=0)
    
    #tree["columns"] = ("eid", "contract_type", "hour_count", "unit_pay", "total_pay")
    schedule_tree.column('#0', minwidth=0, width=0) #remove this line will have a big blank first column
    schedule_tree.column('#1', minwidth=0, width=50)
    schedule_tree.column('#2', minwidth=0, width=62)
    schedule_tree.column('#3', minwidth=0, width=62)
    schedule_tree.column('#4', minwidth=0, width=62)
    schedule_tree.column('#5', minwidth=0, width=62) 
    schedule_tree.column('#6', minwidth=0, width=62)
    schedule_tree.column('#7', minwidth=0, width=62)  
    schedule_tree.column('#8', minwidth=0, width=62)  
    
    schedule_tree.heading('eid', text="EID")
    schedule_tree.heading('mon', text="Monday")
    schedule_tree.heading('tue', text="Tuesday")
    schedule_tree.heading('wed', text="Wednesday")
    schedule_tree.heading('thu', text="Thursday")
    schedule_tree.heading('fri', text="Friday")
    schedule_tree.heading('sat', text="Saturday")
    schedule_tree.heading('sun', text="Sunday")
    
    
    schedule_tree.grid(row = 1, column = 0)    

    # Payroll tab
    payroll_frame = ttk.Frame(notebook)
    notebook.add(payroll_frame, text="Payroll")
    #ttk.Label(payroll_frame, text="Payroll Content").grid(row=0, column=0)
    
    
    payroll_tree = ttk.Treeview(payroll_frame, columns=("eid", "contract_type", "hour_count", "unit_pay", "total_pay"), show="headings", height=15)
    
    button_update_payroll = tk.Button(payroll_frame, text="Update Payroll", command=show_payroll)
    button_update_payroll.grid(row=0, column=0)
    
    #tree["columns"] = ("eid", "contract_type", "hour_count", "unit_pay", "total_pay")
    payroll_tree.column('#0', minwidth=0, width=0) #remove this line will have a big blank first column
    payroll_tree.column('#1', minwidth=0, width=50)
    payroll_tree.column('#2', minwidth=0, width=100)
    payroll_tree.column('#3', minwidth=0, width=100)
    payroll_tree.column('#4', minwidth=0, width=100)
    payroll_tree.column('#5', minwidth=0, width=100)    
    
    payroll_tree.heading('eid', text="EID")
    payroll_tree.heading('contract_type', text="contract_type")
    payroll_tree.heading('hour_count', text="hour_count")
    payroll_tree.heading('unit_pay', text="unit_pay")
    payroll_tree.heading('total_pay', text="total_pay")
    
    payroll_tree.grid(row = 1, column = 0)
    
    
    '''
    tree.bind('<<TreeviewSelect>>', item_selected)
    '''
    #tree.grid(row=1, column=0, sticky='nsew')
    '''
    # add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')    
    '''
    
    
    
    #payroll_list = tk.Listbox(payroll_frame, height=20, width=50)
    #payroll_list.grid(row=2, column = 0, pady=10)

    # Training tab
    training_frame = ttk.Frame(notebook)
    notebook.add(training_frame, text="Training")
    ttk.Label(training_frame, text="Training Content").grid(row=0, column=0)

    notebook.pack(expand=True, fill="both")
    dashboard.mainloop()


root = tk.Tk()
root.title("HR Application Login")
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

label_username = tk.Label(frame, text="Username:")
label_username.grid(row=0, column=0, sticky="e")
entry_username = tk.Entry(frame)
entry_username.grid(row=0, column=1)

label_password = tk.Label(frame, text="Password:")
label_password.grid(row=1, column=0, sticky="e")
entry_password = tk.Entry(frame, show="*")
entry_password.grid(row=1, column=1)

button_login = tk.Button(frame, text="Login", command=login)
button_login.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()