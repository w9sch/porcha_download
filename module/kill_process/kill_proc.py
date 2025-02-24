import json
import psutil
import time
from tkinter import messagebox
import customtkinter as ctk

def load_vital_processes():
    try:
        with open('module\\kill_process\\process.json', 'r') as file:
            data = json.load(file)
            return set(data.get('vital_processes', []))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

vital_processes = load_vital_processes()

def is_vital_process(proc):
    return proc.name() in vital_processes

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Убийца процессов")
        self.geometry("400x400")
        
        self.kill_button = ctk.CTkButton(self, text="Убить процессы", command=self.kill_non_vital_processes)
        self.kill_button.pack(pady=20)
        
        self.process_entry = ctk.CTkEntry(self, placeholder_text="Введите имя процесса")
        self.process_entry.pack(pady=10)
        

        self.show_vital_button = ctk.CTkButton(self, text="Показать жизненно важные процессы", command=self.show_vital_processes)
        self.show_vital_button.pack(pady=10)

        self.add_vital_button = ctk.CTkButton(self, text="Добавить в жизненно важные", command=self.add_to_vital_processes)
        self.add_vital_button.pack(pady=10)

        self.remove_vital_combobox = ctk.CTkComboBox(self, values=list(vital_processes))
        self.remove_vital_combobox.pack(pady=10)

        self.remove_vital_button = ctk.CTkButton(self, text="Удалить из жизненно важных", command=self.remove_from_vital_processes)
        self.remove_vital_button.pack(pady=10)

        self.remove_vital_combobox.set("Выберите процесс для удаления")

    def kill_non_vital_processes(self):
        kol = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if not is_vital_process(proc):
                    kol += 1
                    print(f'Убит процесс: {proc.info["name"]} (PID: {proc.info["pid"]})')
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        messagebox.showinfo("Успех", f"Было завершено {kol} процессов")



    def show_vital_processes(self):
        process_list = "\n".join(vital_processes)
        messagebox.showinfo("Жизненно важные процессы", process_list)

    def add_to_vital_processes(self):
        process_name = self.process_entry.get()
        if process_name:
            vital_processes.add(process_name)
            messagebox.showinfo("Успех", f"Процесс {process_name} добавлен в жизненно важные процессы")
            self.save_vital_processes()
            self.update_combobox()
        else:
            messagebox.showwarning("Ошибка", "Введите имя процесса")

    def remove_from_vital_processes(self):
        process_name = self.remove_vital_combobox.get()
        if process_name:
            vital_processes.discard(process_name)
            messagebox.showinfo("Успех", f"Процесс {process_name} удален из жизненно важных процессов")
            self.save_vital_processes()
            self.update_combobox()
        else:
            messagebox.showwarning("Ошибка", "Выберите процесс для удаления")

    def update_combobox(self):
        self.remove_vital_combobox.configure(values=list(vital_processes))
        self.remove_vital_combobox.set("Выберите процесс для удаления")

    def save_vital_processes(self):
        with open('process.json', 'w') as file:
            json.dump({'vital_processes': list(vital_processes)}, file)

if __name__ == "__main__":
    app = App()
    app.mainloop()
