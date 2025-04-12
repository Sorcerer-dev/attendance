# attendance_widgets.py
import tkinter as tk

def create_attendance_buttons(parent, button_states):
    buttons = []
    colors = {"P": "green", "A": "red", "H": "orange", "OD": "grey"}

    def toggle_button(index):
        states = ["P", "A", "H", "OD"]
        current = button_states[index]
        next_state = states[(states.index(current) + 1) % len(states)]
        button_states[index] = next_state
        buttons[index].config(bg=colors[next_state], text=f"{index+1} ({next_state})")

    frame = tk.Frame(parent)
    frame.pack(pady=20)

    for i in range(60):
        btn = tk.Button(frame, text=f"{i+1} ({button_states[i]})", bg=colors[button_states[i]],
                        font=("Arial", 14), width=6, height=2,
                        command=lambda i=i: toggle_button(i))
        buttons.append(btn)
        btn.grid(row=i//10, column=i%10, padx=5, pady=5)

    return buttons, frame

def toggle_all(button_states, buttons, toggle_button):
    if toggle_button["text"] == "Mark All Absent":
        new_state, new_color = "A", "red"
        toggle_button.config(text="Mark All Present")
    else:
        new_state, new_color = "P", "green"
        toggle_button.config(text="Mark All Absent")

    for i in range(60):
        button_states[i] = new_state
        buttons[i].config(bg=new_color, text=f"{i+1} ({new_state})")
