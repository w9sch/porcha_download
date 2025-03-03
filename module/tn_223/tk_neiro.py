
import tkinter as tk
import customtkinter as ctk
import requests
import json

def send_request():
    user_message = input_text.get("1.0", tk.END).strip()
    selected_model = model_var.get()

    url = "https://api.blackbox.ai/api/chat"
    payload = json.dumps({
        "messages": [
            {
                "content": "пиши на русском, если нету запроса на другой язык, "+user_message,
                "role": "user"
            }
        ],
        "model": selected_model,
        "max_tokens": "1024"
    })

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        try:
            response_data = response.json()
            if 'content' in response_data:
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, response_data['content'])
            else:
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, json.dumps(response_data, ensure_ascii=False, indent=4))
        except json.JSONDecodeError:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "\n" + response.text)
    else:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {response.status_code} - {response.text}")

root = ctk.CTk()
root.title("Chat API Interface")

input_label = ctk.CTkLabel(root, text="Введите сообщение:")
input_label.pack()

input_text = ctk.CTkTextbox(root, height=100, width=500)
input_text.pack()

model_label = ctk.CTkLabel(root, text="Выберите модель:")
model_label.pack()

models = [
    "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
    "Qwen/QwQ-32B-Preview",
    "databricks/dbrx-instruct",
    "deepseek-ai/deepseek-llm-67b-chat",
    "mistralai/Mistral-Small-24B-Instruct-2501",
    "deepseek-ai/DeepSeek-R1",
    "deepseek-ai/DeepSeek-V3"
]

model_var = ctk.StringVar(value=models[0])
model_menu = ctk.CTkComboBox(root, variable=model_var, values=models)
model_menu.pack()

send_button = ctk.CTkButton(root, text="Отправить", command=send_request)
send_button.pack()

output_label = ctk.CTkLabel(root, text="Ответ:")
output_label.pack()

output_text = ctk.CTkTextbox(root, height=200, width=500)
output_text.pack()

root.mainloop()

