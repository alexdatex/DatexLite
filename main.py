import tkinter as tk
from tkinter import ttk, messagebox, DISABLED
import os
from configparser import ConfigParser
from db import SessionLocal, init_db
from db import ComponentService
from db import DBController
from tabs import ComponentInfoTab, SchemaInfoTab, LabelsInfoTab


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
        self.create_reset_button()
        
        # Инициализация данных
        self.init_photo_data()
        
        # Загрузка настроек и запуск
        self.load_settings()
        self.setup_initial_layout()
        self.root.mainloop()
    
    def init_window_settings(self):
        """Инициализация параметров окна"""
        self.root.minsize(500, 300)
        self.default_width = 1000
        self.default_height = 800
        self.default_x = None
        self.default_y = None
        self.config = ConfigParser()
        self.config_file = "settings.ini"
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_main_paned_window(self):
        """Создание главного разделяемого окна"""
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
    
    def create_left_panel(self):
        self.left_panel = ttk.Frame(self.paned_window, width=500)
        self.paned_window.add(self.left_panel, minsize=200)


        # Создание Treeview с вертикальной прокруткой


        self.tree_frame = ttk.Frame(self.left_panel)
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
        
        # Привязка события выбора
        self.photo_tree.bind("<<TreeviewSelect>>", self.on_photo_select)
        button_frame = ttk.Frame(self.left_panel)
        button_frame.pack(fill="x", padx=10, pady=5)
        self.add_btn = tk.Button(button_frame, text="Добавить оборудование", command=self.open_add_dialog)
        self.add_btn.pack(side="left", padx=5)
        self.update_btn = tk.Button(button_frame, text="Обновить", command=self.update_equipment, state=DISABLED)
        self.update_btn.pack(side="left", padx=5)
        self.delete_btn = tk.Button(button_frame, text="Удалить", command=self.delete_equipment, state=DISABLED)
        self.delete_btn.pack(side="left", padx=5)

    def create_right_panel(self):
        """Создание правой панели с описанием"""
        self.right_panel = ttk.Frame(self.paned_window, width=300)
        self.paned_window.add(self.right_panel, minsize=100)

        self.notebook = ttk.Notebook(self.right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.component_info_tab = ComponentInfoTab(self.notebook, self.db_controller)
        self.schema_info_tab = SchemaInfoTab(self.notebook, self.db_controller)
        self.labels_info_tab = LabelsInfoTab(self.notebook, self.db_controller)

        self.notebook.add(self.component_info_tab.frame, text="Данные оборудования")
        self.notebook.add(self.schema_info_tab.frame, text="Схема оборудования")
        self.notebook.add(self.labels_info_tab.frame, text="Метки схемы")


    
    def create_reset_button(self):
        """Создание кнопки сброса настроек"""
        self.reset_button = tk.Button(
            self.root, 
            text="Сбросить настройки", 
            command=self.reset_settings
        )
        self.reset_button.pack(pady=10)
    
    def init_photo_data(self):
        """Инициализация данных о компонентах"""
        components = ComponentService.get_components(self.db)
        self.current_photo_index = 0

        if len(components) > 0 :
            for component in components:
                self.photo_tree.insert("", tk.END, values=(component.id, component.name))

            first_item = self.photo_tree.get_children()[0]
            self.photo_tree.selection_set(first_item)
            self.photo_tree.focus(first_item)

    
    def setup_initial_layout(self):
        """Установка начального расположения элементов"""
        geometry_string = f"{self.window_width}x{self.window_height}"
        if self.window_x is not None and self.window_y is not None:
            geometry_string += f"+{self.window_x}+{self.window_y}"
        self.root.geometry(geometry_string)
        
#        if hasattr(self, 'sash_pos') and self.sash_pos is not None:
#            self.root.after(100, lambda: self.paned_window.sashpos(0, self.sash_pos))
    
    def load_settings(self):
        """Загрузка сохраненных настроек из файла"""
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
        """Сохранение текущих настроек в файл"""
        try:
            self.config['Window'] = {
                'width': self.root.winfo_width(),
                'height': self.root.winfo_height(),
                'x': self.root.winfo_x(),
                'y': self.root.winfo_y(),
#                'sash_pos': self.paned_window.sashpos(0)
            }
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {e}")
    
    def reset_to_defaults(self):
        """Сброс настроек к значениям по умолчанию"""
        self.window_width = self.default_width
        self.window_height = self.default_height
        self.window_x = self.default_x
        self.window_y = self.default_y
        self.sash_pos = None
    
    def reset_settings(self):
        """Сброс настроек и перезапуск приложения"""
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            messagebox.showinfo("Информация", "Настройки сброшены. Приложение будет перезапущено.")
            self.root.destroy()
            PhotoViewerApp()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сбросить настройки: {e}")
    
    def on_photo_select(self, event):
        """Обработчик выбора фотографии в списке"""
        selected_item = self.photo_tree.selection()
        if selected_item:
            item = self.photo_tree.item(selected_item)
            photo_id = item['values'][0]
            self.update_component_info(photo_id)
    
    def open_add_dialog(self):
        print("open_add_dialog")

    def update_equipment(self):
        print("update_equipment")

    def delete_equipment(self):
        print("delete_equipment")

    def update_component_info(self, component_id):
        self.component_info_tab.update(component_id)



    def on_closing(self):
        """Обработчик события закрытия окна"""
        self.save_settings()
        self.root.destroy()

if __name__ == "__main__":
    init_db()
    app = PhotoViewerApp()