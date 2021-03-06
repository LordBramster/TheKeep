import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import yaml
from cryptography.fernet import Fernet
import pyperclip
import random
import time


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.parent = parent

        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.var_enter_username = tk.StringVar(value='Account Name')
        self.var_enter_password = tk.StringVar(value='')
        self.var_new_username = tk.StringVar(value='')
        self.var_new_password = tk.StringVar(value='')
        self.var_new_password_confirm = tk.StringVar(value='')
        self.var_progressbar = tk.DoubleVar(value=0.0)

        self.setup_start_windows()

    def setup_start_windows(self):
        self.setup_login()
        # self.setup_main_menu()
        # self.setup_new_window()

    def setup_next_window(self, name):
        self.clear_frame(self)
        if name == 'MAIN': self.setup_main_menu()
        if name == 'LOGIN': self.setup_login()
        if name == 'VIEW': self.setup_viewer()

    def setup_next_created(self, name):
        self.new_window.destroy()
        generate_uid(UID_STR, UID_DIR)
        self.setup_next_window(name)

    def setup_create_account(self):
        self.new_window = tk.Toplevel(self.parent)
        # new_window.geometry("500x500")
        self.new_window.iconbitmap("gui/locked.ico")
        self.new_window.title("Sign Up")

        frame_root = ttk.LabelFrame(self.new_window, padding=(0, 0, 0, 10))
        frame_root.grid(row=0, column=0, padx=(30, 30), pady=(20, 50), sticky="nsew", rowspan=3)
        frame_root.columnconfigure(index=0, weight=1)

        label = ttk.Label(
            frame_root,
            text="Sign Up",
            justify="center",
            font=("-size", 30, "-weight", "bold"))
        label.grid(row=1, column=0, pady=10, columnspan=2)

        frame_account = ttk.LabelFrame(frame_root, padding=(0, 0, 0, 0))
        frame_account.grid(row=10, column=0, padx=(1, 1), pady=(5, 5), sticky="nsew", rowspan=3)
        frame_account.columnconfigure(index=0, weight=1)

        label_account = ttk.Label(
            frame_account,
            text="Enter account name :",
            justify="left",
            font=("-size", 8, "-weight", "bold"))
        label_account.grid(row=0, column=0, pady=10, columnspan=2, sticky="w")

        entry_name = ttk.Entry(frame_account)
        entry_name.insert(0, self.var_new_username.get())
        entry_name.grid(row=1, column=0, padx=(1, 1), pady=(1, 1), ipady=10, ipadx=60, sticky="ew")

        frame_pass = ttk.LabelFrame(frame_root, padding=(0, 0, 0, 0))
        frame_pass.grid(row=20, column=0, padx=(1, 1), pady=(5, 5), sticky="nsew", rowspan=3)
        frame_pass.columnconfigure(index=0, weight=1)

        label_pass = ttk.Label(
            frame_pass,
            text="Enter a password :",
            justify="left",
            font=("-size", 8, "-weight", "bold"))
        label_pass.grid(row=0, column=0, pady=10, columnspan=2, sticky="w")

        entry_pass = ttk.Entry(frame_pass, show='*')
        entry_pass.insert(0, self.var_new_password.get())
        entry_pass.grid(row=1, column=0, padx=(1, 1), pady=(1, 1), ipady=10, ipadx=60, sticky="ew")

        frame_confirm = ttk.LabelFrame(frame_root, padding=(0, 0, 0, 0))
        frame_confirm.grid(row=30, column=0, padx=(1, 1), pady=(5, 5), sticky="nsew", rowspan=3)
        frame_confirm.columnconfigure(index=0, weight=1)

        label_confirm = ttk.Label(
            frame_confirm,
            text="Re-enter your password :",
            justify="left",
            font=("-size", 8, "-weight", "bold"))
        label_confirm.grid(row=0, column=0, pady=10, columnspan=2, sticky="w")

        entry_pass_confirm = ttk.Entry(frame_confirm, show='*')
        entry_pass_confirm.insert(0, self.var_new_password_confirm.get())
        entry_pass_confirm.grid(row=1, column=0, padx=(1, 1), pady=(1, 1), ipady=10, ipadx=60, sticky="ew")

        button = ttk.Button(frame_root, text="Create Account",
                            style="Accent.TButton",
                            command=lambda: self.setup_next_created('MAIN'))
        button.grid(row=40, column=0, padx=(1, 1), pady=(10, 1), ipady=10, ipadx=30, sticky="ew")

    def setup_login(self):
        frame_root = ttk.LabelFrame(self, padding=(0, 0, 0, 10))
        frame_root.grid(row=0, column=0, padx=(30, 30), pady=(50, 50), sticky="nsew", rowspan=3)
        frame_root.columnconfigure(index=0, weight=1)

        self.img = tk.PhotoImage(file='gui/locked_002.png')
        img_b = tk.Label(frame_root, image=self.img)
        img_b.grid(row=1, column=0, padx=(40, 40), pady=(10, 10), sticky="ew")

        label = ttk.Label(
            frame_root,
            text="Locker",
            justify="center",
            font=("-size", 30, "-weight", "bold"))
        label.grid(row=2, column=0, pady=10, columnspan=2)

        label2 = ttk.Label(
            frame_root,
            text="A simple and secure way, to manage passwords.",
            justify="center",
            font=("-size", 8, "-weight", "normal"))
        label2.grid(row=3, column=0, pady=(10, 1), padx=(1, 1), columnspan=2)

        entry_name = ttk.Entry(frame_root)
        entry_name.insert(0, self.var_enter_username.get())
        entry_name.grid(row=4, column=0, padx=(1, 1), pady=(10, 1), ipady=10, ipadx=40, sticky="ew")

        entry_pass = ttk.Entry(frame_root, show='*')
        entry_pass.insert(0, self.var_enter_password.get())
        entry_pass.grid(row=5, column=0, padx=(1, 1), pady=(10, 1), ipady=10, ipadx=40, sticky="ew")

        button = ttk.Button(frame_root, text="Sign In",
                            style="Accent.TButton",
                            command=lambda: self.setup_next_window('MAIN'))
        button.grid(row=6, column=0, padx=(1, 1), pady=(30, 1), ipady=10, ipadx=40, sticky="ew")

        label3 = ttk.Label(
            frame_root,
            text="or",
            justify="center",
            font=("-size", 8, "-weight", "normal"))
        label3.grid(row=7, column=0, pady=(10, 10), padx=(1, 1), columnspan=2)

        button = ttk.Button(frame_root, text="Create Account",
                            # style="Accent.TButton",
                            command=lambda: self.setup_create_account())
        button.grid(row=8, column=0, padx=(1, 1), pady=(1, 1), ipady=10, ipadx=20, sticky="ew")

        """     
        progressbar = ttk.Progressbar(frame_root, value=0, variable=self.var_progressbar, mode="determinate")
        progressbar.grid(row=10, column=0, padx=(10, 20), pady=(20, 0), sticky="ew")
        """

    def setup_viewer(self):
        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=(20, 5))
        self.paned.add(self.pane_1, weight=1)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.pane_1)
        self.scrollbar.pack(side="right", fill="y")

        # Treeview
        self.treeview = ttk.Treeview(
            self.pane_1,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
            columns=(1, 2, 3),
            height=10)
        self.treeview.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.treeview.yview)

        # Treeview columns
        self.treeview.column("#0", anchor="w", width=300)
        self.treeview.column(1, anchor="w", width=250)
        self.treeview.column(2, anchor="w", width=200)
        self.treeview.column(3, anchor="w", width=100)

        # Treeview headings
        self.treeview.heading("#0", text="Email / Account", anchor="center")
        self.treeview.heading(1, text="Username", anchor="center")
        self.treeview.heading(2, text="Password", anchor="center")
        self.treeview.heading(3, text="2FA-Recovery", anchor="center")

        # Define treeview users
        treeview_data = []
        p = 0
        for parent, value1 in DISPLAY_DATA.items():
            p += 1
            treeview_data.append(
                ("", p, parent, ('', '', ''))
            )
            c = p
            for child, value2 in value1.items():
                c += 1
                treeview_data.append(
                    (p, c, child, (value2['account'], value2['password'], value2['recovery-codes']))
                )
            p = c

        # Insert treeview users
        for item in treeview_data:
            self.treeview.insert(
                parent=item[0], index="end", iid=item[1], text=item[2], values=item[3]
            )
            if item[0] == "" or item[1] in {8, 21}:
                self.treeview.item(item[1], open=True)  # Open parents

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

    def setup_main_menu(self):
        self.img = tk.PhotoImage(file='gui/locked_003.png')
        self.img_b = tk.Label(self, image=self.img)
        self.img_b.grid(row=0, column=0, padx=(40, 40), pady=(20, 10), sticky="ew")

        self.frame_L = ttk.LabelFrame(self, padding=(0, 0, 0, 10))
        self.frame_L.grid(
            row=1, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
        self.frame_L.columnconfigure(index=0, weight=1)

        # Button
        self.button = ttk.Button(self.frame_L, text="Edit Credentials")
        self.button.grid(row=6, column=0, padx=5, pady=10, ipadx=5, ipady=10, sticky="nsew")

        # Button
        self.button2 = ttk.Button(self.frame_L, text="Copy Credentials")
        self.button2.grid(row=7, column=0, padx=5, pady=10, ipadx=5, ipady=10, sticky="nsew")

        # Button
        self.button3 = ttk.Button(self.frame_L, text="Export (as .PDF, .DOCX, or .TXT)")
        self.button3.grid(row=8, column=0, padx=5, pady=10, ipadx=5, ipady=10, sticky="nsew")

        # Accentbutton
        self.accentbutton = ttk.Button(
            self.frame_L, text="Import Credentials", style="Accent.TButton", command=lambda: ask_openfile())
        self.accentbutton.grid(row=9, column=0, padx=5, pady=10, ipadx=5, ipady=10, sticky="nsew")

        # Accentbutton
        self.accentbutton2 = ttk.Button(
            self.frame_L, text="Add New Credentials", style="Accent.TButton")
        self.accentbutton2.grid(row=10, column=0, padx=5, pady=10, ipadx=5, ipady=10, sticky="nsew")

    def click_callback(self, event, widget):
        widget.delete(0, "end")
        return None

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def progressbar_increase(self, number=15):
        self.var_progressbar.set(self.var_progressbar.get() + number)


def clipboard_copy(item):
    pyperclip.copy(item)


def ask_openfile(file_types):
    return filedialog.askopenfilename(filetypes=file_types)


def ask_savefile():
    return filedialog.asksaveasfile()


def load_json(file):
    return json.load(open(file))


def file_write(file, mesg, per='w'):
    with open(file, per) as f:
        f.write(mesg), f.close()


def file_read(file):
    with open(file, 'r') as f:
        data = f.read()
    return data


def file_reads(file):
    with open(file, 'r') as f:
        data = f.readlines()
    return data


def folder_content(path):
    return os.listdir(path)


def encrypt(string, key):
    return Fernet(key).encrypt(string.encode())


def decrypt(string, key):
    return Fernet(key).decrypt(string).decode()


def generate_key():
    return Fernet.generate_key()


def generate_uid(prefix, uid_dir):
    new_uid = f'{prefix}{random.randrange(0, 99999999)}'
    return new_uid if new_uid not in folder_content(uid_dir) else None


def start_gui():
    root = tk.Tk()
    root.iconbitmap("gui/locked.ico")
    root.title("Login")
    root.tk.call("source", "sun-valley.tcl")
    root.tk.call("set_theme", "dark")
    app = App(root)
    app.pack(fill="both", expand=True)
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.geometry("+{}+{}".format(int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2)),
                                  int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))))
    root.mainloop()


