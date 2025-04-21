from tkinter import Toplevel, Label, Entry, Button, Frame
import tkinter as tk
from tkinter import ttk

from views.dialog_mark import MarkDialog


class SchemeDialog(Toplevel):
    def __init__(self, parent, root, db_service, schema_id):
        super().__init__(parent)
        self.parent = parent
        self.root = root
        self.db_service = db_service
        self.schema_id = schema_id
        self.setup_ui()

    def setup_ui(self):
        self.title("Редактировать метки на схеме")
        self.geometry("1200x1000")
        self.resizable(True, True)
        self.wm_minsize(1200, 1000)
        self.grab_set()

        form_frame = Frame(self, padx=10, pady=10)
        form_frame.pack(fill="both", expand=True)

        self.paned_window = tk.PanedWindow(form_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.create_left_panel()
        self.create_right_panel()
        self.fill_list_marks()

    def create_left_panel(self):
        self.left_panel = ttk.Frame(self.paned_window, width=200)
        self.paned_window.add(self.left_panel, minsize=200)

        self.tree_frame = ttk.Frame(self.left_panel)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.marks_list = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="browse",
                                       columns=("id", "name", "description"), show="headings")
        self.marks_list.pack(fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.marks_list.yview)

        # Настройка колонок
        self.marks_list.heading("id", text="ID", anchor=tk.W)
        self.marks_list.heading("name", text="Название", anchor=tk.W)
        self.marks_list.heading("description", text="Описание", anchor=tk.W)
        self.marks_list.column("id", width=0, stretch=tk.NO, minwidth=0)
        self.marks_list.column("name", width=50, stretch=tk.YES, minwidth=50)
        self.marks_list.column("description", width=100, stretch=tk.YES, minwidth=100)

        self.marks_list.bind('<Double-1>', self.on_mark_click)


        # Привязка события выбора
        # self.marks_list.bind("<<TreeviewSelect>>", self.on_mark_select)

    def create_right_panel(self):
        self.right_panel = ttk.Frame(self.paned_window, width=1000)
        self.paned_window.add(self.right_panel, minsize=1000)

        button_frame = ttk.Frame(self.right_panel)
        button_frame.pack(fill="x", padx=10, pady=5)
        self.add_btn = tk.Button(button_frame, text="Добавить метку", command=self.open_add_mark)
        self.add_btn.pack(side="left", padx=5)

    def on_mark_click(self, event):
        selected_item = self.marks_list.selection()
        if selected_item:
            item = self.marks_list.item(selected_item)
            mark_id = item['values'][0]
            MarkDialog(self.parent, self, self.root, self.db_service, self.schema_id, mark_id)

    def open_add_mark(self):
        MarkDialog(self.parent, self, self.root, self.db_service, self.schema_id, None)

    def fill_list_marks(self):
        for item in self.marks_list.get_children():
            self.marks_list.delete(item)

        marks = self.db_service.get_marks(self.schema_id)
        if len(marks) > 0:
            for mark in marks:
                self.marks_list.insert("", tk.END, values=(mark.id, mark.name, mark.description))

            first_item = self.marks_list.get_children()[0]
            self.marks_list.selection_set(first_item)
            self.marks_list.focus(first_item)

    def add_mark(self, mark_id):
        mark = self.db_service.get_mark(mark_id)
        self.marks_list.insert("", tk.END, values=(mark.id, mark.name, mark.description))
