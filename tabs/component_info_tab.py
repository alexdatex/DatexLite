import tkinter as tk
from tkinter import ttk, DISABLED


class ComponentInfoTab:
    def __init__(self, parent, db_service, root):
        self.db_service = db_service
        self.current_component_id = -1
        self.root = root

        self.frame = tk.Frame(parent, padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)

        self.frame_info = tk.Frame(self.frame, padx=10, pady=10)
        self.frame_info.pack(fill="both", expand=True)

        fields = [
            ("Копрус по ГП:", "korpus"),
            ("Технологический номер:", "code"),
            ("Наименовние оборудования:", "name"),
            ("Назначение:", "purpose"),
            ("Производитель:", "manufacturer"),
            ("Тип:", "type"),
            ("Серийный номер:", "serial_number"),
            ("Дата изготовления (год):", "production_date"),
            ("Группа:", "group_name"),
            ("Позиция:", "position")
        ]

        self.entries = {}
        self.text_entries = {}

        for i, (text, name) in enumerate(fields):
            if name == "position":  # Многострочное поле
                ttk.Label(self.frame_info, text=text).grid(row=i, column=0, sticky="e", pady=5)

                text_widget = tk.Text(self.frame_info, width=30, height=10, wrap="word")
                scrollbar = tk.Scrollbar(self.frame_info, command=text_widget.yview)
                text_widget.config(yscrollcommand=scrollbar.set)

                text_widget.grid(row=i, column=1, pady=5, sticky="ns")
                scrollbar.grid(row=i, column=2, sticky="ns")

                text_widget.config(state="normal")
                text_widget.config(state="disabled")
                self.entries[name] = text_widget
                self.text_entries[name] = text_widget
            else:
                ttk.Label(self.frame_info, text=text).grid(row=i, column=0, sticky="e", pady=5)
                entry_text = tk.StringVar()
                entry = tk.Entry(self.frame_info, width=30, textvariable=entry_text)
                entry.grid(row=i, column=1, pady=5)
                entry.config(state="readonly")
                self.entries[name] = entry
                self.text_entries[name] = entry_text

        button_frame = tk.Frame(self.frame, padx=10, pady=5)
        button_frame.pack(fill="both", expand=True)
        self.edit_btn = ttk.Button(button_frame, text="Редактировать оборудование", command=self.open_edit_dialog,
                                  state=DISABLED)
        self.edit_btn.pack(side="left", padx=5)

    def open_edit_dialog(self):
        self.root.update_dialog(self.current_component_id)


    def update(self, component_id):
        self.current_component_id = component_id
        equipment = self.db_service.get_component(component_id)

        for name, entry in self.text_entries.items():
            value = getattr(equipment, name, "")
            if isinstance(entry, tk.Text):
                entry.config(state="normal")
                entry.delete("1.0", tk.END)
                entry.insert("1.0", value)
                entry.config(state=tk.DISABLED)
            else:
                entry.set(value)

        self.edit_btn.config(state=tk.NORMAL)

    def clean(self):
        self.current_component_id = -1
        value = ""
        for name, entry in self.text_entries.items():
            if isinstance(entry, tk.Text):
                entry.config(state="normal")
                entry.delete("1.0", tk.END)
                entry.insert("1.0", value)
                entry.config(state=tk.DISABLED)
            else:
                entry.set(value)

        self.edit_btn.config(state=tk.DISABLED)
