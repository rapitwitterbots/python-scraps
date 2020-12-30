import tkinter as tk
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
import sys
from guessingGame import guessingGame

global selected

def save_file():
    filedialog.asksaveasfile()


def open_file():
    filedialog.askopenfile(mode='r', initialdir="/C:/Users", filetypes=[("all files", "*.*"),
                                                                        ("Python Files", "*.py"), ("Images",
                                                                                                   ["*.jpeg",
                                                                                                    "*.jpg",
                                                                                                    "*.gif",
                                                                                                    "*.png"])])


def save_as_file():
    filedialog.asksaveasfilename()

def cut_text(e, text):
    global selected
    if text.selection_get():
        # grab selected text
        selected = text.selection_get()
        # delete selected text
        text.delete("sel.first", "sel.last")


def copy_text(e, text):
    global selected
    if text.selection_get():
        selected = text.selection_get()
        

def paste_text(e, text):
    if selected:
        position = text.index(INSERT)
        text.insert(position, selected)

def undo_action(e):
    pass

def redo_action(e):
    pass


class BaseWindow:
    padding = {"padx": 10, "pady": 10}
    width = 600
    height = 300
    geometry = str(width) + "x" + str(height)
    about = "This is a little program I made to help me learn how to use the GUI library tkinter in python. It's " \
            "supposed to have several programs and such on it by the end! "
    hotkey_bindings = "F11 - Toggle Full Screen \nESC - Exit Full Screen \nArrow Keys - Scroll"

    def __init__(self, root):
        self.window = root
        self.window.title("Master Program")
        self.window.iconbitmap('')
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)

        """Below I create two frames, one for the menu, one for the container which will house everything else, then I
         place within it a canvas widget. Finally, I create scrollbars within the container frame. 
         Within my canvas I place a frame which will eventually hold all my content and which will be scrollable.
        """

        self.menuframe = Frame(self.window)
        self.container = Frame(self.window)
        self.canvas = Canvas(self.container, width=600, height=300, borderwidth=0, background="#ffffff")
        self.scrolly = Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollx = Scrollbar(self.container, orient="horizontal", command=self.canvas.xview)
        self.content_frame = Frame(self.canvas)

        self.content_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.container.bind(
            "<Configure>",
            self.resize
        )

        """The 'Configure' event triggers whenever the content frame changes size (when we add/remove widgets). Only
        when it changes size do we want to change scrolling properties. The change is 'self.canvas.bbox("all"), which
        gives a 4-value tuple describing the position of two corners of a rectangle, which is the scroll region. The 
        second bind will call the resize function to resize the canvas anytime the window size changes."""

        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrolly.set)
        self.canvas.configure(xscrollcommand=self.scrollx.set)

        """ This tells the canvas to draw the scrollable frame within itself, and positions it at 0,0, anchoring it in
        the top left corner. We then attach the self.scroll object to the canvas widget"""

        self.menuframe.grid(column=0, row=0, sticky=W + E)
        self.container.grid(row=1, column=0, sticky=N + S + E + W)
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)
        self.scrolly.grid(row=0, rowspan=41, column=41, sticky=N + S)
        self.scrollx.grid(row=100, column=0, columnspan=50, sticky=W + E)

        """This simply places all of the aforementioned items within my grid. The code below will construct my menu. I 
        create an overarching menu within which I place four other menus, which "cascade" downwards with their options.
        """

        self.menu = Menu(self.menuframe)

        self.filemenu = Menu(self.menu, tearoff=0)
        self.filemenu.add_command(label="New", command=self.new_file)
        self.filemenu.add_command(label="Open", command=open_file)
        self.filemenu.add_command(label="Save", command=save_file)
        self.filemenu.add_command(label="Save As...", command=save_as_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.window.quit)

        self.editmenu = Menu(self.menu, tearoff=0)
        self.editmenu.add_command(label="Cut", command=lambda: cut_text(False))
        self.editmenu.add_command(label="Copy", command=lambda: copy_text(False))
        self.editmenu.add_command(label="Paste", command=lambda: paste_text(False))
        self.editmenu.add_command(label="Undo", command=lambda: undo_action())
        self.editmenu.add_command(label="Redo", command=lambda: redo_action())

        self.viewmenu = Menu(self.menu, tearoff=0)
        self.viewmenu.add_command(label="Toggle Fullscreen", command=self.toggle_full_screen)

        self.helpmenu = Menu(self.menu, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.message_window)
        self.helpmenu.add_command(label="Hotkey Bindings", command=lambda: BaseWindow.message_window(self,
                                                                                                     BaseWindow.hotkey_bindings))

        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.menu.add_cascade(label="Edit", menu=self.editmenu)
        self.menu.add_cascade(label="View", menu=self.viewmenu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.window.config(menu=self.menu)

        '''These are the keybindings for this particular window'''
        self.window.bind("<F11>", self.toggle_full_screen)
        self.window.bind("<Escape>", self.quit_full_screen)
        self.window.bind("<Left>", lambda event: self.canvas.xview_scroll(-1, "units"))
        self.window.bind("<Right>", lambda event: self.canvas.xview_scroll(1, "units"))
        self.window.bind("<Up>", lambda event: self.canvas.yview_scroll(-1, "units"))
        self.window.bind("<Down>", lambda event: self.canvas.yview_scroll(1, "units"))

    def message_window(self, mess=about):
        self.new_window = Toplevel(self.window)
        self.mess_window = Message(self.new_window, BaseWindow.padding, text=mess, font=20)
        self.mess_window.pack()

    def new_file(self):
        self.new_window = Toplevel(self.window)
        self.textbox = Text(master=self.new_window)
        self.textbox.pack()

    def toggle_full_screen(self):
        if self.window.attributes("-fullscreen") == 0:
            self.window.attributes("-fullscreen", True)
        else:
            self.window.attributes("-fullscreen", False)

    def quit_full_screen(self):
        self.window.attributes("-fullscreen", False)

    def resize(self, event):
        pass


class IORedirector:
    '''a general class for redirecting I/O to this Text widget'''
    def __init__(self, text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    '''class for redirecting stdout to this Text widget'''
    def write(self, str):
        self.text_area.write(str, False)


class MainPage(BaseWindow):  # takes basewindow and builds on top of it
    def __init__(self, root):
        super().__init__(root)

        self.greet = Label(self.content_frame, text="Welcome! Click any of the buttons below to launch their function!")
        self.guessbut = Button(self.content_frame, text="Guessing Game",
                               command=guessingGame)
        sys.stdout = StdoutRedirector(messagebox)
        for i in range(10):
            self.button = Button(self.content_frame, text="Filler")
            self.button.grid(BaseWindow.padding, row=i + 3, column=1)
        '''self.trackbut = Button(self.content_frame, text="Keystroke Tracker", command=keystroke_tracker)
        self.websearchbut = Button(self.content_frame, text="Search the Web", command=websearch)'''

        self.greet.grid(column=2, row=0)
        self.guessbut.grid(BaseWindow.padding, row=1, column=1)
        '''self.trackbut.grid(BaseWindow.padding, row=1, column=2)
        self.websearchbut.grid(BaseWindow.padding, row=1, column=3)'''


def main():
    root = tk.Tk()
    gui = MainPage(root)
    root.mainloop()


if __name__ == "__main__":
    main()
