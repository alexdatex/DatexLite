import tkinter as tk
from tkinter import ttk

class SchemaInfoTab:
    def __init__(self, parent, db_service):
        self.controller = None
        self.frame = ttk.Frame(parent)
        self.db_service = db_service
        self.paned_window = tk.PanedWindow(self.frame, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        self.create_top_panel()
        self.create_bottom_panel()

    def create_top_panel(self):
        self.top_panel = ttk.Frame(self.paned_window, height=500)
        self.paned_window.add(self.top_panel, min=200)

        # Создание Treeview с вертикальной прокруткой
        self.tree_frame = ttk.Frame(self.top_panel)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.photo_tree = ttk.Treeview(
            self.tree_frame,
            yscrollcommand=self.tree_scroll.set,
            selectmode="browse",
            columns=("id", "name"),
            show="headings"
        )
        self.photo_tree.pack(fill=tk.BOTH, expand=True)

        self.tree_scroll.config(command=self.photo_tree.yview)

        # Настройка колонок
        self.photo_tree.heading("id", text="ID", anchor=tk.W)
        self.photo_tree.heading("name", text="Название", anchor=tk.W)
        self.photo_tree.column("id", width=0, stretch=tk.NO, minwidth=0)
        self.photo_tree.column("name", width=450, stretch=tk.YES, minwidth=200)

    def create_bottom_panel(self):
        self.bottom_panel = ttk.Frame(self.paned_window, height=500)
        self.paned_window.add(self.bottom_panel, min=200)

    def update(self, component_id):
        component = self.db_service.get_component(component_id)
