import tkinter as tk
from tkinter import W, messagebox
import sys
sys.path.insert(1, './')
from API import input_api as i_api, distribution_api as d_api, reconstruction_api as r_api


def reconstruction_gui(input_frame, length_first, length_second, length_third, threshold):
    delete_frame(input_frame)
    distribution_frame = tk.Frame(gui)
    distribution_frame.pack()

    label = tk.Label(distribution_frame, text = "Reconstruction stage")
    label.configure(font=(20))
    label.grid(row = 0, column = 0, columnspan=3, sticky = W, pady=30)

    label = tk.Label(distribution_frame, text = "Firebase: " + str(length_first) + " shares used")
    label.grid(row = 1, column = 0, sticky = W, pady=30, padx=10)

    label = tk.Label(distribution_frame, text = "Dropbox: " + str(length_second) + " shares used")
    label.grid(row = 2, column = 0, sticky = W, pady=30, padx=10)

    label = tk.Label(distribution_frame, text = "CleverCloud: " + str(length_third) + " shares used")
    label.grid(row = 3, column = 0, sticky = W, pady=30, padx=10)

    secret = r_api(threshold)

    label = tk.Label(distribution_frame, text = "The secret is: " + secret)
    label.grid(row = 4, column = 0, sticky = W, pady=30, padx=10)

def distribution_gui(input_frame, first_part, second_part, third_part, threshold):
    delete_frame(input_frame)
    distribution_frame = tk.Frame(gui)
    distribution_frame.pack()

    label = tk.Label(distribution_frame, text = "Distribution stage")
    label.configure(font=(20))
    label.grid(row = 0, column = 0, columnspan=3, sticky = W, pady=30)

    string_first_part = str(first_part)
    string_first_part = string_first_part[1:len(string_first_part)-1]

    string_second_part = str(second_part)
    string_second_part = string_second_part[1:len(string_second_part)-1]

    string_third_part = str(third_part)
    string_third_part = string_third_part[1:len(string_third_part)-1]

    label = tk.Label(distribution_frame, text = "Firebase: " + string_first_part)
    label.grid(row = 1, column = 0, sticky = W, pady=30, padx=10)
    
    label = tk.Label(distribution_frame, text = "Dropbox: " + string_second_part)
    label.grid(row = 3, column = 0, sticky = W, pady=30, padx=10)

    label = tk.Label(distribution_frame, text = "CleverCloud: " + string_third_part)
    label.grid(row = 5, column = 0, sticky = W, pady=30, padx=10)

    len_fst = len(first_part)
    len_sec = 0
    len_thr = 0

    if len_fst < threshold:  
        len_sec = len(second_part)
    if len_fst + len_sec < threshold:
        len_thr = len(third_part)

    button = tk.Button(distribution_frame, 
                            text='Confirm', 
                            width=25, 
                            command=lambda: reconstruction_gui(distribution_frame, len_fst, len_sec, len_thr, threshold))
    button.grid(row = 7, column = 0, columnspan = 1, sticky = W, pady=15)

def send_input(input_frame, text_secret, text_shares, text_threshold):
    secret = text_secret.get()
    shares_number = int(text_shares.get())
    threshold = int(text_threshold.get())
    share_list, threshold = i_api(secret, shares_number, threshold)
    (first_part, second_part, third_part) = d_api(share_list)
    distribution_gui(input_frame, first_part, second_part, third_part, threshold)

def delete_frame(frame):
    # messagebox.showwarning("showwarning", "Warning")
    for widgets in frame.winfo_children():
      widgets.destroy()
    frame.pack_forget()
    frame.destroy()

def set_input_window():
    gui.geometry("480x520")
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
                            command=lambda: send_input(input_frame, text_secret, text_shares, text_threshold))
    button.grid(row = 4, column = 1, columnspan = 2, sticky = W, pady=15)
    
if __name__ == '__main__':
    gui = tk.Tk()
    set_input_window()
    input_gui()
    gui.mainloop()