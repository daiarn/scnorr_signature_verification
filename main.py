from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from scnorr_signature import ScnorrSignatureContainer

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
ttk.Label(frame, text="Viešo rakto antraštė:").grid(column=0, row=2)
puk = ttk.Entry(frame)
puk.grid(column=1, row=2)
# puk.insert(0, "PuK")
ttk.Label(frame, text="Žinutės antraštė:").grid(column=0, row=3)
message = ttk.Entry(frame)
message.grid(column=1, row=3)
# message.insert(0, "Enc. Vote Ci")
ttk.Label(frame, text="r antraštė:").grid(column=0, row=4)
r = ttk.Entry(frame)
r.grid(column=1, row=4)
# r.insert(0, "Signature comp.   R")
ttk.Label(frame, text="s antraštė:").grid(column=0, row=5)
s = ttk.Entry(frame)
s.grid(column=1, row=5)
# s.insert(0, "Signature comp.   S")
ttk.Label(frame, text="verifikacijos atsakymo antraštė:").grid(column=0, row=6)
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
        text.insert('end', "Ne visi laukai užpildyti" + '\n')
        return
    if not container.file:
        text.insert('end', "Nepasirinktitas failas" + '\n')

    headers = {
        "public_key": puk.get(),
        "message": message.get(),
        "r": r.get(),
        "s": s.get(),
        "verification": verification.get(),
    }

    container.p = int(p.get())
    container.g = int(g.get())
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
    text='Pasirinkti failą',
    command=open_text_file
).grid(column=0, row=9, sticky='w', padx=10, pady=10)

ttk.Button(frame, text="Tikrinti", command=validation).grid(column=1, row=9)

root.mainloop()
