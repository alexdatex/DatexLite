import tkinter as tk
from tkinter import ttk

class LabelsInfoTab:
    def __init__(self, parent, db_service):
        self.controller = None
        self.frame = ttk.Frame(parent)
        self.db_service = db_service

        self.desc_label = tk.Label(self.frame,
                                 text="Описание:",
                                 font=("Arial", 12, "bold"))
        self.desc_label.pack(pady=10)

        self.desc_text = tk.Text(self.frame,
                               wrap=tk.WORD,
                               height=10,
                               padx=5,
                               pady=5)
        self.desc_text.pack(fill=tk.BOTH, expand=True, padx=5)


    def update(self, component_id):
        """Обновление описания компонента"""
        component = self.db_service.get_component(component_id)

        self.desc_text.config(state=tk.NORMAL)
        self.desc_text.delete(1.0, tk.END)
        self.desc_text.insert(tk.END, component.description)
        self.desc_text.config(state=tk.DISABLED)