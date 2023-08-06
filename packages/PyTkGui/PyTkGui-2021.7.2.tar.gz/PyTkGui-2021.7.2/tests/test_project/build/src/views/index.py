# -*- coding: utf-8 -*-
from PyTkGui.widgets import *
from PyTkGui import Component, ComponentStyle, Variable, Eventer
from ..components.SB_Button import SB_Button


class Index(Component):
    def __init__(self, master, **comp_options):
        super().__init__(master)

        # data
        Variable(self, master, "count", 0)
        Variable(self, master, "content", "clicked 0 times!")

        # template
        self.root = ColumnLayout(self.master, pack = comp_options.pop("pack", {}), **comp_options)
        self.Label_300 = Label(self.root, text = "less than 5", cond = "count < 5", component = self, pack = {'fill': 'both'})
        self.Label_490 = Label(self.root, variable = self.content_var, anchor = "center", pack = {'fill': 'both', 'expand': True})
        self.RowLayout_323 = RowLayout(self.root, pack = {'fill': 'x'})
        self.SB_Button_408 = SB_Button(self.RowLayout_323, text = "up", command = Eventer(self, "count_up"), pack = {'fill': 'both', 'expand': True, 'padx': '0 5'})
        self.SB_Button_620 = SB_Button(self.RowLayout_323, text = "down", command = Eventer(self, "count_down"), pack = {'fill': 'both', 'expand': True})

    # methods
    def count_up(self):
        self.count += 1
        self.content = f"clicked {self.count} times!"

    def count_down(self):
        if self.count > 0:
            self.count -= 1
            self.content = f"clicked {self.count} times!"

