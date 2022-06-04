import tkinter as tk
from tkinter import W, messagebox, filedialog
import sys
import json
import traceback

from matplotlib.pyplot import flag
sys.path.insert(1, './')
from API import input_api as i_api
from API import distribution_firebase_api as d_fb_api, distribution_clevercloud_api as d_cc_api, distribution_cosmos_api as d_co_api
from API import retrieval_firebase_api as r_fb_api, retrieval_clevercloud_api as r_cc_api, retrieval_cosmos_api as r_co_api
from API import reconstruction_api as r_api
from API import check_threshold_shares as check_th_sh

def delete_frame(frame):
    for widgets in frame.winfo_children():
      widgets.destroy()
    frame.pack_forget()
    frame.destroy()

def back_to_start(frame):
    delete_frame(frame)
    frame = tk.Frame(gui)
    frame.pack()    

    start_gui()

def secret_reconstruction_gui(frame, list_of_shares):
    delete_frame(frame)
    frame = tk.Frame(gui)
    frame.pack()

    secret = r_api(list_of_shares)

    title = tk.Label(frame, text="The secret is:")
    title.configure(font=(20))
    title.grid(row = 0, column = 1, columnspan = 2, sticky = W, pady=30)

    label_select = tk.Label(frame, text = str(secret))
    label_select.configure(font=(20))
    label_select.grid(row = 1, column = 1, sticky = W, pady=30, padx=10)

    button = tk.Button(frame, 
                            text='Back to start', 
                            width=25, 
                            command=lambda: back_to_start(frame))
    button.grid(row = 2, column = 1, sticky = W, pady=15)

def reconstruct_secret(frame, 
                list_of_arguments, 
                button, 
                labels_fb,
                labels_cc,
                labels_co):
    counter = 0

    threshold = list_of_arguments[0]
    shares_number = list_of_arguments[1]

    list_of_shares = []

    for label in labels_fb:
        path_file = label["text"]    
        file = open(path_file)
        fb_key = json.load(file)
        app_name = "app" + str(counter)
        share = r_fb_api(fb_key, app_name)
        list_of_shares.append(share)        
        counter += 1

    for label in labels_cc:
        path_file = label["text"]    
        file = open(path_file)
        cc_key = json.load(file)
        share = r_cc_api(cc_key)
        list_of_shares.append(share)
        counter += 1

    for label in labels_co:
        path_file = label["text"]    # 
        file = open(path_file)
        co_key = json.load(file)
        share = r_co_api(co_key)
        list_of_shares.append(share)
        counter += 1

    secret_reconstruction_gui(frame, list_of_shares)


def sent_confirmation_gui(frame):
    delete_frame(frame)
    frame = tk.Frame(gui)
    frame.pack()

    title = tk.Label(frame, text="The secret has been shared")
    title.configure(font=(20))
    title.grid(row = 0, column = 1, columnspan = 2, sticky = W, pady=30)

    label_select = tk.Label(frame, text = "Would you like to reconstruct the share now?")
    label_select.grid(row = 1, column = 1, sticky = W, pady=30, padx=10)

    button = tk.Button(frame, 
                            text='Confirm', 
                            width=25, 
                            command=lambda: reconstruction_input_gui(frame))
    button.grid(row = 2, column = 1, sticky = W, pady=15)
    button.config( height = 2, width = 45 )

def distribute_shares(frame, 
                list_of_arguments, 
                button, 
                labels_fb,
                labels_cc,
                labels_co): 
    counter = 0

    secret = list_of_arguments[0]
    shares_number = list_of_arguments[1]
    threshold = list_of_arguments[2]

    share_list = i_api(secret, shares_number, threshold)

    for label in labels_fb:
        path_file = label["text"]    
        file = open(path_file)
        fb_key = json.load(file)
        app_name = "app" + str(counter)
        d_fb_api(fb_key, app_name, share_list[counter])
        counter += 1

    for label in labels_cc:
        path_file = label["text"]    
        file = open(path_file)
        cc_key = json.load(file)
        d_cc_api(cc_key, share_list[counter])
        counter += 1

    for label in labels_co:
        path_file = label["text"]    # 
        file = open(path_file)
        co_key = json.load(file)
        d_co_api(co_key, share_list[counter])
        counter += 1

    sent_confirmation_gui(frame)


