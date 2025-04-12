# this file is used to create a calendar page using tkinter and tkcalendar

# uses user defined modules like attendance_screen to open the attendance screen
import tkinter as tk
from tkinter import ttk, Toplevel
from tkcalendar import Calendar
from datetime import datetime
from attendance_screen import open_attendance_screen

root = None
cal = None

# Function to open a popup for selecting month or year
def open_date_selector(is_year):
    popup = Toplevel(root)
    popup.title("Select Month & Year" if is_year else "Select Year")
    popup.geometry("200x150")

    selected_date_str = cal.get_date()
    selected_date_obj = datetime.strptime(selected_date_str, "%Y-%m-%d")
    current_year = selected_date_obj.year
    current_month = selected_date_obj.month

    if is_year:
        tk.Label(popup, text="Select Year:").pack(pady=5)
        year_var = tk.StringVar(value=str(current_year))
        year_dropdown = ttk.Combobox(popup, textvariable=year_var, values=[str(y) for y in range(2000, 2031)], width=5)
        year_dropdown.pack(pady=5)

        # This function applies the selected year to the calendar
        def apply_year():
            cal.config(year=int(year_var.get()))
            popup.destroy()

        tk.Button(popup, text="Apply", command=apply_year).pack(pady=10)
    else:
        tk.Label(popup, text="Select Month:").pack(pady=5)
        month_var = tk.StringVar(value=str(current_month))
        month_dropdown = ttk.Combobox(popup, textvariable=month_var, values=[str(m) for m in range(1, 13)], width=3)
        month_dropdown.pack(pady=5)

        # This function applies the selected month to the calendar
        def apply_month():
            cal.config(month=int(month_var.get()))
            popup.destroy()

        tk.Button(popup, text="Apply", command=apply_month).pack(pady=10)

# Function to open the calendar and set up the main window 
def open_calendar():
    global root, cal
    root = tk.Tk()
    root.title("Select Date")
    root.state('zoomed')

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_year, current_month, current_day = map(int, current_date.split('-'))

    cal = Calendar(root, selectmode='day', date_pattern='yyyy-MM-dd',
                   year=current_year, month=current_month, day=current_day,
                   font=("Arial", 20), padx=40, pady=40)
    cal.pack(pady=20)

    cal.bind("<Button-1>", lambda event: open_date_selector(event.x < cal.winfo_width() // 2))

    next_button = tk.Button(root, text="Next", command=lambda: open_attendance_screen(cal.get_date(), root, open_calendar),
                         bg="blue", fg="white", font=("Arial", 16), width=40, height=2)

    next_button.pack(pady=10)

    root.mainloop()
