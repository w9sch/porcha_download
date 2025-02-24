import customtkinter as ctk
import requests
import json

def send_request():
    url = url_entry.get("1.0", "end").strip()
    headers = headers_entry.get("1.0", "end").strip()
    payload = payload_entry.get("1.0", "end").strip()
    try:
        headers = json.loads(headers) if headers else {}
        payload = json.loads(payload) if payload else {}

        response = requests.request("GET", url, headers=headers, json=payload)
        response_text.delete("1.0", ctk.END)
        response_text.insert(ctk.END, response.text)
    except Exception as e:
        response_text.delete("1.0", ctk.END)
        response_text.insert(ctk.END, f"Error: {str(e)}")

app = ctk.CTk()
app.title("w")
ctk.CTkLabel(app, text="URL:").grid(row=0, column=0, sticky="w")
url_entry = ctk.CTkTextbox(app, width=500, height=100)
url_entry.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(app, text="Headers (JSON):").grid(row=1, column=0, sticky="w")
headers_entry = ctk.CTkTextbox(app, width=500, height=100)
headers_entry.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(app, text="Payload (JSON):").grid(row=2, column=0, sticky="w")
payload_entry = ctk.CTkTextbox(app, width=500, height=100)
payload_entry.grid(row=2, column=1, padx=5, pady=5)
send_button = ctk.CTkButton(app, text="Send Request", command=send_request)
send_button.grid(row=3, column=0, columnspan=2, pady=10)

ctk.CTkLabel(app, text="Ответ:").grid(row=4, column=0, sticky="w")
response_text = ctk.CTkTextbox(app, width=500, height=100)
response_text.grid(row=4, column=1, padx=5, pady=5)

app.mainloop()