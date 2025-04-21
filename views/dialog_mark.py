from tkinter import Toplevel, Label, Entry, Button, Frame, messagebox, DISABLED, filedialog
from datetime import datetime
from tkinter import Toplevel, Label, Entry, Button, Frame
import tkinter as tk
from tkinter import ttk
import io
import os
from PIL import Image, ImageTk

from db.models.mark import Mark
from db.models.mark_image import MarkImage


class MarkDialog(Toplevel):
    def __init__(self, parent, parent2, root, controller, schema_id, mark_id=None):
        super().__init__(parent)
        self.parent2 = parent2
        self.root = root
        self.controller = controller
        self.mark_id = mark_id
        self.schema_id = schema_id
        self.setup_ui()
        self.point_mark = (0,0)

        if mark_id:
            parent.after(100, self.fill_form)
            #self.fill_form()

    def setup_ui(self):
        self.title("Редактировать метку" if self.mark_id else "Добавить метку")
        self.geometry("800x600")
        self.resizable(False, False)
        self.grab_set()

        form_frame = Frame(self, padx=10, pady=10)
        form_frame.pack(fill="both", expand=True)

        form_frame_info = Frame(form_frame, padx=10, pady=10)
        form_frame_info.pack(fill="both", expand=True)

        self.entries = {}
        Label(form_frame_info, text="Название").grid(row=1, column=0, sticky="e", pady=5)
        entry = Entry(form_frame_info, width=30)
        entry.grid(row=1, column=1, pady=5)
        self.entries["name"] = entry

        Label(form_frame_info, text="Описание").grid(row=2, column=0, sticky="e", pady=5)
        entry = Entry(form_frame_info, width=30)
        entry.grid(row=2, column=1, pady=5)
        self.entries["description"] = entry

        self.paned_window = tk.PanedWindow(form_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.create_left_panel()
        self.create_right_panel()

        button_frame = Frame(form_frame)
        button_frame.pack(pady=10)

        self.tmpMarks = []

        Button(button_frame, text="Сохранить", command=self.save).pack(side="left", padx=5)
        Button(button_frame, text="Отмена", command=self.destroy).pack(side="left", padx=5)

    def save(self):
        x,y = self.point_mark
        mark = Mark(
            name=self.entries["name"].get(),
            description=self.entries["description"].get(),
            schema_id=self.schema_id,
            x=x,
            y=y
        )
        self.controller.add_mark(mark)

        for item in self.tmpMarks:
            item.mark_id = mark.id
            self.controller.add_mark_image(item)

        self.parent2.add_mark(mark.id)
        self.destroy()


    def create_left_panel(self):
        self.left_panel = ttk.Frame(self.paned_window, width=150)
        self.paned_window.add(self.left_panel, minsize=150)

        self.tree_frame = ttk.Frame(self.left_panel)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.marks_list = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="browse",
                                       columns=("id", "name", "description"), show="headings")
        self.marks_list.pack(fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.marks_list.yview)

        # Настройка колонок
        self.marks_list.heading("id", text="ID", anchor=tk.W)
        self.marks_list.heading("name", text="Название", anchor=tk.W)
        self.marks_list.heading("description", text="Описание", anchor=tk.W)
        self.marks_list.column("id", width=0, stretch=tk.NO, minwidth=0)
        self.marks_list.column("name", width=50, stretch=tk.YES, minwidth=50)
        self.marks_list.column("description", width=100, stretch=tk.YES, minwidth=100)

        self.marks_list.bind("<<TreeviewSelect>>", self.on_schema_select)

        button_frame = Frame(self.left_panel)
        button_frame.pack(pady=10)

        Button(button_frame, text="Добавить", command=self.add_image).pack(side="left", padx=5)
        Button(button_frame, text="Удалить", command=self.destroy, state=DISABLED).pack(side="left", padx=5)

    def create_right_panel(self):
        self.right_panel = ttk.Frame(self.paned_window, width=500)
        self.paned_window.add(self.right_panel, minsize=500)

        self.image_canvas = tk.Canvas(self.right_panel, bg='white')
        self.image_canvas.pack(fill=tk.BOTH, expand=True)

    def fill_form(self):
        mark = self.controller.get_mark(self.mark_id)
        mark_images = self.controller.get_mark_images(self.mark_id)

        for item in self.marks_list.get_children():
            self.marks_list.delete(item)
        if len(mark_images) > 0:
            for item in mark_images:
                self.marks_list.insert("", tk.END, values=(item.id, mark.name, item.description))

            first_item = self.marks_list.get_children()[0]
            self.marks_list.selection_set(first_item)
            self.marks_list.focus(first_item)

    def add_image(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=(
                ("Изображения", "*.jpg *.jpeg *.png *.gif *.bmp"),
            )
        )
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    name = os.path.basename(file_path)

                    mark_image = MarkImage(
                        name=name,
                        data=file_data,
                        description="",
                        mark_id=self.mark_id
                    )
                    self.tmpMarks.append(mark_image)
                    tmp_id = 0 - len(self.tmpMarks)
                    self.marks_list.insert("", tk.END, values=(tmp_id, mark_image.name, mark_image.description))

            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка добавление файла: {e}")

    def on_schema_select(self, event):
        selected_item = self.marks_list.selection()
        if selected_item:
            item = self.marks_list.item(selected_item)
            mark_id = item['values'][0]
            self.update_schema_info(mark_id)

    def update_schema_info(self, mark_id):
        if mark_id < 0:
            tmp = mark_id * -1 - 1
            data = self.tmpMarks[tmp].data
        else:
            item = self.controller.get_mark_image(mark_id)
            data = item.data
        self.display_image(data)

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

    def clear_image_display(self):
        self.image_canvas.delete("all")
        if hasattr(self.image_canvas, 'image'):
            del self.image_canvas.image
