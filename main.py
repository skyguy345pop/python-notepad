from tkinter import Button, Text, StringVar, IntVar, Frame, Tk, PhotoImage, RAISED, END, colorchooser, Label
from tkinter.ttk import Combobox
from tkinter.font import families, Font
from tkinter.filedialog import askopenfilename, asksaveasfilename
from os import startfile
from PIL import ImageGrab, ImageTk

bold_on = False
italic_on = False
bold = "normal"
italic = "roman"
underline = False

def pick_colour(text_edit, font_colour_icon):
    colour = colorchooser.askcolor()[1]
    if colour:
        font_colour_icon.config(foreground = colour)
        text_edit.config(foreground = colour)

def add_image(text_edit):
    img = ImageGrab.grabclipboard()
    if img is not None:
        img = ImageTk.PhotoImage(img)
        text_edit.image_create("insert", image = img)
        if not hasattr(text_edit, "images"):
            text_edit.images = []
        text_edit.images.append(img)

def save(window, text_edit):
    filepath = asksaveasfilename(filetypes=[("Text Files", "*.docx"), ("Text Files", "*.txt"), ("Text Files", "*.doc")])
    if not filepath:
        return
    
    with open(filepath, "w") as f:
        content = text_edit.get(1.0, END)
        f.write(content)
    window.title(f"OpenFile: {filepath}")

def open_file(window, text_edit):
    filepath = askopenfilename(filetypes=[("Text Files","*.docx"), ("Text Files", "*.txt"), ("Text Files", "*.doc")])
    if not filepath:
        return
    
    text_edit.delete(1.0, END)
    with open(filepath, "r") as f:
        content = f.read()
        text_edit.insert(END, content)
    window.title(f"OpenFile: {filepath}")

def print_file():
    filepath = askopenfilename(filetypes=[("Text Files","*.docx"), ("Text Files", "*.txt"), ("Text Files", "*.doc")])
    if not filepath:
        return
    startfile(filepath, "print")

def main():
    sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
    def Text_changed(index, value, op):
        global bold
        global italic
        global underline
        font = Font(family = font_menu.get(), size = size_menu.get(), underline=underline, slant=italic, weight=bold)
        text_edit.configure(font=font)
    def Text_changed_button(button):
        global bold_on
        global italic_on
        global bold
        global italic
        global underline
        if button == "bold" and not bold_on:
            bold = "bold"
            bold_on = True
        elif button == "bold" and bold_on:
            bold = "normal"
            bold_on = False
        elif button == "italic" and not italic_on:
            italic = "italic"
            italic_on = True
        elif button == "italic" and italic_on:
            italic = "roman"
            italic_on = False
        elif button == "underline" and not underline:
            underline = True
        elif button == "underline" and underline:
            underline = False
        font = Font(family = font_menu.get(), size = size_menu.get(), underline=underline, slant=italic, weight=bold)
        text_edit.configure(font=font)
    
    window = Tk()
    Bold_Icon = PhotoImage(file = "icons\\Bold.png")
    Bold_Icon = Bold_Icon.subsample(8, 8)
    italic_icon = PhotoImage(file = "icons\\Italic.png")
    italic_icon = italic_icon.subsample(8, 8)
    underline_icon = PhotoImage(file = "icons\\Underline.png")
    underline_icon = underline_icon.subsample(8, 8)
    window.title("Text Editor")
    window.rowconfigure(0, minsize=400)
    window.columnconfigure(1, minsize=500)
    fonts = families()
    font = StringVar(value="calibrii")
    size = IntVar(value=18)

    frame = Frame(window, relief=RAISED, bd = 2)

    text_edit = Text(window, font=(f"{font} {size.get()}"))
    text_edit.grid(row=0, column=1)
    save_button = Button(frame, text = "Save", command = lambda: save(window, text_edit))
    open_button = Button(frame, text = "Open", command = lambda: open_file(window, text_edit))
    print_button = Button(frame, text = "Print", command = lambda: print_file())
    font_colour_button = Button(frame, text="A", font=("calibrii", 30), command = lambda: pick_colour(text_edit, font_colour_button))
    bold_button = Button(frame, text="Bold", image = Bold_Icon, command = lambda: Text_changed_button("bold"))
    italic_button = Button(frame, text="italic", image = italic_icon, command = lambda: Text_changed_button("italic"))
    underline_button = Button(frame, text="underline", image = underline_icon, command = lambda: Text_changed_button("underline"))
    font_menu = Combobox(frame, textvariable=font, state="readonly", values = fonts)
    size_menu = Combobox(frame, textvariable=size, values = sizes)

    save_button.grid(row = 0, column = 0, padx=5, pady=5, sticky = "ew")
    open_button.grid(row = 0, column = 1, padx=5, sticky = "ew")
    print_button.grid(row = 0, column = 2, padx=5, sticky = "ew")
    bold_button.grid(row = 1, column = 1, padx=5, sticky = "ew")
    italic_button.grid(row = 1, column = 2, padx=5, sticky = "ew")
    underline_button.grid(row = 1, column = 3, padx=5, sticky = "ew")
    font_colour_button.grid(row = 2, column = 1, padx=5, sticky = "ew")
    font_menu.grid(row = 1, column = 0, pady=(0, 0))
    size_menu.grid(row = 1, column = 0, pady=(50, 0))
    frame.grid(row = 0, column = 0, pady=(50, 50), sticky="ns")
    font.trace("w", Text_changed)
    size.trace("w", Text_changed)

    window.bind("<Control-s>", lambda x: save(window, text_edit))
    window.bind("<Control-o>", lambda x: open_file(window, text_edit))
    window.bind("<Control-p>", lambda x: print_file())
    window.bind("<Control-v>", lambda x: add_image(text_edit))
    window.bind("<Control-b>", lambda x: Text_changed_button("bold"))
    window.bind("<Control-i>", lambda x: Text_changed_button("italic"))
    window.bind("<Control-u>", lambda x: Text_changed_button("underline"))

    window.mainloop()

main()