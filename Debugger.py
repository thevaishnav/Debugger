from tkinter import *
from tkinter import ttk
import threading
import time
from Chunk import Chunk
from Variables import Variables
from Input import Input


class Debugger(Tk):
    is_debugging = False
    chunks: dict[str: Chunk] = {}
    chunk_count = 0
    __viewing_chunk: Chunk = None

    def __init__(self):
        super(Debugger, self).__init__()
        self.__messages_id: int = 0
        self.title("Debugger")
        self.panned = PanedWindow(bg=Variables.bg, orient=HORIZONTAL)
        self.waiting = False
        self.wait_button = None
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background=Variables.list_bg, foreground=Variables.list_fg, rowheight=25,
                        font=Variables.list_font, fieldbackground=Variables.bg, bd=0)
        style.configure("Treeview.Heading", background=Variables.list_bg, foreground=Variables.list_fg,
                        font=Variables.list_font, bd=0)
        style.map("Treeview", background=[('selected', '#458a5a')])

        frameTX = Frame(self, bg=Variables.bg)
        self.tree_view = ttk.Treeview(self, columns=("Time",))
        self.text = Text(frameTX, state=DISABLED, bg=Variables.bg, fg=Variables.fg, font=Variables.text_font)
        self.menuBar = Frame(frameTX, bg=Variables.bg, height=Variables.menu_height)
        self.__input_frame = Input(self.menuBar)

        self.panned.add(self.tree_view)
        self.panned.add(frameTX)
        self.tree_view.heading("#0", text="Message")
        self.tree_view.heading("#1", text="Time")
        self.tree_view.columnconfigure(0, weight=1)
        self.tree_view.columnconfigure(1, weight=0)

        self.tree_view.bind("<ButtonRelease-1>", self._on_list_item_select)
        self.tree_view.bind("<Any-KeyRelease>", self._on_list_item_select)
        self.text.tag_configure(Variables.callback_tag, foreground="#AAAAAA")
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def __create_input_frame(self):
        pass

    def _insert_text(self, to_insert: str):
        self.text["state"] = NORMAL
        self.text.delete("0.0", END)
        self.text.insert("0.0", to_insert)
        self.text["state"] = DISABLED
        Debugger.__viewing_chunk = None

    def _insert_chuck_to_text(self, chunk: Chunk):
        Debugger.__viewing_chunk = chunk
        self.text["state"] = NORMAL
        self.text.delete("0.0", END)
        self.text.insert("0.0", chunk.__str__() + "\n\n")
        ins_ind = self.text.index(END)
        self.text.insert(END, "---------------------------\nCallback History:\n" + chunk.callback_history)
        self.text.tag_add(Variables.callback_tag, ins_ind, END)
        self.text["state"] = DISABLED

        if chunk._asking_for_input:
            self.__show_input_frame()
        else:
            self.__hide_input_frame()

    def __show_input_frame(self):
        self.__input_frame.pack(side=LEFT, fill=BOTH, expand=1)

    def __hide_input_frame(self):
        self.__input_frame.pack_forget()

    def run(self, main_func: callable):
        threading.Thread(target=main_func).start()

        self.panned.pack(fill=BOTH, expand=1)
        if len(self.chunks) == 0:
            self._insert_text("Details will be shown here")
            self.tree_view.insert("", END, "No debugs")
        self.menuBar.pack(side=TOP, fill=X, expand=0)
        self.text.pack(side=TOP, fill=BOTH, expand=1)
        super().mainloop()

    def wait_for_continue(self):
        self.waiting = True
        self.wait_button = Button(self.menuBar, text="Continue", command=self.__stop_waiting, bg=Variables.bg,
                                  fg=Variables.fg, font=Variables.input_font)
        self.wait_button.pack()
        while self.waiting:
            time.sleep(0.1)

    def take_input(self, label: str, chunk: Chunk) -> str:
        while Debugger.__viewing_chunk != chunk: time.sleep(0.1)

        self.__show_input_frame()
        self.__input_frame.set_label(label)
        while not self.__input_frame.has_user_confirmed: time.sleep(0.1)
        return self.__input_frame.reset_and_hide()

    def pop_chunk(self, chunk: Chunk):
        if chunk.ID in Debugger.chunks:
            Debugger.chunks.pop(chunk.ID)
            self.tree_view.delete(chunk.ID)
            del chunk

    def __stop_waiting(self):
        self.waiting = False
        if self.wait_button: self.wait_button.destroy()

    def _indents(self):
        return "\t" * self.chunk_count

    def Log(self, message: str) -> Chunk:
        if len(self.chunks) == 0: self.tree_view.delete(*self.tree_view.get_children())

        mess_id = f"mes_{self.__messages_id}"
        self.__messages_id += 1
        ch = Chunk(self, mess_id, message)
        self.chunks[mess_id] = ch
        self.tree_view.insert("", END, text=message, values=(ch.log_time,), iid=mess_id)
        self.tree_view.selection_set(mess_id)
        self._insert_chuck_to_text(ch)
        return ch

    def refresh_chunk(self, chunk: Chunk):
        if Debugger.__viewing_chunk == chunk:
            self._insert_chuck_to_text(chunk)

    def _refresh_tree(self):
        self.tree_view.delete(*self.tree_view.get_children())
        for chunk in Debugger.chunks.values():
            self.tree_view.insert("", END, text=chunk.name, values=(chunk.log_time,), iid=chunk.ID)

    def _on_list_item_select(self, event):
        item_id = self.tree_view.focus()
        if item_id:
            try:
                self._insert_chuck_to_text(self.chunks[item_id])
            except KeyError:
                self._insert_text("No Info Found")

    def _on_closing(self):
        self.destroy()
        quit()
