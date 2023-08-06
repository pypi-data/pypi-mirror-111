# -*- coding: utf-8 -*-
from PyTkGui.widgets import *
from PyTkGui import Component, ComponentStyle, Variable, Eventer


class App(Component):
    def __init__(self, master, **comp_options):
        super().__init__(master)

        # template
        self.root = ColumnLayout(self.master, pack = comp_options.pop("pack", {}), **comp_options)
        self.RowLayout_786 = RowLayout(self.root, pack = {'fill': 'x'})
        self.RouterLink_808 = RouterLink(self.RowLayout_786, self, to = "/", text = "Index", pack = {})
        self.Separator_891 = Separator(self.RowLayout_786, orient = "vertical", pack = {'padx': 5})
        self.RouterLink_266 = RouterLink(self.RowLayout_786, self, to = "/Widgets", text = "Widgets", pack = {})
        self.Separator_566 = Separator(self.root, pack = {'fill': 'x'})
        self.router_view = RouterView(self.root, self.master)