def browseFiles(label_file_explorer):
    file_name = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("JSON files",
                                                        "*.json*"),
                                                        ("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
    label_file_explorer.configure(text= file_name)

def something():
    return 1

def entries_creator(frame, next_pos, entries_number, database_name):
    label = tk.Label(frame, text = database_name + " keys: ")
    label.configure(font=(7))
    label.grid(row = next_pos, column = 1, sticky = W, pady=(20, 0))
    next_pos += 1

    list_labels = []

    for i in range(entries_number):
        label_file_explorer = tk.Label(frame,
                                text = "Add key file",
                                height = 4,
                                fg = "blue")
        label_file_explorer.grid(row = next_pos, column = 1, sticky = W)

        next_pos += 1
        button_explore = tk.Button(frame,
                        text = "Browse Files",
                        command = lambda: browseFiles(label_file_explorer))
        button_explore.grid(row = next_pos, column = 1, sticky = W)
        
        next_pos += 1
        list_labels.append(label_file_explorer)

    return (list_labels, next_pos)


def access_databases_gui(frame, 
                list_of_arguments,
                shares_proportions):
    delete_frame(frame)
    main_frame = tk.Frame(gui)
    main_frame.pack(fill = tk.BOTH, expand = 1)

    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand = 1)

    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    frame = tk.Frame(canvas)

    canvas.create_window((0, 0), window=frame, anchor="nw")

    next_pos = 0 

    label = tk.Label(frame, text = "Access databases stage")
    label.configure(font=(20))
    label.grid(row = next_pos, column = 1, columnspan=3, sticky = W,  pady=(30, 10))
    next_pos += 1

    fb_number = shares_proportions[0]
    cc_number = shares_proportions[1]
    co_number = shares_proportions[2]

    labels_fb = []
    labels_cc = []
    labels_co = []

    if (fb_number != 0):
        labels_fb, next_pos = entries_creator(frame, next_pos, fb_number, "Google Firebase")
    
    if (cc_number != 0):
        labels_cc, next_pos = entries_creator(frame, next_pos, cc_number, "Clever Cloud")
            
    if (co_number != 0):
        labels_co, next_pos = entries_creator(frame, next_pos, co_number , "Azure Cosmos") 

    len_of_args = len(list_of_arguments)
    
    if (len_of_args == 3):
        button = tk.Button(frame, 
                                text="Distribute",
                                width=25, 
                                command=lambda: distribute_shares(
                                    main_frame, 
                                    list_of_arguments, 
                                    button,
                                    labels_fb,
                                    labels_cc,
                                    labels_co
                                    ))
        button.grid(row = next_pos, column = 1, sticky = W, pady=(30, 0))
    else:
        button = tk.Button(frame, 
                                text="Reconstruct",
                                width=25, 
                                command=lambda: reconstruct_secret(
                                    main_frame, 
                                    list_of_arguments, 
                                    button,
                                    labels_fb,
                                    labels_cc,
                                    labels_co
                                    ))
        button.grid(row = next_pos, column = 1, sticky = W, pady=(30, 0))

    
def equal_shares_number(frame, 
                        list_of_arguments, 
                        button, label_select,
                        num_firebase, num_clever, num_cosmos): 
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

    if (num_cosmos.get() != ''):
        num_cosmos = int(num_cosmos.get())
        shares_placed += num_cosmos
        shares_proportions[2] = num_cosmos

    shares_number = list_of_arguments[1]
           
    if (shares_number == shares_placed):
        access_databases_gui(frame, list_of_arguments, shares_proportions) 
    else:
        label_select['text'] = "Number of shares: " + str(shares_number) + "\n" " You selected: " + str(shares_placed)

def choose_number_databases_gui(frame, 
                list_of_arguments, 
                button, label_select,
                isFirebase, isClever, isCosmos, 
                ck_firebase, ck_clever, ck_cosmos):

    shares_number = list_of_arguments[1]
    label_select['text'] = "Number of shares: " + str(shares_number)
    ck_firebase.config(state=tk.DISABLED)
    ck_clever.config(state=tk.DISABLED)
    ck_cosmos.config(state=tk.DISABLED)

    num_firebase = tk.Spinbox(frame, from_=0, to= 0)
    num_clever = tk.Spinbox(frame, from_=0, to= 0)
    num_cosmos = tk.Spinbox(frame, from_=0, to= 0)

    if (isFirebase.get() == 1):
        num_firebase = tk.Spinbox(frame, from_=1, to= shares_number)
        num_firebase.grid(row = 2, column = 2, sticky = W)
    if (isClever.get() == 1):
        num_clever = tk.Spinbox(frame, from_=1, to= shares_number)
        num_clever.grid(row = 3, column = 2, sticky = W)
    if (isCosmos.get() == 1):
        num_cosmos = tk.Spinbox(frame, from_=1, to= shares_number)
        num_cosmos.grid(row = 4, column = 2, sticky = W)
        
    button['text'] = 'Confirm'
    button['command'] =lambda: equal_shares_number(frame, 
                                            list_of_arguments, 
                                            button,  label_select,
                                            num_firebase, num_clever, num_cosmos) 


