import tkinter as tk
from tkinter import W, messagebox


def reconstruction_gui(input_frame):
    delete_frame(input_frame)
    distribution_frame = tk.Frame(gui)
    distribution_frame.pack()

    label = tk.Label(distribution_frame, text = "Reconstruction stage")
    label.configure(font=(20))
    label.grid(row = 0, column = 0, columnspan=3, sticky = W, pady=30)

    label = tk.Label(distribution_frame, text = "Firebase")
    label.grid(row = 1, column = 0, sticky = W, pady=30, padx=10)

def distribution_gui(input_frame):
    delete_frame(input_frame)
    distribution_frame = tk.Frame(gui)
    distribution_frame.pack()
    label = tk.Label(distribution_frame, text = "Distribution stage")
    label.configure(font=(20))
    label.grid(row = 0, column = 0, columnspan=3, sticky = W, pady=30)

    label = tk.Label(distribution_frame, text = "Firebase")
    label.grid(row = 1, column = 0, sticky = W, pady=30, padx=10)
    
    label = tk.Label(distribution_frame, text = "Dropbox")
    label.grid(row = 2, column = 0, sticky = W, pady=30, padx=10)

    label = tk.Label(distribution_frame, text = "Clever")
    label.grid(row = 3, column = 0, sticky = W, pady=30, padx=10)

    button = tk.Button(distribution_frame, 
                            text='Confirm', 
                            width=25, 
                            command=lambda: reconstruction_gui(distribution_frame))
    button.grid(row = 4, column = 0, columnspan = 1, sticky = W, pady=15)

def delete_frame(frame):
    # messagebox.showwarning("showwarning", "Warning")
    for widgets in frame.winfo_children():
      widgets.destroy()
    frame.pack_forget()
    frame.destroy()

def set_input_window():
    gui.geometry("380x420")
    gui.title("Secret Sharing Application")

    icon = tk.PhotoImage(file="./GraphicalUserInterface/s-logo.png")
    gui.iconphoto(True, icon)

def input_gui():
    input_frame = tk.Frame(gui)
    input_frame.pack()

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
                            command=lambda: distribution_gui(input_frame))
    button.grid(row = 4, column = 1, columnspan = 2, sticky = W, pady=15)
    
if __name__ == '__main__':
    gui = tk.Tk()
    set_input_window()
    input_gui()
    gui.mainloop()