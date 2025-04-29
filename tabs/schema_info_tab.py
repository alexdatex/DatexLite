import io
import os
import tkinter as tk
from tkinter import ttk, filedialog, DISABLED, messagebox, simpledialog, NORMAL

from PIL import Image, ImageTk

from db.models import EquipmentSchema
from views.dialog_marks_scheme import SchemeDialog


class SchemaInfoTab:
    def __init__(self, parent, db_service, root, tk_root):
        self.current_schema_id = -1
        self.root = root
        self.db_service = db_service
        self.parent = parent
        self.is_active = True
        self.tk_root = tk_root

        self.frame = tk.Frame(parent, padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)

        self.paned_window = tk.PanedWindow(self.frame, orient=tk.VERTICAL, sashrelief=tk.RAISED,
                                           sashwidth=5)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.create_top_panel()
        self.create_bottom_panel()
        self.parent.bind("<<NotebookTabChanged>>", self.check_active_status)

    def check_active_status(self, event):
        current_tab = self.parent.select()
        if current_tab == str(self.frame):
            if not self.is_active:
                self.is_active = True
                self.on_activate()
        else:
            if self.is_active:
                self.is_active = False
                self.on_deactivate()

    def on_activate(self):
        self.show_preview()

    def on_deactivate(self):
        """Вызывается при деактивации вкладки"""

    def create_top_panel(self):
        self.top_panel = ttk.Frame(self.paned_window, height=400)
        self.paned_window.add(self.top_panel, min=400)

        self.frame_info = tk.Frame(self.top_panel, padx=10, pady=10)
        self.frame_info.pack(fill="both", expand=True)

        # Создание Treeview с вертикальной прокруткой
        self.tree_frame = ttk.Frame(self.frame_info)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.photo_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="browse",
                                       columns=("id", "name", "description"), show="headings")
        self.photo_tree.pack(fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.photo_tree.yview)

        # Настройка колонок
        self.photo_tree.heading("id", text="ID", anchor=tk.W)
        self.photo_tree.heading("name", text="Имя файла", anchor=tk.W)
        self.photo_tree.heading("description", text="Описание", anchor=tk.W)
        self.photo_tree.column("id", width=0, stretch=tk.NO, minwidth=0)
        self.photo_tree.column("name", width=100, stretch=tk.YES, minwidth=200)
        self.photo_tree.column("description", width=450, stretch=tk.YES, minwidth=300)

        self.photo_tree.bind("<<TreeviewSelect>>", self.on_schema_select)

        button_frame = tk.Frame(self.top_panel, padx=10, pady=5)
        button_frame.pack(fill="both", expand=True)
        self.add_btn = ttk.Button(button_frame, text="Добавить схему", command=self.open_add_scheme, state=DISABLED)
        self.add_btn.pack(side="left", padx=5)
        self.delete_btn = ttk.Button(button_frame, text="Удалить схему", command=self.delete_schema, state=DISABLED)
        self.delete_btn.pack(side="left", padx=5)

        button_frame = tk.Frame(self.top_panel, padx=10, pady=5)
        button_frame.pack(fill="both", expand=True)
        self.show_marks_btn = ttk.Button(button_frame, text="Редактировать метки на схеме", command=self.open_edit_marks_dialog, state=DISABLED)
        self.show_marks_btn.pack(side="left", padx=5)

    def open_add_scheme(self):
        file_path = filedialog.askopenfilename(
            title="Select Photo",
            filetypes=(
                ("Изображения", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("PDF файлы", "*.pdf"),
                ("All files", "*.*"))
        )
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    name = os.path.basename(file_path)
                    description = simpledialog.askstring("Описание схемы", "Введите описание схемы:",
                                                         parent=self.tk_root)

                    if file_path.lower().endswith('.pdf'):
                        import fitz
                        doc = fitz.open(stream=file_data, filetype="pdf")
                        total_pages = len(doc)
                        page = doc[0]
                        pix = page.get_pixmap()
                        image_data = pix.tobytes("png")
                    else:
                        image_data = file_data

                    schema = EquipmentSchema(name=name,
                                             data_original=file_data,
                                             data_image=image_data,
                                             description=description,
                                             equipment_id=self.current_component_id, user_id=self.root.user_id,
                                             is_deleted=False)

                    self.db_service.add_schema(schema)
                    self.update_list_schemas()

            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка добавление файла: {e}", parent=self)

    def open_edit_dialog(self):
        pass

    def delete_schema(self):
        answer = messagebox.askyesno(
            "Подтверждение удаления",
            "Вы точно хотите удалить эту схему?",
            icon='warning'
        )
        if answer:
            self.db_service.delete_schema(self.current_schema_id)
            self.current_schema_id = -1
            self.delete_btn.config(state=DISABLED)
            self.show_marks_btn.config(state=DISABLED)
            self.clear_image_display()
            self.update_list_schemas()

    def open_edit_marks_dialog(self):
        SchemeDialog(self.tk_root, self, self.db_service, self.root, self.root.user_id, self.current_schema_id)

    def create_bottom_panel(self):
        self.bottom_panel = ttk.Frame(self.paned_window)
        self.paned_window.add(self.bottom_panel, min=200)

        self.frame_info = tk.Frame(self.bottom_panel, padx=10, pady=10)
        self.frame_info.pack(fill="both", expand=True)

        self.image_canvas = tk.Canvas(self.frame_info, bg='white')
        self.image_canvas.pack(fill=tk.BOTH, expand=True)


    def update(self, component_id):
        if component_id:
            self.add_btn.configure(state=NORMAL)

        self.show_marks_btn.configure(state=DISABLED)
        self.current_component_id = component_id
        self.clear_image_display()
        self.update_list_schemas()

    def update_list_schemas(self):
        for item in self.photo_tree.get_children():
            self.photo_tree.delete(item)
        schemas = self.db_service.get_schemas(self.current_component_id)
        if len(schemas) > 0:
            for schema in schemas:
                self.photo_tree.insert("", tk.END,
                                       values=(
                                           schema.id,
                                           schema.name, schema.description))
            first_item = self.photo_tree.get_children()[0]
            self.photo_tree.selection_set(first_item)
            self.photo_tree.focus(first_item)

    def on_schema_select(self, event):
        selected_item = self.photo_tree.selection()
        if selected_item:
            self.add_btn.configure(state=NORMAL)
            self.show_marks_btn.configure(state=NORMAL)
            self.delete_btn.configure(state=NORMAL)
            item = self.photo_tree.item(selected_item)
            schema_id = item['values'][0]
            self.update_schema_info(schema_id)

        else:
            self.delete_btn.configure(state=DISABLED)


    def clear_image_display(self):
        self.image_canvas.delete("all")
        if hasattr(self.image_canvas, 'image'):
            del self.image_canvas.image

    def display_image(self, image_data):
        self.clear_image_display()

        try:
            image = Image.open(io.BytesIO(image_data))

            # Calculate aspect ratio
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()

            img_width, img_height = image.size
            ratio = min(canvas_width / img_width, canvas_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)

            image = image.resize((new_width, new_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Center the image
            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2

            self.image_canvas.image = photo  # Keep a reference
            self.image_canvas.create_image(x, y, image=photo, anchor=tk.NW)
        except Exception as e:
            print(f"Error displaying image: {e}")

    def update_schema_info(self, schema_id):
        self.current_schema_id = schema_id
        self.show_preview()

    def show_preview(self):
        if self.current_schema_id != -1:
            schema = self.db_service.get_schema(self.current_schema_id)
            if self.is_active:
                self.display_image(schema.data_image)

    def clean(self):
        for item in self.photo_tree.get_children():
            self.photo_tree.delete(item)

        self.add_btn.configure(state=DISABLED)
        self.delete_btn.configure(state=DISABLED)
        self.show_marks_btn.configure(state=DISABLED)

        self.current_schema_id = -1
        self.clear_image_display()
