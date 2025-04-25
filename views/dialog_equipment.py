from tkinter import Toplevel, Label, Entry, Button, Frame, messagebox
from datetime import datetime
from tkinter import ttk


class EquipmentDialog(Toplevel):
    def __init__(self, parent, root, controller, equipment_id=None):
        super().__init__(parent)
        self.root = root
        self.controller = controller
        self.equipment_id = equipment_id
        self.setup_ui()

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
        self.geometry("400x350")
        self.resizable(False, False)
        self.grab_set()
        self.center_window(self)

        form_frame = Frame(self, padx=10, pady=10)
        form_frame.pack(fill="both", expand=True)

        fields = [
            ("Технологический номер:", "code"),
            ("Наименовние оборудования:", "name"),
            ("Назначение:", "purpose"),
            ("Производитель:", "manufacturer"),
            ("Тип:", "type"),
            ("Серийный номер:", "serial_number"),
            ("Дата изготовления (год):", "production_date"),
            ("Группа:", "group_name")
        ]

        self.entries = {}
        for i, (text, name) in enumerate(fields):
            Label(form_frame, text=text).grid(row=i, column=0, sticky="e", pady=5)
            entry = Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            self.entries[name] = entry

        button_frame = Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Сохранить", command=self.save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.destroy).pack(side="left", padx=5)

    def fill_form(self):
        equipment = self.controller.get_component(self.equipment_id)
        if equipment:
            self.entries["name"].insert(0, equipment.name)
            self.entries["code"].insert(0, equipment.code)
            self.entries["purpose"].insert(0, equipment.purpose)
            self.entries["manufacturer"].insert(0, equipment.manufacturer)
            self.entries["type"].insert(0, equipment.type)
            self.entries["serial_number"].insert(0, equipment.serial_number)
            self.entries["production_date"].insert(0, equipment.production_date)
            self.entries["group_name"].insert(0, equipment.group_name)

    def save(self):
        if self.validate():
            data = {name: entry.get() for name, entry in self.entries.items()}
#            data["production_date"] = datetime.strptime(data["production_date"], "%Y-%m-%d").date()

            data["code_lower"]=data["code"].lower()
            data["name_lower"]=data["name"].lower()
            data["purpose_lower"]=data["purpose"].lower()
            data["manufacturer_lower"]=data["manufacturer"].lower()
            data["type_lower"]=data["type"].lower()
            data["serial_number_lower"]=data["serial_number"].lower()
            data["production_date_lower"]=data["production_date"].lower()
            data["group_name_lower"]=data["group_name"].lower()

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

        # for name, entry in self.entries.items():
        #     if not entry.get():
        #         messagebox.showerror("Ошибка", f"Поле '{name}' должно быть заполнено!")
        #         return False
        #
        # try:
        #     datetime.strptime(self.entries["production_date"].get(), "%Y-%m-%d")
        # except ValueError:
        #     messagebox.showerror("Ошибка", "Некорректный формат даты! Используйте ГГГГ-ММ-ДД")
        #     return False

        return True
