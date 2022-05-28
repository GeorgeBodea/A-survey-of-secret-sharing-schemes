import tkinter as tk
from tkinter import W, messagebox
import sys

from matplotlib.pyplot import flag
sys.path.insert(1, './')
from API import input_api as i_api, distribution_firebase_api as d_fb_api, reconstruction_api as r_api

def delete_frame(frame):
    # messagebox.showwarning("showwarning", "Warning")
    for widgets in frame.winfo_children():
      widgets.destroy()
    frame.pack_forget()
    frame.destroy()

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

def reconstruct_gui():
    return 1

def send_input(input_frame, 
                secret, shares_number, threshold, 
                button, 
                list_entry_fb):
    # Secret
    share_list = i_api(secret, shares_number, threshold)
    counter = 0
    
    for entry in list_entry_fb:
        fb_key = entry.get()
        app_name = "app" + str(counter)
        d_fb_api(fb_key, share_list[counter], app_name)
        counter += 1

    # secret = text_secret.get()
    # shares_number = int(text_shares.get())
    # threshold = int(text_threshold.get())
    # share_list, threshold = i_api(secret, shares_number, threshold)
    # (first_part, second_part, third_part) = d_api(share_list)
    # distribution_gui(input_frame, first_part, second_part, third_part, threshold)

def db_set_gui(input_frame, 
                secret, shares_number, threshold, shares_proportions):
    delete_frame(input_frame)
    input_frame = tk.Frame(gui)
    input_frame.pack()

    next_pos = 0 

    label = tk.Label(input_frame, text = "Input stage")
    label.configure(font=(20))
    label.grid(row = next_pos, column = 0, columnspan=3, sticky = W, pady=30)
    next_pos += 1

    if (shares_proportions[0] != 0):
        label = tk.Label(input_frame, text = "Firebase keys: ")
        label.configure(font=(10))
        label.grid(row = next_pos, column = 0, columnspan=3, sticky = W, pady=30)
        next_pos += 1

        list_entry_fb = []
        for i in range(shares_proportions[0]):
            entry = tk.Entry(input_frame)
            entry.grid(row = next_pos, column = 1, sticky = W, pady=5)
            entry.insert(0, "Key")
            next_pos += 1
            list_entry_fb.append(entry)

    button = tk.Button(input_frame, 
                            text="Confirm",
                            width=25, 
                            command=lambda: send_input(
                                input_frame, 
                                secret, shares_number, threshold, 
                                button,
                                list_entry_fb
                                ))
    button.grid(row = next_pos, column = 1, sticky = W, pady=15)
    
def check_shares_number(input_frame, 
                        secret, shares_number, threshold, 
                        button, label_select,
                        num_firebase, num_clever, num_dropbox): 
    shares_placed = 0                    
    shares_proportions = [0, 0, 0]
    if (num_firebase.get() != ''):
        num_firebase = int(num_firebase.get())
        shares_placed += num_firebase
        shares_proportions[0] = num_firebase

    if (num_clever.get() != ''):
        num_clever = int(num_clever.get()) 
        shares_placed += num_clever
        shares_proportions[1] = num_clever  

    if (num_dropbox.get() != ''):
        num_dropbox = int(num_dropbox.get())
        shares_placed += num_dropbox
        shares_proportions[2] = num_dropbox
           
    if (shares_number == shares_placed):
        db_set_gui(input_frame, secret, shares_number, threshold, shares_proportions) 
    else:
        label_select['text'] = "Number of shares: " + str(shares_number) + "\n" " You selected: " + str(shares_placed)

