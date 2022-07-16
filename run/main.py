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

        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value='Insert Test String Here ...')
        self.var_5 = tk.DoubleVar(value=75.0)
        self.setup_widgets()

    def setup_widgets(self):
        self.img = tk.PhotoImage(file='gui/locked.png')
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
                                  command=lambda: self.clipboard_copy(self.var_4.get()))
        self.button2.grid(row=7, column=0, padx=5, pady=10, ipadx=1, ipady=5, sticky="nsew")

        # Button
        self.button3 = ttk.Button(self.frame_L, text="Export (as .PDF, .DOCX, or .TXT)",
                                  command=lambda: self.clipboard_copy(self.var_4.get()))
        self.button3.grid(row=8, column=0, padx=5, pady=10, ipadx=1, ipady=5, sticky="nsew")

        # Accentbutton
        self.accentbutton = ttk.Button(
            self.frame_L, text="Import Credentials", style="Accent.TButton", command=lambda: self.ask_openfile()
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

    def ask_openfile(self):
        return filedialog.askopenfile()

    def ask_savefile(self):
        return filedialog.asksaveasfile()

    def clipboard_copy(self, item):
        pyperclip.copy(item)


def load_json(file):
    return json.load(open(file))


def file_write(file, mesg):
    with open(file, 'w') as f:
        f.write(mesg), f.close()


def file_read(file):
    with open(file, 'r') as f:
        data = f.read()
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
    FILE_BLANK = 'bucket/blank.json'
    FILE_DUMP_KEY = f'.ky'
    FILE_DUMP_FILE = f'dump.ky'

    # to_encrypt = '{"name@domain.com": {"account-001": {"account": "Someguy", "password": "321321", "recovery-codes": ["123123-321321"]}'
    # to_encrypt = '{"name":"John", "age":30, "city":"New York"}'

    DISPLAY_DATA = load_json(FILE_BLANK)
    to_encrypt = json.dumps(DISPLAY_DATA)

    key = generate_key()

    enctex = encrypt(to_encrypt, key)
    n1 = enctex.decode('UTF-8')
    file_write(FILE_DUMP_FILE, n1)

    file_data = file_read(FILE_DUMP_FILE)
    n2 = file_data.encode('UTF-8')
    completed = json.loads(decrypt(n2, key))
    DISPLAY_DATA = completed
    start_gui()
