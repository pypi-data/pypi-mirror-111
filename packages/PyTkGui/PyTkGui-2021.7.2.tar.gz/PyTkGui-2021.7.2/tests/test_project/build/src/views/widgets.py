# -*- coding: utf-8 -*-
from PyTkGui.widgets import *
from PyTkGui import Component, ComponentStyle, Variable, Eventer



class Widgets(Component):
    def __init__(self, master, **comp_options):
        super().__init__(master)

        # data
        Variable(self, master, "select_nums", 4)
        Variable(self, master, "table_columns", [1, 2, 3])
        Variable(self, master, "table_rows", [1, 2, 3])

        # template
        self.root = ColumnLayout(self.master, pack = comp_options.pop("pack", {}), **comp_options)
        self.MenuBar_503 = MenuBar(self.root, pack = {})
        self.Menu_107 = Menu(self.MenuBar_503, text = "Menu1", pack = {})
        self.MenuItem_788 = MenuItem(self.Menu_107, text = "SubMenu1", pack = {})
        self.GroupBox_984 = GroupBox(self.root, title = "displays", pack = {'fill': 'both', 'pady': '0 5'})
        self.RowLayout_788 = RowLayout(self.GroupBox_984, pack = {})
        self.Label_845 = Label(self.RowLayout_788, text = "I'm label", pack = {'fill': 'both'})
        self.Image_425 = Image(self.RowLayout_788, source = "/Volumes/Dev/00_ongoing/SHLEE/modules/PyTkGui/tests/test_project/build/src/assets/tcl_tk.png", width = 300, height = 300, pack = {'fill': 'both', 'expand': True})
        self.ProgressBar_797 = ProgressBar(self.RowLayout_788, value = 30, pack = {'fill': 'x'})
        self.GroupBox_550 = GroupBox(self.root, title = "table", pack = {'fill': 'both', 'expand': True})
        self.Table_917 = Table(self.GroupBox_550, editable = True, pack = {})
        self.TableHeader_316 = TableHeader(self.Table_917, pack = {})
        self.TableColumn_108 = TableColumn(self.TableHeader_316, text = "column {idx}", sequence = "idx", iterator = "table_columns", component = self, pack = {})
        self.TableBody_780 = TableBody(self.Table_917, pack = {})
        self.TableRow_614 = TableRow(self.TableBody_780, sequence = "ridx", iterator = "table_rows", component = self, pack = {})
        self.TableItem_997 = TableItem(self.TableRow_614, value = "item {ridx}_{cidx}", sequence = "cidx", iterator = "table_columns", component = self, pack = {})
        self.GroupBox_517 = GroupBox(self.root, title = "controls", pack = {})
        self.ColumnLayout_227 = ColumnLayout(self.GroupBox_517, pack = {})
        self.RowLayout_312 = RowLayout(self.ColumnLayout_227, pack = {'pady': '0 5'})
        self.Input_995 = Input(self.RowLayout_312, text = "I'm input", pack = {})
        self.Range_312 = Range(self.RowLayout_312, value = 70, pack = {})
        self.Select_757 = Select(self.RowLayout_312, index = 0, value = "select item 4", pack = {})
        self.SelectItem_612 = SelectItem(self.Select_757, value = "select item {idx + 1}", sequence = "idx", iterator = "range(select_nums)", component = self, pack = {})
        self.RowLayout_670 = RowLayout(self.ColumnLayout_227, pack = {'pady': '0 5'})
        self.Button_346 = Button(self.RowLayout_670, text = "I'm button {idx + 1}", sequence = "idx", iterator = "range(3)", component = self, pack = {'padx': '0 5'})
        self.Button_554 = Button(self.RowLayout_670, text = "ho!", command = Eventer(self, "incr_cols"), pack = {'padx': '0 5'})
        self.CheckButton_762 = CheckButton(self.RowLayout_670, text = "I'm checkbutton", pack = {})
        self.RowLayout_612 = RowLayout(self.ColumnLayout_227, pack = {})
        self.RadioButton_273 = RadioButton(self.RowLayout_612, text = "radio on", pack = {})
        self.RadioButton_997 = RadioButton(self.RowLayout_612, text = "radio off", pack = {})

    # methods
    def incr_cols(self):
        self.table_columns.append(len(self.table_columns) + 1)