def db_types_gui(input_frame, 
                secret, shares_number, threshold, 
                button, label_select,
                isFirebase, isClever, isDropbox, 
                ck_firebase, ck_clever, ck_dropbox):
    label_select['text'] = "Number of shares: " + str(shares_number)
    ck_firebase.config(state=tk.DISABLED)
    ck_clever.config(state=tk.DISABLED)
    ck_dropbox.config(state=tk.DISABLED)

    num_firebase = tk.Spinbox(input_frame, from_=0, to= 0)
    num_clever = tk.Spinbox(input_frame, from_=0, to= 0)
    num_dropbox = tk.Spinbox(input_frame, from_=0, to= 0)

    if (isFirebase.get() == 1):
        num_firebase = tk.Spinbox(input_frame, from_=1, to= shares_number)
        num_firebase.grid(row = 2, column = 2, sticky = W)
        # num_firebase.bind(event_name, handler, add=None)
    if (isClever.get() == 1):
        num_clever = tk.Spinbox(input_frame, from_=1, to= shares_number)
        num_clever.grid(row = 3, column = 2, sticky = W)
    if (isDropbox.get() == 1):
        num_dropbox = tk.Spinbox(input_frame, from_=1, to= shares_number)
        num_dropbox.grid(row = 4, column = 2, sticky = W)
        
    button['text'] = 'Confirm'
    button['command'] =lambda: check_shares_number(input_frame, 
                                            secret, shares_number, threshold, 
                                            button,  label_select,
                                            num_firebase, num_clever, num_dropbox) 


def shares_location_gui(input_frame, secret, shares_number, threshold):
    delete_frame(input_frame)
    input_frame = tk.Frame(gui)
    input_frame.pack()

    title = tk.Label(input_frame, text="Setup databases stage")
    title.configure(font=(20))
    title.grid(row = 0, column = 1, columnspan = 2, sticky = W, pady=30)

    label_select = tk.Label(input_frame, text = "Select your types of cloud databases: ")
    label_select.grid(row = 1, column = 1, sticky = W, pady=30, padx=10)

    isFirebase = tk.IntVar()
    ck_firebase = tk.Checkbutton(input_frame, text="Google Firebase", variable=isFirebase)
    ck_firebase.grid(row = 2, column = 1, sticky = W, pady=20, padx=30)

    isClever = tk.IntVar()
    ck_clever = tk.Checkbutton(input_frame, text="CleverCloud", variable=isClever)
    ck_clever.grid(row = 3, column = 1, sticky = W, pady=20, padx=30)

    isDropbox = tk.IntVar()
    ck_dropbox = tk.Checkbutton(input_frame, text="Dropbox", variable=isDropbox)
    ck_dropbox.grid(row = 4, column = 1, sticky = W, pady=20, padx=30)

    button = tk.Button(input_frame, 
                            text="Confirm databases types",
                            width=25, 
                            command=lambda: db_types_gui(
                                input_frame, 
                                secret, shares_number, threshold, 
                                button, label_select,
                                isFirebase, isClever, isDropbox, 
                                ck_firebase, ck_clever, ck_dropbox))
    button.grid(row = 5, column = 1, sticky = W, pady=15)

    # shares_number = int(text_shares)
    # for i in range(1, shares_number+1):
    #     text_secret = tk.Entry(input_frame)
    #     text_secret.grid(row = i, column = 1, sticky = W)

def input_gui(input_frame):
    delete_frame(input_frame)
    input_frame = tk.Frame(gui)
    input_frame.pack()

    title = tk.Label(input_frame, text="Input stage")
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
                            command=lambda: shares_location_gui(input_frame, 
                            text_secret.get(), 
                            int(text_shares.get()),
                            int(text_threshold.get())
                            ))
    button.grid(row = 4, column = 1, columnspan = 2, sticky = W, pady=15)

def start_gui():
    start_frame = tk.Frame(gui)
    start_frame.pack()

    title = tk.Label(start_frame, text="Secret Sharing Application")
    title.configure(font=(20))
    title.grid(row = 0, column = 1, columnspan = 3, sticky = W, pady=30)

    label = tk.Label(start_frame, text="Would you like to: ")
    label.grid(row = 1, column = 1, sticky = W, pady=20, padx=30)

    button = tk.Button(start_frame, 
                            text='Share a secret', 
                            width=25, 
                            command=lambda: input_gui(start_frame))
    button.grid(row = 2, column = 1, sticky = W, pady=15)

    button = tk.Button(start_frame, 
                            text='Reconstruct a secret', 
                            width=25, 
                            command=lambda: input_gui(start_frame))
    button.grid(row = 3, column = 1, sticky = W, pady=15)

def set_input_window():
    gui.geometry("480x520")
    gui.title("Secret Sharing Application")

    icon = tk.PhotoImage(file="./GraphicalUserInterface/s-logo.png")
    gui.iconphoto(True, icon)
    
if __name__ == '__main__':
    gui = tk.Tk()
    set_input_window()
    start_gui()
    gui.mainloop()