def get_data_from(dump_file, key_file):
    # CHECK FILES DO EXIST
    if not os.path.exists(dump_file):
        FILE_DUMP_FILE = ask_openfile(FILES_ACCEPT)
    if not os.path.exists(key_file):
        FILE_DUMP_KEY = ask_openfile(FILES_ACCEPT)

    # GET KEY
    key_retrieved = file_read(key_file)
    print(f'GET KEY -> {key_retrieved}')

    # DECRYPT JSON
    data_retrieved = file_read(dump_file)
    dump_data = json.loads(decrypt(data_retrieved.encode('UTF-8'), key_retrieved))

    return dump_data


def push_data_to(from_data, dump_file, key_file):
    # KEY GENERATION
    key_generated = generate_key()
    file_write(key_file, key_generated.decode('UTF-8'))
    print(f'NEW KEY -> {key_generated}')

    # ENCRYPT DICT
    encrypted_with_key = encrypt(json.dumps(from_data), key_generated)
    file_write(dump_file, encrypted_with_key.decode('UTF-8'))


if __name__ == "__main__":
    FILES_ACCEPT = [('Custom Files', '*.ky')]
    FILE_BLANK = 'bucket/JSON/blank.json'
    FILE_DUMP_KEY = f'bucket/users/k_dump.ky'
    FILE_DUMP_FILE = f'bucket/users/j_dump.ky'
    DISPLAY_DATA = get_data_from(FILE_DUMP_FILE, FILE_DUMP_KEY)
    # SET_BLANK_DATA = load_json(FILE_BLANK)
    UID_ACTIVE = None
    UID_STR = 'uid-'
    UID_DIR = './bucket/users/'

    # START GUI
    start_gui()
