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
            ("Название:", "name"),
            ("Код оборудования:", "code"),
            ("Назначение:", "purpose"),
            ("Производитель:", "manufacturer"),
            ("Тип:", "type"),
            ("Серийный номер:", "serial_number"),
            ("Дата изготовления (ГГГГ-ММ-ДД):", "production_date"),
            ("Место размещения:", "location")
        ]

        self.entries = {}
        self.text_entries = {}
        for i, (text, name) in enumerate(fields):
            tk.Label(self.frame_info, text=text).grid(row=i, column=0, sticky="e", pady=5)
            entry_text = tk.StringVar()
            entry = tk.Entry(self.frame_info, width=30, textvariable=entry_text)
            entry.config(state="readonly")
            entry.grid(row=i, column=1, pady=5)
            self.entries[name] = entry
            self.text_entries[name] = entry_text

        button_frame = tk.Frame(self.frame, padx=10, pady=5)
        button_frame.pack(fill="both", expand=True)
        self.edit_btn = tk.Button(button_frame, text="Редактировать оборудование", command=self.open_edit_dialog,
                                  state=DISABLED)
        self.edit_btn.pack(side="left", padx=5)

    def open_edit_dialog(self):
        self.root.update_dialog(self.current_component_id)


    def update(self, component_id):
        self.current_component_id = component_id
        equipment = self.db_service.get_component(component_id)
        self.text_entries["name"].set(equipment.name)
        self.text_entries["code"].set(equipment.code)
        self.text_entries["purpose"].set(equipment.purpose)
        self.text_entries["manufacturer"].set(equipment.manufacturer)
        self.text_entries["type"].set(equipment.type)
        self.text_entries["serial_number"].set(equipment.serial_number)
        self.text_entries["production_date"].set(equipment.production_date.strftime("%Y-%m-%d"))
        self.text_entries["location"].set(equipment.location)
        self.edit_btn.config(state=tk.NORMAL)

    def clean(self):
        self.current_component_id = -1
        self.text_entries["name"].set("")
        self.text_entries["code"].set("")
        self.text_entries["purpose"].set("")
        self.text_entries["manufacturer"].set("")
        self.text_entries["type"].set("")
        self.text_entries["serial_number"].set("")
        self.text_entries["production_date"].set("")
        self.text_entries["location"].set("")
        self.edit_btn.config(state=tk.DISABLED)
