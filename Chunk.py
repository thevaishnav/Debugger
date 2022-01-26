import inspect
import os
import datetime


class Chunk:
    def __init__(self, dbg, _ID, name):
        self._info = []
        self.callback_history = _get_callback_history()
        self.dbg = dbg
        self._ID = _ID
        self._name = name
        self._asking_for_input = False
        now = datetime.datetime.now()
        self._log_time = f"{now.hour}:{now.minute}:{now.second}"

    @property
    def ID(self):
        return self._ID

    @property
    def name(self):
        return self._name

    @property
    def log_time(self):
        return self._log_time

    def add_line(self, line: str):
        self._info.append(line)
        self.dbg.refresh_chunk(self)

    def pop_line(self, index=-1):
        if len(self._info) >= 1:
            self._info.pop(index)
            self.dbg.refresh_chunk(self)

    def pop_charas(self, character_count: int = 1):
        if len(self._info) >= 1 and len(self._info[-1]) > character_count:
            ll = self._info.pop()
            ll = ll[:len(ll) - character_count]
            self._info.append(ll)
            self.dbg.refresh_chunk(self)

    def append(self, text: str):
        self._info[-1] += text
        self.dbg.refresh_chunk(self)

    def input(self, label: str = ""):
        self._asking_for_input = True
        usr_inp = self.dbg.take_input(label, self)
        self._asking_for_input = False
        self.add_line(f">> {usr_inp}")
        return usr_inp

    def __str__(self):
        return "\n".join(self._info)


def _get_callback_history():
    stacks = []
    t1_max = -1
    t2_max = -1
    t3_max = -1

    for s in inspect.stack()[3:]:
        try:
            the_class = s[0].f_locals["self"].__class__.__name__ + "."
        except KeyError:
            the_class = ""
        the_method = s[0].f_code.co_name
        t1 = str(s.lineno)
        t2 = f"{the_class}{the_method}"
        t3 = os.path.basename(s[1])
        if len(t1) > t1_max: t1_max = len(t1)
        if len(t2) > t2_max: t2_max = len(t2)
        if len(t3) > t3_max: t3_max = len(t3)
        stacks.append((t1, t2, t3))

    t1_max += 5
    t2_max += 5
    t3_max += 5
    return "  Line" + " " * (t1_max - 4) + "function" + " " * (t2_max - 8) + "File" + " " * (t3_max - 4) + "\n  " \
           + "".join(
        t1 + " " * (t1_max - len(t1))
        + t2 + " " * (t2_max - len(t2))
        + t3 + " " * (t3_max - len(t3)) + "\n  "
        for t1, t2, t3 in stacks
    )
