from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from scnorr_signature import ScnorrSignatureContainer

root = Tk()

root.title("Scnorr Signature verification")
root.geometry("400x600")

frame = ttk.Frame(root, padding=10)
frame.grid()
ttk.Label(frame, text="p:").grid(column=0, row=0)
p = ttk.Entry(frame)
p.grid(column=1, row=0)
ttk.Label(frame, text="g:").grid(column=0, row=1)
g = ttk.Entry(frame)
g.grid(column=1, row=1)
ttk.Label(frame, text="Viešo rakto antraštė:").grid(column=0, row=2)
puk = ttk.Entry(frame)
puk.grid(column=1, row=2)
ttk.Label(frame, text="Žinutės antraštė:").grid(column=0, row=3)
message = ttk.Entry(frame)
message.grid(column=1, row=3)
ttk.Label(frame, text="r antraštė:").grid(column=0, row=4)
r = ttk.Entry(frame)
r.grid(column=1, row=4)
ttk.Label(frame, text="s antraštė:").grid(column=0, row=5)
s = ttk.Entry(frame)
s.grid(column=1, row=5)

# Text editor
text = Text(root, height=12)
text.grid(column=0, row=6)

container = ScnorrSignatureContainer()


def check_inputs():
    return p.get() and g.get() and puk.get() and message.get() and r.get() and s.get()


def validation():
    if not check_inputs():
        text.insert('1.0', "Ne visi laukai užpildyti")
        return

    headers = {
        "public_key": puk.get(),
        "message": message.get(),
        "r": r.get(),
        "s": s.get(),
    }

    container.p = p.get()
    container.g = g.get()
    container.headers = headers

    container.get_results()

    # read the text file and show its content on the Text
    if container.file:
        text.insert('1.0', container.file.readlines())


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
    root,
    text='Open a File',
    command=open_text_file
).grid(column=0, row=7, sticky='w', padx=10, pady=10)

ttk.Button(frame, text="Tikrinti", command=validation).grid(column=0, row=9)
ttk.Button(frame, text="Išeiti", command=root.destroy).grid(column=1, row=9)

root.mainloop()
