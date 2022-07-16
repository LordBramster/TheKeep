import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
from cryptography.fernet import Fernet
import pyperclip
import ast


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.parent = parent

        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value='Copied String !')
        self.var_5 = tk.DoubleVar(value=75.0)
        self.setup_windows()

    def setup_windows(self):
        self.setup_login()
        # self.setup_main_menu()
        # self.setup_new_window()

    def setup_new_window(self):
        new_window = tk.Toplevel(self.parent)
        new_window.geometry("500x500")
        new_window.iconbitmap("gui/locked.ico")
        new_window.title("New Window")

    def setup_login(self):
        self.img = tk.PhotoImage(file='gui/locked_003.png')
        img_b = tk.Label(self, image=self.img)
        img_b.grid(row=0, column=0, padx=(40, 40), pady=(20, 10), sticky="ew")

        frame_root = ttk.Frame(self, padding=(0, 0, 0, 10))
        frame_root.grid(row=1, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
        frame_root.columnconfigure(index=0, weight=1)

        button = ttk.Button(frame_root, text="Login")
        button.grid(row=6, column=0, padx=5, pady=10, ipadx=1, ipady=5, sticky="nsew")

    def setup_main_menu(self):
        self.img = tk.PhotoImage(file='gui/locked_003.png')
        self.img_b = tk.Label(self, image=self.img)
        self.img_b.grid(row=0, column=0, padx=(40, 40), pady=(20, 10), sticky="ew")

        self.frame_L = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.frame_L.grid(
            row=1, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.frame_L.columnconfigure(index=0, weight=1)

        # Button
        self.button = ttk.Button(self.frame_L, text="Edit Credentials")
        self.button.grid(row=6, column=0, padx=5, pady=10, ipadx=1, ipady=5, sticky="nsew")

        # Button
        self.button2 = ttk.Button(self.frame_L, text="Copy Credentials",
                                  command=lambda: clipboard_copy(self.var_4.get()))
        self.button2.grid(row=7, column=0, padx=5, pady=10, ipadx=1, ipady=5, sticky="nsew")

        # Button
        self.button3 = ttk.Button(self.frame_L, text="Export (as .PDF, .DOCX, or .TXT)",
                                  command=lambda: self.openNewWindow())
        self.button3.grid(row=8, column=0, padx=5, pady=10, ipadx=1, ipady=5, sticky="nsew")

        # Accentbutton
        self.accentbutton = ttk.Button(
            self.frame_L, text="Import Credentials", style="Accent.TButton", command=lambda: ask_openfile()
        )
        self.accentbutton.grid(row=9, column=0, padx=5, pady=10, ipadx=1, ipady=5, sticky="nsew")

        # Accentbutton
        self.accentbutton2 = ttk.Button(
            self.frame_L, text="Add New Credentials", style="Accent.TButton"
        )
        self.accentbutton2.grid(row=10, column=0, padx=5, pady=10, ipadx=1, ipady=5, sticky="nsew")

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
            height=10,
        )
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

        # Define treeview data
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

        # Insert treeview data
        for item in treeview_data:
            self.treeview.insert(
                parent=item[0], index="end", iid=item[1], text=item[2], values=item[3]
            )
            if item[0] == "" or item[1] in {8, 21}:
                self.treeview.item(item[1], open=True)  # Open parents

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))


def clipboard_copy(self, item):
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


def encrypt(string, key):
    return Fernet(key).encrypt(string.encode())


def decrypt(string, key):
    return Fernet(key).decrypt(string).decode()


def generate_key():
    return Fernet.generate_key()


def start_gui():
    root = tk.Tk()
    root.iconbitmap("gui/locked.ico")
    root.title("Locker")
    root.tk.call("source", "sun-valley.tcl")
    root.tk.call("set_theme", "dark")
    app = App(root)
    app.pack(fill="both", expand=True)
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.geometry("+{}+{}".format(int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2)),
                                  int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))))
    root.mainloop()


if __name__ == "__main__":
    FILES_ACCEPT = [('Custom Files', '*.ky')]
    FILE_BLANK = 'bucket/JSON/blank.json'
    FILE_DUMP_KEY = f'bucket/data/k_dump.ky'
    FILE_DUMP_FILE = f'bucket/data/j_dump.ky'
    # SET_BLANK_DATA = load_json(FILE_BLANK)

    # CHECK FILES DO EXIST
    if not os.path.exists(FILE_DUMP_FILE):
        FILE_DUMP_FILE = ask_openfile(FILES_ACCEPT)
    if not os.path.exists(FILE_DUMP_KEY):
        FILE_DUMP_KEY = ask_openfile(FILES_ACCEPT)

    # GET KEY
    key_retrieved = file_read(FILE_DUMP_KEY)

    # DECRYPT JSON
    data_retrieved = file_read(FILE_DUMP_FILE)
    DISPLAY_DATA = json.loads(decrypt(data_retrieved.encode('UTF-8'), key_retrieved))

    # KEY GENERATION
    key_generated = generate_key()
    file_write(FILE_DUMP_KEY, key_generated.decode('UTF-8'))

    # ENCRYPT DICT
    encrypted_with_key = encrypt(json.dumps(DISPLAY_DATA), key_generated)
    file_write(FILE_DUMP_FILE, encrypted_with_key.decode('UTF-8'))

    print(f'GET KEY -> {key_retrieved}')
    print(f'NEW KEY -> {key_generated}')

    # START GUI
    start_gui()
