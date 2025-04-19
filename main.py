import tkinter as tk
from tkinter import ttk, messagebox, DISABLED
import os
from configparser import ConfigParser
from db import SessionLocal, init_db
from db import ComponentService, Equipment
from db import DBController
from tabs import ComponentInfoTab, SchemaInfoTab, LabelsInfoTab
from views.dialog_equipment import EquipmentDialog


class PhotoViewerApp:
    def __init__(self):
        self.db = SessionLocal()
        self.db_controller = DBController(self.db)

        self.root = tk.Tk()
        self.root.title("DATEX Lite")
        
        # Инициализация параметров окна
        self.init_window_settings()
        
        # Создание главного интерфейса
        self.create_main_paned_window()
        self.create_left_panel()
        self.create_right_panel()
        
        # Инициализация данных
        self.update_equipment_list()
        
        # Загрузка настроек и запуск
        self.load_settings()
        self.setup_initial_layout()
        self.root.mainloop()
    
    def init_window_settings(self):
        """Инициализация параметров окна"""
        self.root.minsize(800, 800)
        self.default_width = 1000
        self.default_height = 800
        self.default_x = None
        self.default_y = None
        self.config = ConfigParser()
        self.config_file = "settings.ini"
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_main_paned_window(self):
        """Создание главного разделяемого окна"""
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=5)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.left_panel = tk.Frame(self.paned_window, width=100)
        self.right_panel = tk.Frame(self.paned_window)

        self.paned_window.add(self.left_panel)
        self.paned_window.add(self.right_panel)

        self.paned_window.paneconfigure(self.left_panel, minsize=150)
    #   self.paned_window.paneconfigure(self.right_panel, weight=1)

    #        self.paned_window.sashpos(0, 250)

    def create_left_panel(self):

        # Создание Treeview с вертикальной прокруткой
        self.tree_frame = ttk.Frame(self.left_panel)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.photo_tree = ttk.Treeview(
            self.tree_frame,
            yscrollcommand=self.tree_scroll.set,
            selectmode="browse",
            columns=("id", "name", "code"),
            show="headings"
        )
        self.photo_tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree_scroll.config(command=self.photo_tree.yview)
        
        # Настройка колонок
        self.photo_tree.heading("id", text="ID", anchor=tk.W)
        self.photo_tree.heading("name", text="Название", anchor=tk.W)
        self.photo_tree.heading("code", text="Номер", anchor=tk.W)
        self.photo_tree.column("id", width=0, stretch=tk.NO, minwidth=0)
        self.photo_tree.column("name", width=450, stretch=tk.YES, minwidth=200)
        self.photo_tree.column("code", width=200, stretch=tk.YES, minwidth=200)

        # Привязка события выбора
        self.photo_tree.bind("<<TreeviewSelect>>", self.on_photo_select)

        button_frame = ttk.Frame(self.left_panel)
        button_frame.pack(fill="x", padx=10, pady=5)
        self.add_btn = tk.Button(button_frame, text="Добавить оборудование", command=self.open_add_dialog)
        self.add_btn.pack(side="left", padx=5)
        self.delete_btn = tk.Button(button_frame, text="Удалить", command=self.delete_equipment, state=DISABLED)
        self.delete_btn.pack(side="left", padx=5)

    def create_right_panel(self):
        """Создание правой панели с описанием"""

        self.notebook = ttk.Notebook(self.right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.component_info_tab = ComponentInfoTab(self.notebook, self.db_controller, self)
        self.schema_info_tab = SchemaInfoTab(self.notebook, self.db_controller, self, self.root)
        self.labels_info_tab = LabelsInfoTab(self.notebook, self.db_controller, self)

        self.notebook.add(self.component_info_tab.frame, text="Данные оборудования")
        self.notebook.add(self.schema_info_tab.frame, text="Схема оборудования")
        self.notebook.add(self.labels_info_tab.frame, text="Метки схемы")

    def update_equipment_list(self):
        for item in self.photo_tree.get_children():
            self.photo_tree.delete(item)
        components = ComponentService.get_components(self.db)
        if len(components) > 0 :
            for component in components:
                self.photo_tree.insert("", tk.END,
                                       values=(
                                           component.id,
                                           component.name,
                                           component.code))
            first_item = self.photo_tree.get_children()[0]
            self.photo_tree.selection_set(first_item)
            self.photo_tree.focus(first_item)

    def setup_initial_layout(self):
        geometry_string = f"{self.window_width}x{self.window_height}"
        if self.window_x is not None and self.window_y is not None:
            geometry_string += f"+{self.window_x}+{self.window_y}"
        self.root.geometry(geometry_string)

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                self.config.read(self.config_file)
                self.window_width = self.config.getint('Window', 'width', fallback=self.default_width)
                self.window_height = self.config.getint('Window', 'height', fallback=self.default_height)
                self.window_x = self.config.getint('Window', 'x', fallback=self.default_x)
                self.window_y = self.config.getint('Window', 'y', fallback=self.default_y)
#                self.sash_pos = self.config.getint('Window', 'sash_pos', fallback=None)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить настройки: {e}")
                self.reset_to_defaults()
        else:
            self.reset_to_defaults()
    
    def save_settings(self):
        try:
            self.config['Window'] = {
                'width': str(self.root.winfo_width()),
                'height': str(self.root.winfo_height()),
                'x': str(self.root.winfo_x()),
                'y': str(self.root.winfo_y()),
            }
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {e}")

    def on_photo_select(self, event):
        selected_item = self.photo_tree.selection()
        if selected_item:
            item = self.photo_tree.item(selected_item)
            photo_id = item['values'][0]
            self.update_component_info(photo_id)
    
    def open_add_dialog(self):
        EquipmentDialog(self.root, self, self.db_controller, None)

    def update_dialog(self, equipment_id):
        EquipmentDialog(self.root, self, self.db_controller, equipment_id)

    def update_equipment(self, equipment_id, data):
        equipment = self.db.query(Equipment).get(equipment_id)
        if equipment:
            for key, value in data.items():
                if key != "id":
                    setattr(equipment, key, value)
        self.db.commit()
        self.current_component_id = -1
        self.empty_component_info()
        self.update_equipment_list()
        # EquipmentDialog(self.root, self.db_controller, equipment_id)

    def delete_equipment(self):
        self.delete_btn.config(state=tk.DISABLED)
        equipment = ComponentService.get_component(self.db, self.current_component_id)
        self.db.delete(equipment)
        self.db.commit()
        self.current_component_id = -1
        self.empty_component_info()
        self.update_equipment_list()

    def update_component_info(self, component_id):
        self.current_component_id = component_id
        self.delete_btn.config(state=tk.NORMAL)
        self.component_info_tab.update(component_id)
        self.schema_info_tab.update(component_id)
        self.labels_info_tab.update(component_id)

    def empty_component_info(self):
        self.current_component_id = -1
        self.component_info_tab.clean()

    def add_equipment(self, data):
        equipment = Equipment(**data)
        self.db.add(equipment)
        self.db.commit()
        self.photo_tree.insert("", tk.END, values=(equipment.id, equipment.name))

    def on_closing(self):
        self.save_settings()
        self.root.destroy()

    def reset_to_defaults(self):
        self.window_width = self.default_width
        self.window_height = self.default_height
        self.window_x = self.default_x
        self.window_y = self.default_y

if __name__ == "__main__":
    init_db()
    app = PhotoViewerApp()