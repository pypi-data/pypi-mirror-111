# -*- coding: utf-8 -*-
from PyTkGui.widgets import *
from PyTkGui import Component, ComponentStyle, Variable, Eventer


class SB_Button(Component):
    def __init__(self, master, **comp_options):
        super().__init__(master)

        # style
        style = ComponentStyle(self.master)
        style.configure("SB.TButton", **{'background': 'slateblue', 'foreground': 'white'})
        style.map("SB.TButton", **{'background': [('active', 'indigo')]})
        
        # template
        self.root = Button(self.master, style = "SB.TButton", pack = comp_options.pop("pack", {}), **comp_options)
