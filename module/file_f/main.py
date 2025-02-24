import os
import customtkinter as ctk
from tkinter import filedialog, Listbox
import asyncio
from concurrent.futures import ThreadPoolExecutor

class Frame3(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.currentPath = ctk.StringVar(value=os.getcwd())
        self.listbox = Listbox(self)
        self.listbox.pack(fill=ctk.BOTH, expand=True)
        self.size_cache = {}
        self.executor = ThreadPoolExecutor(max_workers=4)

        self.listbox.bind('<Double-1>', self.changePathByClick)
        self.listbox.bind('<Return>', self.changePathByClick)
        select_button = ctk.CTkButton(self, text="Выберите путь", command=self.select_directory)
        select_button.pack(pady=10)
        back_button = ctk.CTkButton(self, text="Назад", command=self.goBack)
        back_button.pack(pady=10)

    def select_directory(self):
        folder_selected = filedialog.askdirectory()
        if not folder_selected:
            return

        self.currentPath.set(folder_selected)
        asyncio.run(self.update_file_list(folder_selected))

    async def get_file_size(self, file_path):
        return os.path.getsize(file_path)

    async def get_folder_size(self, folder_path):
        total_size = 0
        try:
            with os.scandir(folder_path) as it:
                for entry in it:
                    if entry.is_file():
                        total_size += entry.stat().st_size
                    elif entry.is_dir():
                        total_size += await self.get_folder_size(entry.path)
        except PermissionError:
            # print(f"Permission denied: {folder_path}")
            a=2
        return total_size

    async def process_folder(self, folder_path):
        size = await self.get_folder_size(folder_path)
        return size

    async def process_files_and_folders(self, root_path):
        items = os.listdir(root_path)
        sizes = {}

        for item in items:
            item_path = os.path.join(root_path, item)
            if item_path in self.size_cache:
                sizes[item] = self.size_cache[item_path]
                continue

            if os.path.isdir(item_path):
                size = await self.process_folder(item_path)
                sizes[item] = size
            elif os.path.isfile(item_path):
                size = await self.get_file_size(item_path)
                sizes[item] = size

            self.size_cache[item_path] = sizes[item]

        return sizes

    def goBack(self, event=None):
        newPath = os.path.dirname(self.currentPath.get())
        self.currentPath.set(newPath)
        asyncio.run(self.update_file_list(newPath))
        print('Going Back to:', newPath)

    async def update_file_list(self, path):
        try:
            directory = os.listdir(path)
        except FileNotFoundError:
            return

        self.listbox.delete(0, ctk.END)

        items_sizes = await self.process_files_and_folders(path)

        sorted_items = sorted(items_sizes.items(), key=lambda item: item[1], reverse=True)

        for item, size in sorted_items:
            if os.path.isdir(os.path.join(path, item)):
                formatted_line = f"{item:<50} {size // (1024 * 1024)} MB"
            else:
                formatted_line = f"{item:<50} {size // (1024 * 1024)} MB"
            self.listbox.insert(ctk.END, formatted_line)

    def changePathByClick(self, event=None):
        selected_index = self.listbox.curselection()
        if selected_index:
            picked = self.listbox.get(selected_index)
            picked_name = picked[:50].strip()
            path = os.path.join(self.currentPath.get(), picked_name)

            if os.path.isfile(path):
                print('Opening: ' + path)
                os.startfile(path)
            elif os.path.isdir(path):
                self.currentPath.set(path)
                asyncio.run(self.update_file_list(path))

root = ctk.CTk()
root.title("File Explorer")
root.geometry("600x400")

frame = Frame3(root)
frame.pack(fill="both", expand=True)

root.mainloop()