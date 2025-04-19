import tkinter as tk
from tkinter import ttk

class ComponentInfoTab:
    def __init__(self, parent, db_service):
        self.controller = None
        self.frame = tk.Frame(parent, padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)
        self.db_service = db_service
        #
        # self.desc_label = tk.Label(self.frame,
        #                          text="Описание:",
        #                          font=("Arial", 12, "bold"))
        # self.desc_label.pack(pady=10)
        #
        # self.desc_text = tk.Text(self.frame,
        #                        wrap=tk.WORD,
        #                        height=3,
        #                        padx=5,
        #                        pady=5)
        # self.desc_text.pack(fill=tk.BOTH, expand=True, padx=5)

        fields = [
            ("Название:", "name"),
            ("Назначение:", "purpose"),
            ("Производитель:", "manufacturer"),
            ("Серийный номер:", "serial"),
            ("Дата изготовления (ГГГГ-ММ-ДД):", "date"),
            ("Место размещения:", "location")
        ]

        self.entries = {}
        for i, (text, name) in enumerate(fields):
            tk.Label(self.frame, text=text).grid(row=i, column=0, sticky="e", pady=5)
            entry = tk.Entry(self.frame, width=30)
            entry.config(state="readonly")
            entry.grid(row=i, column=1, pady=5)
            self.entries[name] = entry


    def update(self, component_id):
        """Обновление описания компонента"""
        # component = self.db_service.get_component(component_id)
        #
        # self.desc_text.config(state=tk.NORMAL)
        # self.desc_text.delete(1.0, tk.END)
        # self.desc_text.insert(tk.END, component.description)
        # self.desc_text.config(state=tk.DISABLED)