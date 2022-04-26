import tkinter as tk
from tkinter import W, messagebox

def distribution_stage(input_frame):
    delete_frame(input_frame)
    label = tk.Label(input_frame, text = "Distribution stage")
    label.grid(row = 0, column = 2, columnspan = 2, sticky = W, pady=30)

    label = tk.Label(input_frame, text = "Firebase")
    label.grid(row = 1, column = 0, columnspan = 2, sticky = W, pady=30)
    
    label = tk.Label(input_frame, text = "Dropbox")
    label.grid(row = 1, column = 1, columnspan = 2, sticky = W, pady=30)

    label = tk.Label(input_frame, text = "Clever")
    label.grid(row = 1, column = 2, columnspan = 2, sticky = W, pady=30)

def delete_frame(frame):
    messagebox.showwarning("showwarning", "Warning")
    # list_of_widgets = input_frame.grid_slaves()
    # for widgets in list_of_widgets:
    #     widgets.grid_forget()
    for widgets in frame.winfo_children():
      widgets.destroy()

def set_input_window():
    gui.geometry("380x420")
    gui.title("Secret Sharing Application")

    icon = tk.PhotoImage(file="./GraphicalUserInterface/s-logo.png")
    gui.iconphoto(True, icon)

def input_stage():
    title = tk.Label(input_frame, text="Secret Sharing Application ")
    title.configure(font=(20))
    title.grid(row = 0, column = 2, columnspan = 2, sticky = W, pady=30)

    label_secret = tk.Label(input_frame, text="Input the secret: ")
    label_secret.grid(row = 1, column = 0, columnspan = 3, sticky = W, pady=20, padx=30)

    text_secret = tk.Entry(input_frame)
    text_secret.grid(row = 1, column = 3, sticky = W)

    label_shares = tk.Label(input_frame, text="Input the number of shares: ")
    label_shares.grid(row = 2, column = 0, columnspan = 3, sticky = W, pady=20, padx=30)    

    text_shares = tk.Entry(input_frame)
    text_shares.grid(row = 2, column = 3, sticky = W)

    label_threshold = tk.Label(input_frame, text="Input the threshold: ")
    label_threshold.grid(row = 3, column = 0, columnspan = 3, sticky = W, pady=20, padx=30)    

    text_threshold = tk.Entry(input_frame)
    text_threshold.grid(row = 3, column = 3, sticky = W)

    button = tk.Button(input_frame, 
                            text='Confirm', 
                            width=25, 
                            command=lambda: distribution_stage(input_frame))
    button.grid(row = 4, column = 1, columnspan = 2, sticky = W, pady=15)
    
if __name__ == '__main__':
    gui = tk.Tk()
    set_input_window()
    input_frame = tk.Frame(gui)
    input_frame.pack()
    input_stage()
    gui.mainloop()