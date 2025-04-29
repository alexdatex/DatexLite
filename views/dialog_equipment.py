from tkinter import Toplevel, Label, Entry, Frame, messagebox, StringVar, Text, END, Scrollbar
from tkinter import ttk


class EquipmentDialog(Toplevel):
    def __init__(self, parent, root, controller, equipment_id=None):
        super().__init__(parent)
        self.root = root
        self.controller = controller
        self.equipment_id = equipment_id
        self.setup_ui()
        self.iconphoto(False, self.root.photo)

        if equipment_id:
            self.fill_form()

    def center_window(self,main_frame):
        main_frame.update_idletasks()
        width = main_frame.winfo_width()
        height = main_frame.winfo_height()
        x = (main_frame.winfo_screenwidth() // 2) - (width // 2)
        y = (main_frame.winfo_screenheight() // 2) - (height // 2)
        main_frame.geometry(f'+{x}+{y}')

    def setup_ui(self):
        self.title("Редактировать оборудование" if self.equipment_id else "Добавить оборудование")
        self.geometry("450x520")
        self.resizable(False, False)
        self.grab_set()
        self.center_window(self)

        form_frame = Frame(self, padx=10, pady=10)
        form_frame.pack(fill="both", expand=True)

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
            ("Позиция:", "position"),
        ]

        self.entries = {}
        self.text_entries = {}

        for i, (text, name) in enumerate(fields):
            if name == "position":  # Многострочное поле
                ttk.Label(form_frame, text=text).grid(row=i, column=0, sticky="e", pady=5)
                text_widget = Text(form_frame, width=30, height=10, wrap="word")
                scrollbar = Scrollbar(form_frame, command=text_widget.yview)
                text_widget.config(yscrollcommand=scrollbar.set)

                text_widget.grid(row=i, column=1, pady=5, sticky="ns")
                scrollbar.grid(row=i, column=2, sticky="ns")

                text_widget.config(state="normal")
                self.entries[name] = text_widget
                self.text_entries[name] = text_widget
            else:
                ttk.Label(form_frame, text=text).grid(row=i, column=0, sticky="e", pady=5)
                entry_text = StringVar()
                entry = Entry(form_frame, width=30, textvariable=entry_text)
                entry.grid(row=i, column=1, pady=5)
                self.entries[name] = entry_text
                self.text_entries[name] = entry_text

        button_frame = Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Сохранить", command=self.save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.destroy).pack(side="left", padx=5)

    def fill_form(self):
        equipment = self.controller.get_component(self.equipment_id)
        if equipment:
            for name, entry in self.text_entries.items():
                value = getattr(equipment, name, "")
                if isinstance(entry, Text):
                    entry.delete("1.0", END)
                    entry.insert("1.0", value)
                else:
                    entry.set(value)

    def save(self):
        if self.validate():

            data = {}
            for name, entry in self.text_entries.items():
                if isinstance(entry, Text):
                    data[name] = entry.get("1.0", "end-1c")
                else:
                    data[name] = entry.get()
                data[f"{name}_lower"] = data[name].lower()

            if self.equipment_id:
                self.root.update_equipment(self.equipment_id, data)
            else:
                self.root.add_equipment(data)

            self.destroy()

    def validate(self):
        names = ["name","group_name"]
        for name in names:
            entry = self.entries.get(name)
            if not entry.get():
                messagebox.showerror("Ошибка", f"Поле '{name}' должно быть заполнено!", parent=self)
                return False
        return True
