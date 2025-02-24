import customtkinter as ctk
import speedtest
import socket
import requests
import time
from threading import Thread

def bytes_to_mb(bytes):
    KB = 1024  # One Kilobyte is 1024 bytes
    MB = KB * 1024  # One MB is 1024 KB
    return int(bytes/MB)

def check_proxy():
    try:
        response = requests.get('https://www.google.com', timeout=5)
        return False
    except requests.exceptions.ProxyError:
        return True

def ping_server():
    try:
        host = "google.com"
        port = 80
        socket.setdefaulttimeout(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start_time = time.time()  # Используем time.time() для получения текущего времени
        s.connect((host, port))
        end_time = time.time()
        s.close()
        return round((end_time - start_time) * 1000)  # Время в миллисекундах
    except (socket.timeout, socket.error):
        return None

def run_speed_test():
    speed_test = speedtest.Speedtest()
    
    # Get a list of available servers
    servers = speed_test.get_best_server()
    
    # Update progress bar and labels
    download_progress.start()
    upload_progress.start()
    
    def test():
        download_speed = bytes_to_mb(speed_test.download())
        upload_speed = bytes_to_mb(speed_test.upload())
        
        download_progress.stop()
        upload_progress.stop()
        
        download_label.configure(text=f"Cкорость загруки: {download_speed} MB/s")
        upload_label.configure(text=f"Cкорость выгрузки: {upload_speed} MB/s")
        
        if check_proxy():
            proxy_checkbox.select()
        else:
            proxy_checkbox.deselect()
        
        ping_value = ping_server()
        if ping_value:
            ping_label.configure(text=f"Ping: {ping_value} ms")
        else:
            ping_label.configure(text="Ping: timeout")
    
    Thread(target=test).start()
    
# Настройка GUI
app = ctk.CTk()
app.title("Скорость интернета")

start_button = ctk.CTkButton(app, text="тест", command=run_speed_test)
start_button.grid(row=0, column=0, columnspan=2, pady=10)

# Прогресс-бар и метка для скорости загрузки
download_label = ctk.CTkLabel(app, text="Cкорость загрузки: - MB/s")
download_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

download_progress = ctk.CTkProgressBar(app, orientation="horizontal", mode="indeterminate")
download_progress.grid(row=1, column=1, padx=5, pady=5)

# Прогресс-бар и метка для скорости выгрузки
upload_label = ctk.CTkLabel(app, text="Cкорость выгрузки: - MB/s")
upload_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

upload_progress = ctk.CTkProgressBar(app, orientation="horizontal", mode="indeterminate")
upload_progress.grid(row=2, column=1, padx=5, pady=5)

# Чекбокс для отображения использования прокси
proxy_checkbox = ctk.CTkCheckBox(app, text="Используется прокси", state="disabled")
proxy_checkbox.grid(row=3, column=0, sticky="w", padx=5, pady=5)

# Метка для отображения пинга
ping_label = ctk.CTkLabel(app, text="Ping (по google.com): - ms")
ping_label.grid(row=3, column=1, sticky="w", padx=5, pady=5)

app.mainloop()