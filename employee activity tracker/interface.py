import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# Function to run the tracker script
def start_tracking():
    name = name_entry.get()
    if not name.strip():
        messagebox.showerror("Input Error", "Please enter your name.")
        return
    
    messagebox.showinfo("Login", f"Welcome, {name}! Starting activity tracking.")
    
    # Run the tracking script
    python_exe = sys.executable  # Path to Python executable
    script_path = os.path.join(os.path.dirname(__file__), "activity_tracker.py")  # Fixed __file__
    subprocess.Popen([python_exe, script_path])  # Launch script in parallel
    
    root.destroy()  # Optional: close login window

# GUI Setup
root = tk.Tk()
root.title("Employee Activity Tracker Login")
root.geometry("350x200")
root.configure(bg="#f0f2f5")

tk.Label(root, text="Employee Activity Tracker", font=("Helvetica", 16, "bold"), bg="#f0f2f5").pack(pady=20)
tk.Label(root, text="Enter Employee Name:", bg="#f0f2f5").pack()

name_entry = tk.Entry(root, font=("Helvetica", 12), width=30)
name_entry.pack(pady=5)

login_btn = tk.Button(root, text="Login", command=start_tracking, font=("Helvetica", 12),
                      bg="#007bff", fg="white", padx=10, pady=5)
login_btn.pack(pady=20)

root.mainloop()
