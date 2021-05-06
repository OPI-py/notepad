import tkinter as tk


class TextWidget(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        # action for the underlying widget
        self.first = self._w + "first"
        self.tk.call("rename", self._w, self.first)
        self.tk.createcommand(self._w, self.icursor_agent)

    def icursor_agent(self, *args):
        # requested action
        command = (self.first,) + args
        try:
            result = self.tk.call(command)
        except Exception:
            return None

        # generate an event when icursor move or edited
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")):
            self.event_generate("<<IcursorModify>>", when="tail")

        return result 