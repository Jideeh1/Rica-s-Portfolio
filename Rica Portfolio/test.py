import psutil
import time
import os
import tkinter as tk
import win32gui
import re
import subprocess

from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
from tkinter import messagebox


start_time = None
tracking = False
last_window = None
last_app = None
activity_log = {}


# Functionss
def show_log_path():
    log_path = os.path.join(os.path.expanduser("~/Documents"), "STA Logs")
    # Show log path in a simple message box
    messagebox.showinfo("Log Path", f"Log files are saved in:\n{log_path}")

def get_active_window_title():
    try:
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except Exception as e:
        return "Unknown"

def get_base_application_name(window_title):
    match = re.search(r'(\w[\w\s]*\w+)$', window_title)
    if match:
        return match.group(1).strip()
    return "Unknown"

def log_window_activity():
    global last_window, start_time, activity_log, last_app
    current_window = get_active_window_title()
    now = datetime.now()

    current_app = get_base_application_name(current_window)

    if current_app == "Screen Time Counter":
        return

    if last_window and last_app != current_app:
        time_spent = now - start_time
        if last_app in activity_log:
            activity_log[last_app] += time_spent
        else:
            activity_log[last_app] = time_spent
        print(f"App: {last_app}, Time Spent: {time_spent}, Date: {now.strftime('%I:%M %p %m-%d-%Y')}")
        start_time = now

    last_window = current_window
    last_app = current_app

def format_time(total_time):
    total_seconds = int(total_time.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return f"{hours}:{minutes:02}:{seconds:02}"

def save_activity_log():
    now = datetime.now()
    log_filename = now.strftime("%m-%d-%Y") + " activity log.txt"

    documents_path = os.path.expanduser("~/Documents")

    if documents_path is None:
        print("Path could not be found.")
        return
    
    test_folder = os.path.join(documents_path, "STA Logs")

    if not os.path.exists(test_folder):
        try:
            os.makedirs(test_folder)
        except Exception as e:
            print(f"Error creating folder: {e}")
            return
    
    log_file_path = os.path.join(test_folder, log_filename)

    try:
        with open(log_file_path, "w", encoding="utf-8") as file:
            for app, total_time in activity_log.items():
                formatted_time = format_time(total_time)
                file.write(f"{app} | {formatted_time} | {now.strftime('%I:%M %p %m-%d-%Y')}\n")
        
        print(f"Activity log saved to: {log_file_path}")
    except Exception as e:
        print(f"An error have ocurred in saving the activity log: {e}")

def update_timer():
    global start_time
    if tracking and start_time:
        elapsed_time = datetime.now() - start_time
        timer_label.config(text=f"Elapsed Time: {elapsed_time}")
        log_window_activity()
    application.after(1000, update_timer)

def run_app():
    global start_time, tracking, last_window, last_app
    if not tracking:
        start_time = datetime.now()
        last_window = get_active_window_title()
        last_app = get_base_application_name(last_window)
        tracking = True
        run.config(text="Stop", command=stop)
        print("Screen time tracking started.")

def stop():
    global tracking, last_window
    if tracking:
        tracking = False
        log_window_activity()
        save_activity_log()
        last_window = None
        print(f"Screen time tracking stopped.")
        run.config(text="Run", command=run_app)

def reset():
    global start_time, tracking, last_window, last_app, activity_log
    tracking = False
    start_time = None
    last_window = None
    last_app = None
    activity_log = {}
    
    now = datetime.now()
    log_filename = now.strftime("%m-%d-%Y") + " activity log.txt"
    documents_path = os.path.expanduser("~/Documents")
    test_folder = os.path.join(documents_path, "STA Logs")
    log_file_path = os.path.join(test_folder, log_filename)
    
    confirm = messagebox.askyesno(
        "Delete Log File", 
        f"Are you sure you want to delete TODAY's log file ({log_filename})? This action cannot be undone."
    )

    if confirm:
        if os.path.exists(log_file_path):
            try:
                os.remove(log_file_path)
                print(f"Log file {log_filename} deleted.")
            except Exception as e:
                print(f"Error deleting log file: {e}")
        
        timer_label.config(text="Elapsed Time: 0:00:00")
        run.config(text="Run", command=run_app)
        print("Screen time reset.")
    else:
        print("Log file deletion canceled.")

def open_log_folder():
    user_documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    test_folder = os.path.join(user_documents_path, "STA Logs")
    
    if os.path.exists(test_folder):
        subprocess.run(["explorer", test_folder])
    else:
        messagebox.showerror("Error", f"Folder '{test_folder}' does not exist.")

def open_recent_log():
    user_documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    test_folder = os.path.join(user_documents_path, "STA Logs")
    
    if os.path.exists(test_folder):
        log_files = [f for f in os.listdir(test_folder) if f.endswith(".txt")]
        
        if log_files:
            recent_log_file = max(log_files, key=lambda f: os.path.getmtime(os.path.join(test_folder, f)))
            recent_log_path = os.path.join(test_folder, recent_log_file)
            
            subprocess.run(["explorer", recent_log_path])
        else:
            messagebox.showerror("Error", "No log files found in the 'STA Logs' folder.")
    else:
        messagebox.showerror("Error", f"Folder '{test_folder}' does not exist.")

application = tk.Tk()
application.geometry("750x300")
application.iconbitmap("assets/monitor.ico")
application.title('Screen Time Counter')

navbar = Menu(application)
filemenu = Menu(navbar, tearoff=0)
filemenu.add_command(label="View Files", command=open_log_folder)
filemenu.add_command(label="Load Recent File", command=open_recent_log)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=application.quit)
navbar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(navbar, tearoff=0)
helpmenu.add_command(label="Log Path", command=lambda: show_log_path())
navbar.add_cascade(label="Help", menu=helpmenu)

timer_label = tk.Label(application, text="Elapsed Time: 0:00:00", font=("Arial", 20))
timer_label.pack(pady=20)

run = tk.Button(application, text="Run", font=("Arial", 25), command=run_app)
run.place(relx=0.35, rely=0.5, anchor="center")

quit_btn = tk.Button(application, text="Exit", font=("Arial", 25), command=application.quit)
quit_btn.place(relx=0.65, rely=0.5, anchor="center")

reset_btn = tk.Button(application, text="Reset", font=("Arial", 25), command=reset)
reset_btn.place(relx=0.5, rely=0.7, anchor="center")

application.config(menu=navbar)

update_timer()
application.mainloop()
