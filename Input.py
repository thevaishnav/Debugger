from tkinter import *
from Variables import Variables


class Input(Frame):
    def __init__(self, master):
        super(Input, self).__init__(master, bg=Variables.bg, height=Variables.menu_height)
        self.__txt_var = StringVar(self)
        self.__label = Label(self, text="label", bg=Variables.bg, fg=Variables.fg, font=Variables.input_font)
        self.__entry = Entry(self, textvariable=self.__txt_var, bg=Variables.inp_bg, fg=Variables.inp_fg,
                             font=Variables.input_font)
        self.__button = Button(self, text="Continue", bg=Variables.bg, fg=Variables.fg, font=Variables.input_font,
                               command=self.__confirm_input)
        self.__has_user_confirmed = False

        self.__entry.bind("<Return>", self.__confirm_input)
        self.__label.pack(side=LEFT, fill=Y)
        self.__entry.pack(side=LEFT, fill=Y)
        self.__button.pack(side=LEFT, fill=Y)

    def __confirm_input(self, ev=None):
        self.__has_user_confirmed = True

    def set_label(self, label: str):
        self.__label["text"] = label

    @property
    def has_user_confirmed(self):
        return self.__has_user_confirmed

    @property
    def user_input(self):
        return self.__txt_var.get()

    def reset_and_hide(self) -> str:
        self.__has_user_confirmed = False
        tr = self.__txt_var.get()
        self.__txt_var.set("[NOT<->SET]")
        self.pack_forget()
        return tr
