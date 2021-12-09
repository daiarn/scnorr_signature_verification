import csv
import datetime
import hashlib

from tkinter import *
from tkinter import ttk
from tkinter import filedialog


def h28(text):
    if not type(text) == str:
        text = str(text)
    encoded = text.encode()
    result = hashlib.sha256(encoded).hexdigest()
    return result[-7:].upper()


def hd28(text):
    hex_value = h28(text)
    dec = int(hex_value, 16)
    return dec


class ScnorrSignatureContainer:

    def __init__(self):
        self.file = None
        self.p = 0
        self.g = 0
        self.headers = {}

    def get_results(self):
        try:
            success = self._process_rows()
        except BaseException:
            return "Unexpected error occurred try again or contact developer"
        if success:
            return "File scanned successfully"

    def _process_rows(self):
        if not self.file:
            return False

        reader = csv.DictReader(self.file, delimiter=';')
        result_rows = []
        for row in reader:
            if not self._validate(row):
                if self._is_not_empty_row(row):
                    row[self.headers["verification"]] = False
                result_rows.append(row)
                continue
            r = int(row[self.headers["r"]])
            s = int(row[self.headers["s"]])
            message = row[self.headers["message"]]
            public_key = int(row[self.headers["public_key"]])

            signature = ScnorrSignature(self.p, self.g, public_key)
            result = signature.signature_verification(r, s, message)
            row[self.headers["verification"]] = result
            result_rows.append(row)

        if len(result_rows) > 0:
            self._result_csv(result_rows)
            return True
        return False

    def _validate(self, row):
        return (
                self.headers["r"] in row.keys() and
                self.headers["s"] in row.keys() and
                self.headers["message"] in row.keys() and
                self.headers["public_key"] in row.keys() and
                row[self.headers["r"]] != "" and
                row[self.headers["s"]] != "" and
                row[self.headers["message"]] != "" and
                row[self.headers["public_key"]] != "" and
                row[self.headers["r"]].isdigit() and
                row[self.headers["s"]].isdigit() and
                row[self.headers["public_key"]].isdigit()
        )

    def _is_not_empty_row(self, row):
        return (
            row[self.headers["r"]] != "" or
            row[self.headers["s"]] != "" or
            row[self.headers["message"]] != "" or
            row[self.headers["public_key"]] != ""
        )

    def _result_csv(self, rows):
        filename = f'Verification_{datetime.datetime.now().strftime("%Y_%m_%d_%H%M")}.csv'
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)


class ScnorrSignature:

    def __init__(self, p, g, a):
        self.p = p
        self.g = g
        self.a = a

    def signature_verification(self, r, s, message):
        """g^s = r * a^h mod p"""

        h = hd28(message + str(r))
        g_s = pow(self.g, s, self.p)
        a_h = pow(self.a, h, self.p)
        rah = (r * a_h) % self.p
        return g_s == rah


root = Tk()

root.title("Scnorr Signature verification")
root.geometry("600x600")

frame = ttk.Frame(root, padding=10)
frame.grid()
ttk.Label(frame, text="p:").grid(column=0, row=0)
p = ttk.Entry(frame)
p.grid(column=1, row=0)
# p.insert(0, "264043379")
ttk.Label(frame, text="g:").grid(column=0, row=1)
g = ttk.Entry(frame)
# g.insert(0, "2")
g.grid(column=1, row=1)
ttk.Label(frame, text="Public key header:").grid(column=0, row=2)
puk = ttk.Entry(frame)
puk.grid(column=1, row=2)
# puk.insert(0, "PuK")
ttk.Label(frame, text="Signed message header:").grid(column=0, row=3)
message = ttk.Entry(frame)
message.grid(column=1, row=3)
# message.insert(0, "Enc. Vote Ci")
ttk.Label(frame, text="Signature r-component header:").grid(column=0, row=4)
r = ttk.Entry(frame)
r.grid(column=1, row=4)
# r.insert(0, "Signature comp.   R")
ttk.Label(frame, text="Signature s-component header:").grid(column=0, row=5)
s = ttk.Entry(frame)
s.grid(column=1, row=5)
# s.insert(0, "Signature comp.   S")
ttk.Label(frame, text="Verification result header:").grid(column=0, row=6)
verification = ttk.Entry(frame)
verification.grid(column=1, row=6)
# verification.insert(0, "V")

# Text editor
text = Text(root, height=12, width=70)
text.grid(column=0, row=7)

container = ScnorrSignatureContainer()


def check_inputs():
    return p.get() and g.get() and puk.get() and message.get() and r.get() and s.get() and verification.get()


def validation():
    if not check_inputs():
        text.insert('end', "Not all fields filled" + '\n')
        return
    if not container.file:
        text.insert('end', "Missing file" + '\n')

    headers = {
        "public_key": puk.get(),
        "message": message.get(),
        "r": r.get(),
        "s": s.get(),
        "verification": verification.get(),
    }

    try:
        container.p = int(p.get())
        container.g = int(g.get())
    except ValueError:
        text.insert('end', "p and g values must be integers" + '\n')

    container.headers = headers

    result_message = container.get_results()
    if result_message:
        text.insert('end', result_message + '\n')


def open_text_file():
    # file type
    filetypes = (
        ('csv files', '*.csv'),
        ('All files', '*.*')
    )
    # show the open file dialog
    file = filedialog.askopenfile(filetypes=filetypes)
    container.file = file


# open file button
open_button = ttk.Button(
    frame,
    text='Choose file',
    command=open_text_file
).grid(column=0, row=9, sticky='w', padx=10, pady=10)

ttk.Button(frame, text="Verify", command=validation).grid(column=1, row=9)

root.mainloop()
