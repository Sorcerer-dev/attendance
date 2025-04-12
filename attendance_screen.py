# This file is used to create the attendance screen where users can mark attendance for a selected date.

# Requires user defined modules like attendance_widgets and excel_util for creating buttons and saving to Excel.
import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas, Frame
import os
from datetime import datetime
from attendance_widgets import create_attendance_buttons, toggle_all
from excel_util import save_attendance_to_excel

# Function to open the attendance screen
def open_attendance_screen(date_str, previous_window, open_calendar_callback):
    selected_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%m-%Y")
    previous_window.destroy()

    attendance_window = tk.Tk()
    attendance_window.title("Mark Attendance")
    attendance_window.state('zoomed')

    file_name = "attendance.xlsx"
    button_states = ["P"] * 60

    # Load existing states if available
    if os.path.exists(file_name):
        import pandas as pd 
        df = pd.read_excel(file_name)
        if selected_date in df.columns: 
            button_states = df[selected_date].fillna("P").tolist() 

    canvas = Canvas(attendance_window) 
    scrollbar = Scrollbar(attendance_window, orient="vertical", command=canvas.yview) 
    scrollable_frame = Frame(canvas) 
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) 
    canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    buttons, frame = create_attendance_buttons(scrollable_frame, button_states)

    toggle_btn = tk.Button(scrollable_frame, text="Mark All Absent", font=("Arial", 14), width=20, height=1)
    toggle_btn.pack(pady=10)
    toggle_btn.config(command=lambda: toggle_all(button_states, buttons, toggle_btn))

    # Function to mark attendance and save to Excel
    def mark_attendance():
        save_attendance_to_excel(file_name, selected_date, button_states)
        messagebox.showinfo("Success", "Attendance Marked Successfully!")
        attendance_window.destroy()
        open_calendar_callback()  # Call the passed callback function

    mark_button = tk.Button(scrollable_frame, text="Mark Attendance", command=mark_attendance,
                            bg="blue", fg="white", font=("Arial", 16), width=15, height=2)
    mark_button.pack(pady=10)

    back_button = tk.Button(scrollable_frame, text="Back",
                            command=lambda: [attendance_window.destroy(), open_calendar_callback()],
                            font=("Arial", 14), width=15, height=2)
    back_button.pack(pady=10)

    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))
    attendance_window.mainloop()
