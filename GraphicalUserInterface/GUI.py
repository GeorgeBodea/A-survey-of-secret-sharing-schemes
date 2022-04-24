import tkinter as tk
from tkinter import messagebox

def distribution_stage():
    label = tk.Label(gui, text = "Distribution stage")
    label.pack()

def delete_input_window(label, button):
    messagebox.showwarning("showwarning", "Warning")
    label.destroy()
    button.destroy()
    distribution_stage()

def set_input_window():
    gui.geometry("420x420")
    gui.title("Secret Sharing Application")

    icon = tk.PhotoImage(file="./GraphicalUserInterface/s-logo.png")
    gui.iconphoto(True, icon)


def input_stage():
    set_input_window()
    label = tk.Label(gui, text="Input the secret")
    label.pack()

    button = tk.Button(gui, 
                            text='Confirm', 
                            width=25, 
                            command=lambda: delete_input_window(label, button))
    button.pack()
    

def start_gui():
    input_stage()

if __name__ == '__main__':
    gui = tk.Tk()
    start_gui()
    gui.mainloop()