def choose_databases_gui(frame, list_of_arguments):
    delete_frame(frame)
    frame = tk.Frame(gui)
    frame.pack()

    title = tk.Label(frame, text="Setup databases stage")
    title.configure(font=(20))
    title.grid(row = 0, column = 1, columnspan = 2, sticky = W, pady=30)

    label_select = tk.Label(frame, text = "Select your types of cloud databases: ")
    label_select.grid(row = 1, column = 1, sticky = W, pady=30, padx=10)

    isFirebase = tk.IntVar()
    ck_firebase = tk.Checkbutton(frame, text="Google Firebase", variable=isFirebase)
    ck_firebase.grid(row = 2, column = 1, sticky = W, pady=20, padx=30)

    isClever = tk.IntVar()
    ck_clever = tk.Checkbutton(frame, text="Clever Cloud", variable=isClever)
    ck_clever.grid(row = 3, column = 1, sticky = W, pady=20, padx=30)

    isCosmos = tk.IntVar()
    ck_cosmos = tk.Checkbutton(frame, text="Azure Cosmos", variable=isCosmos)
    ck_cosmos.grid(row = 4, column = 1, sticky = W, pady=20, padx=30)

    button = tk.Button(frame, 
                            text="Confirm databases types",
                            width=25, 
                            command=lambda: choose_number_databases_gui(
                                frame, 
                                list_of_arguments,
                                button, label_select,
                                isFirebase, isClever, isCosmos, 
                                ck_firebase, ck_clever, ck_cosmos))
    button.grid(row = 5, column = 1, sticky = W, pady=15)

def check_shares_number(frame, list_of_arguments): 
    shares = list_of_arguments[1]
    threshold = list_of_arguments[2]
    try:
        check_th_sh(shares, threshold)
    except Exception as error:
        print(repr(error))
        messagebox.showwarning("showwarning", repr(error))
    else:
        choose_databases_gui(frame, list_of_arguments)

def check_threshold(frame, list_of_arguments):
    threshold = list_of_arguments[1]
    try:
        if threshold < 1:
            raise ValueError("The threshold should be higher than 0")
    except Exception as error:
        print(repr(error))
        messagebox.showwarning("showwarning", repr(error))
    else:
        choose_databases_gui(frame, list_of_arguments)            

def reconstruction_input_gui(frame):
    delete_frame(frame)
    frame = tk.Frame(gui)
    frame.pack()

    title = tk.Label(frame, text="Reconstruct input stage")
    title.configure(font=(20))
    title.grid(row = 0, column = 1, columnspan = 2, sticky = W, pady=30)

    label_threshold = tk.Label(frame, text="Input the threshold: ")
    label_threshold.grid(row = 3, column = 0, columnspan = 3, sticky = W, pady=20, padx=30)    

    text_threshold = tk.Entry(frame)
    text_threshold.grid(row = 3, column = 3, sticky = W)

    button = tk.Button(frame, 
                            text='Confirm', 
                            width=25, 
                            command=lambda: check_threshold(frame, 
                                list_of_arguments = [-1, int(text_threshold.get())]
                            ))
    button.grid(row = 4, column = 1, columnspan = 2, sticky = W, pady=15)


def distribution_input_gui(frame):
    delete_frame(frame)
    frame = tk.Frame(gui)
    frame.pack()

    title = tk.Label(frame, text="Input stage")
    title.configure(font=(20))
    title.grid(row = 0, column = 2, columnspan = 2, sticky = W, pady=30)

    label_secret = tk.Label(frame, text="Input the secret: ")
    label_secret.grid(row = 1, column = 0, columnspan = 3, sticky = W, pady=20, padx=30)

    text_secret = tk.Entry(frame)
    text_secret.grid(row = 1, column = 3, sticky = W)

    label_shares = tk.Label(frame, text="Input the number of shares: ")
    label_shares.grid(row = 2, column = 0, columnspan = 3, sticky = W, pady=20, padx=30)    

    text_shares = tk.Entry(frame)
    text_shares.grid(row = 2, column = 3, sticky = W)

    label_threshold = tk.Label(frame, text="Input the threshold: ")
    label_threshold.grid(row = 3, column = 0, columnspan = 3, sticky = W, pady=20, padx=30)    

    text_threshold = tk.Entry(frame)
    text_threshold.grid(row = 3, column = 3, sticky = W)

    button = tk.Button(frame, 
                            text='Confirm', 
                            width=25, 
                            command=lambda: check_shares_number(frame, 
                            [text_secret.get(), int(text_shares.get()), int(text_threshold.get())]
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
                            command=lambda: distribution_input_gui(start_frame))
    button.grid(row = 2, column = 1, sticky = W, pady=15)

    button = tk.Button(start_frame, 
                            text='Reconstruct a secret', 
                            width=25, 
                            command=lambda: reconstruction_input_gui(start_frame))
    button.grid(row = 3, column = 1, sticky = W, pady=15)

def set_input_window():
    gui.geometry("480x520")
    gui.title("Secret Sharing Application")

    icon = tk.PhotoImage(file="./GraphicalUserInterface/s-logo.png")
    gui.iconphoto(True, icon)
    
def show_error(self, *args):
    err = traceback.format_exception(*args)
    print(err)
    messagebox.showerror('Exception', err[-1])

if __name__ == '__main__':
    gui = tk.Tk()
    set_input_window()
    tk.Tk.report_callback_exception = show_error
    start_gui()
    gui.mainloop()