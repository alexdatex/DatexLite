from tkinter import Toplevel, Label, Entry, Frame, messagebox, StringVar, Text, END, Scrollbar
from tkinter import ttk

from db import Equipment


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

    def center_window(self, main_frame):
        main_frame.update_idletasks()
        width = main_frame.winfo_width()
        height = main_frame.winfo_height()
        x = (main_frame.winfo_screenwidth() // 2) - (width // 2)
        y = (main_frame.winfo_screenheight() // 2) - (height // 2)
        main_frame.geometry(f'+{x}+{y}')

    def setup_ui(self):
        self.title("Редактировать оборудование" if self.equipment_id else "Добавить оборудование")
        self.geometry("450x550")
        self.resizable(False, False)
        self.grab_set()
        self.center_window(self)

        form_frame = Frame(self, padx=10, pady=10)
        form_frame.pack(fill="both", expand=True)

        fields = [
            ("Корпус по ГП:", "korpus"),
            ("Технологический номер:", "code"),
            ("Наименовние оборудования:", "name"),
            ("Назначение:", "purpose"),
            ("Производитель:", "manufacturer"),
            ("Тип:", "type"),
            ("Серийный номер:", "serial_number"),
            ("Дата изготовления (год):", "production_date"),
            ("Группа:", "group_name"),
            ("Аудит выполнен:", "is_audit_completed"),
            ("Позиция:", "position"),
        ]

        self.entries = {}
        self.text_entries = {}

        for i, (text, name) in enumerate(fields):
            ttk.Label(form_frame, text=text).grid(row=i, column=0, sticky="e", pady=5)
            if name == "position":  # Многострочное поле
                text_widget = Text(form_frame, width=30, height=10, wrap="word")
                scrollbar = Scrollbar(form_frame, command=text_widget.yview)
                text_widget.config(yscrollcommand=scrollbar.set)

                text_widget.grid(row=i, column=1, pady=5, sticky="ns")
                scrollbar.grid(row=i, column=2, sticky="ns")

                text_widget.config(state="normal")
                self.entries[name] = text_widget
                self.text_entries[name] = text_widget
            else:
                if name == "is_audit_completed":
                    # Создаем Combobox с вариантами "Нет" и "Да"
                    combobox = ttk.Combobox(form_frame, values=["Нет, в процессе", "Да"])
                    combobox.grid(row=i, column=1, pady=5)
                    combobox.set("Нет, в процессе")  # Устанавливаем значение по умолчанию
                    self.entries[name] = combobox
                    self.text_entries[name] = combobox
                else:
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
        self.update_entries_from_equipmentupdate_entries_from_equipment(equipment)

    def update_entries_from_equipmentupdate_entries_from_equipment(self, equipment):
        """Обновляет все поля формы из атрибутов объекта equipment"""
        for field_name, field_widget in self.text_entries.items():
            # Получаем значение из equipment или пустую строку по умолчанию
            field_value = getattr(equipment, field_name, "")

            # Обработка для виджета Text
            if isinstance(field_widget, Text):
                self._update_text_widget(field_widget, field_value)
                continue

            # Обработка для Combobox
            if isinstance(field_widget, ttk.Combobox):
                self._update_combobox_widget(field_widget, field_value)
                continue

            # Обработка для всех остальных виджетов (Entry, Spinbox и т.д.)
            self._update_standard_widget(field_widget, field_value)

    def _update_text_widget(self, widget, value):
        """Обновляет содержимое текстового виджета"""
        widget.delete("1.0", END)
        widget.insert("1.0", str(value))

    def _update_combobox_widget(self, widget, value):
        """Обновляет значение Combobox на основе переданного значения"""
        # Преобразуем булево или числовое значение в "Да"/"Нет"
        if value in (True, 1, "1", "Да"):
            widget.set("Да")
        else:
            widget.set("Нет, в процессе")

    def _update_standard_widget(self, widget, value):
        """Обновляет стандартные виджеты (Entry, Spinbox и др.)"""
        try:
            widget.set(str(value))
        except AttributeError:
            # Если у виджета нет метода set, используем delete/insert
            widget.delete(0, END)
            widget.insert(0, str(value))

    def save(self):
        if self.validate():

            data = {}
            for name, entry in self.text_entries.items():
                if isinstance(entry, Text):
                    value = entry.get("1.0", "end-1c")
                elif isinstance(entry, ttk.Combobox):
                    value = 1 if entry.get() == 'Да' else 0
                else:
                    value = entry.get()

                # Сохраняем значение
                data[name] = value

                # Добавляем lowercase версию, если есть соответствующее поле
                lower_field = f"{name}_lower"
                if hasattr(Equipment, lower_field):
                    data[lower_field] = str(value).lower()

            if self.equipment_id:
                self.root.update_equipment(self.equipment_id, data)
            else:
                self.root.add_equipment(data)

            self.destroy()

    def validate(self):
        names = ["name", "group_name"]
        for name in names:
            entry = self.entries.get(name)
            if not entry.get():
                messagebox.showerror("Ошибка", f"Поле '{name}' должно быть заполнено!", parent=self)
                return False
        return True
